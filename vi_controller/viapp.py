import os

import psycopg2
import psycopg2.extensions
import psycopg2.extras

from bs4 import BeautifulSoup
from datetime import date, datetime

from vi_model import dictionary
from vi_model.lxmltocadnum import LXmlToCadnum
from vi_model.tcadnum import TCadnum
from vi_model.tlist import TList
from vi_model.tlistxml import TListXml
from vi_model.tparameter import TParameter
from vi_service import convertor, parser
from vi_service.tools import get_xml_list, get_soup
from vi_service.vilogger import ViLogger


class ViApp:
    __slots__ = ('_conn', '_in_params', '_d_realty', '_t_cadnum', '_t_list',
                 '_t_list_xml', '_l_xml_to_cadnum', '_t_parameter',
                 '_path', '_puid', '_luid', '_lcode', '_lanno',
                 '_sdate', '_edate', '_adate', '_log')

    def __init__(self, **kwargs):
        self._log = ViLogger('viapp.log')
        dbhost = kwargs.get('dbhost', None)
        dbname = kwargs.get('dbname', None)
        dbuser = kwargs.get('dbuser', None)
        dbpwrd = kwargs.get('dbpwrd', None)
        psycopg2.extras.register_uuid()
        try:
            self._conn = psycopg2.connect(
                host=dbhost, dbname=dbname, user=dbuser, password=dbpwrd)
        except psycopg2.OperationalError:
            self._log.print_log('Ошибка подключения к БД.', self._log.ERROR)
            raise Exception()
        self._log.print_log('База данных подключена.')

        self._path = kwargs.get('path', None)
        self._lcode = kwargs.get('lcode', None)
        self._lanno = kwargs.get('lanno', None)
        self._adate = kwargs.get('adate', None)
        self._puid = convertor.to_int(kwargs.get('puid', None))
        self._luid = convertor.to_uuid(kwargs.get('luid', None))
        self._sdate = convertor.to_date(kwargs.get('sdate', None))
        self._edate = convertor.to_date(kwargs.get('edate', None))

        self._in_params = {'Parcel': [parser.parcels,
                                      parser.area,
                                      parser.location,
                                      parser.category,
                                      parser.utilization,
                                      parser.fond_date]}
        self._d_realty = dictionary.d_realty
        self._t_cadnum = TCadnum()
        self._t_list = TList()
        self._t_list_xml = TListXml()
        self._l_xml_to_cadnum = LXmlToCadnum()
        self._t_parameter = TParameter()
        self._log.print_log('Объекты инициализиированы.')

        self._fill_list_codes()
        self._log.print_log('Список перечней синхронизирован.')
        self._fill_cadnum()
        self._log.print_log('Кадастровые номера синхронизированы.')

    def __del__(self):
        self._conn.close()

    def in_xml(self) -> bool:
        """
        Считывает входящий XML файл и парсит входящие характеристики объектов недвижимости.
        Возвращает True, если операция завершилась успешно, False, если возникла ошибка.
        """
        if self._t_list.get_id(self._lcode):
            self._log.print_log(
                'Перечень с указанным номером уже был ранее загружен.', self._log.ERROR)
            return False
        self._log.print_log('Загрузка входящего перечня начата.')
        # Находим все входящие XML
        xml_files = get_xml_list(self._path, 'listinfo_*.xml')
        if xml_files is None:
            self._log.print_log(
                'Входящие XML-файлы не найдены.', self._log.ERROR)
            return False

        flag: bool = False
        # Нужно инициализировать переменную
        list_date: date = datetime.now().date()

        # В обработке после всех файлов 6 таблиц
        self._log.set_total_actions(len(xml_files) + 6)
        self._log.print_log(
            'Общее количество файлов для обработки: ' + str(self._log.get_total_actions() - 6))
        # Начинаем обработку каждого XML
        for xml in xml_files:
            self._log.print_log(
                f'Обработка файла {xml}', self._log.INFO, self._log.IS_ACTION)
            xml_soup: BeautifulSoup = get_soup(xml)
            if not xml_soup:
                return False

            xml_list_date = convertor.to_date(
                xml_soup.find('ListInfo')['DateForm'])
            if xml_list_date:
                if not flag:
                    list_date = xml_list_date
                if flag and xml_list_date != list_date:
                    self._log.print_log(
                        f'Даты формирования файлов в перечне отличаются друг от друга {xml_list_date} - {list_date}.',
                        self._log.WARNING)
                list_date = xml_list_date
                if not flag:
                    # После того, как выявили дату составления перечня, добавляем его в БД и получаем id
                    self._luid = self._t_list.add(self._puid, self._lcode, self._lanno,
                                                  list_date, self._sdate)
                flag = True
            else:
                self._log.print_log(
                    'Не найдена информация по перечню (ListInfo).', self._log.ERROR)
                return False
            xml_id = self._t_list_xml.add(
                self._luid, os.path.basename(xml), False)

            # Обрабатываем каждый из видов недвижимости и заполняем кадастровые номера
            for o_type in self._d_realty.keys():
                for realty_soup in xml_soup.select(o_type):
                    cadnum_id = self._t_cadnum.add(
                        self._d_realty[o_type], realty_soup['CadastralNumber'])
                    link_id = self._l_xml_to_cadnum.add(xml_id, cadnum_id)
                    # Парсим входящиее характеристики объекта и добавляем их в БД
                    for param_func in self._in_params[o_type]:
                        param = param_func(realty_soup)
                        if param_func == parser.fond_date and self._adate:
                            param[1] = self._adate
                        if param[1] is not None:
                            self._t_parameter.add(link_id, param[0], param[1])

        self._insert_data(self._t_cadnum)
        self._insert_data(self._t_list)
        self._insert_data(self._t_list_xml)
        self._insert_data(self._l_xml_to_cadnum)
        self._insert_data(self._t_parameter)

        self._conn.commit()
        self._log.print_log('COMMIT', self._log.INFO, self._log.IS_ACTION)
        return True

    def out_xml(self, updating: bool = False) -> bool:
        """
        Считывает исходящие FD и COST XML файлы и парсит характеристики объектов недвижимости.
        Возвращает True, если операция завершилась успешно, False, если возникла ошибка.
        Аргументы:
            updating: bool  - флажок внесения исправлений в перечень. Если он установлен в True,
                              то добавлением данных в БД и коммитить будет метод исправления.
                              По-умолчанию False.
        """
        if not updating:
            # Да, это костыль. Возможно, потом переделаю
            cursor = self._conn.cursor()
            sql_str: str = f"UPDATE t_list SET end_date = '" + str(self._edate) + "' WHERE list_id = '" + \
                str(self._luid) + "';"
            cursor.execute(sql_str)
            cursor.close()

        fd_files = get_xml_list(self._path, 'fd_*.xml')
        cost_files = get_xml_list(self._path, 'cost_*.xml')
        if fd_files is None:
            self._log.print_log('FD-файлы не найдены.', self._log.ERROR)
            return False
        if cost_files is None:
            self._log.print_log('COST-файлы не найдены.', self._log.ERROR)
            return False
        if not updating:
            # В обработке после всех файлов 5 таблиц
            self._log.set_total_actions(len(fd_files) + len(cost_files) + 5)
        else:
            # Добавим еще несколько действий для переноса характеристик
            self._log.set_total_actions(len(fd_files) + len(cost_files) + 7)
        self._log.print_log(
            'Общее количество файлов для обработки: ' + str(self._log.get_total_actions()-5))
        self._log.print_log('Загрузка исходящего FD перечня начата.')
        if not self._fd_xml(fd_files):
            return False
        self._log.print_log('Загрузка исходящего COST перечня начата.')
        if not self._cost_xml(cost_files):
            return False
        if not updating:
            self._insert_data(self._t_list)
            self._insert_data(self._t_list_xml)
            self._insert_data(self._l_xml_to_cadnum)
            self._insert_data(self._t_parameter)

            self._conn.commit()
            self._log.print_log('COMMIT', self._log.INFO, self._log.IS_ACTION)
        return True

    def upd_xml(self) -> bool:
        """
        Получает характеристики из перечня, который исправляется и
        считывает исправленные исходящие FD и COST XML файлы.
        Возвращает True, если операция завершилась успешно, False, если возникла ошибка.
        """
        # Сохраним старый id перечня, чтобы потом взять из него нужные характеристики
        prev_luid = self._luid
        list_date = self._t_list.get_list_date(prev_luid)[0]
        start_date = self._t_list.get_list_date(prev_luid)[1]
        self._luid = self._t_list.add(self._puid, self._lcode, self._lanno,
                                      list_date, start_date, self._edate)
        if not self.out_xml(True):
            self._log.print_log(
                'Ошибка обработки исходящих файлов при обновлении.', self._log.ERROR)
            return False
        cadnum_to_fix = set()
        for link_info in self._l_xml_to_cadnum.data.values():
            cadnum_to_fix.add(link_info[1])
        self._log.print_log(
            'Перечень кадастровых номеров для переноса сформирован')
        cursor = self._conn.cursor()
        xml_name_to_fix = dict()
        for cadnum_id in cadnum_to_fix:
            sql_str = f"""
            SELECT tp.param_typ_id, tp.value, tlx.xml_name FROM t_parameter tp
            LEFT JOIN l_xml_to_cadnum lxtc ON tp.link_id = lxtc.link_id
            LEFT JOIN t_cadnum tc ON lxtc.cadnum_id = tc.cadnum_id
            LEFT JOIN t_list_xml tlx ON lxtc.xml_id = tlx.xml_id
            WHERE
            tc.cadnum_id = '{cadnum_id}' AND
            tlx.list_id = '{prev_luid}' AND
            param_typ_id <> 6000 AND
            param_typ_id <> 7000 AND
            param_typ_id <> 8000;
            """
            xml_link_to_fix = dict()
            self._log.print_log(sql_str)
            cursor.execute(sql_str)
            for row in cursor.fetchall():
                if not (row[2] in xml_name_to_fix.keys()):
                    xml_id = self._t_list_xml.add(self._luid, row[2], False)
                    xml_name_to_fix[row[2]] = xml_id
                else:
                    xml_id = xml_name_to_fix[row[2]]
                if not (cadnum_id in xml_link_to_fix.keys()):
                    link_id = self._l_xml_to_cadnum.add(xml_id, cadnum_id)
                    xml_link_to_fix[cadnum_id] = link_id
                else:
                    link_id = xml_link_to_fix[cadnum_id]
                self._t_parameter.add(link_id, row[0], row[1])
            input(self._t_list_xml.data)
        cursor.close()
        self._log.print_log(
            'Перенос характеристик из оригинального перечня завершен', self._log.INFO, self._log.IS_ACTION)
        self._insert_data(self._t_list)
        self._insert_data(self._t_list_xml)
        self._insert_data(self._l_xml_to_cadnum)
        self._insert_data(self._t_parameter)

        self._conn.commit()
        self._log.print_log('COMMIT', self._log.INFO, self._log.IS_ACTION)
        return True

    def _fd_xml(self, xml_files: list) -> bool:
        """
        Считывает исходящий FD XML файлы и парсит характеристики объектов недвижимости.
        Возвращает True, если операция завершилась успешно, False, если возникла ошибка.
        """
        for xml in xml_files:
            self._log.print_log(
                f'Обработка файла {xml}', self._log.INFO, self._log.IS_ACTION)
            xml_soup: BeautifulSoup = get_soup(xml)
            if not xml_soup:
                self._log.print_log(
                    f'Не могу считать файл {xml}', self._log.ERROR)
                return False

            realty_groups = parser.group_dict(xml_soup)
            if not realty_groups:
                self._log.print_log(
                    f'Не могу считать группы недвижимости в файле {xml}', self._log.ERROR)
                return False
            xml_id = self._t_list_xml.add(
                self._luid, os.path.basename(xml), True)
            for realty_soup in xml_soup.select('Real_Estate'):
                cadnum_code = realty_soup.find('CadastralNumber').get_text()
                cadnum_id = self._t_cadnum.get_id(cadnum_code)
                if not cadnum_id:
                    self._log.print_log(f'Кадастровый номер {cadnum_code} не найден во входящем списке.',
                                        self._log.ERROR)
                    return False
                link_id = self._l_xml_to_cadnum.add(xml_id, cadnum_id)
                self._t_parameter.add(link_id, parser.group_dict_id(
                ), realty_groups[realty_soup['ID_Group']])
        return True

    def _cost_xml(self, xml_files: list) -> bool:
        """
        Считывает исходящий COST XML файлы и парсит характеристики объектов недвижимости.
        Возвращает True, если операция завершилась успешно, False, если возникла ошибка.

        арг
        """
        for xml in xml_files:
            self._log.print_log(
                f'Обработка файла {xml}', self._log.INFO, self._log.IS_ACTION)
            xml_soup: BeautifulSoup = get_soup(xml)
            if not xml_soup:
                return False
            xml_id = self._t_list_xml.add(
                self._luid, os.path.basename(xml), True)
            for realty_soup in xml_soup.select('Parcel'):
                cadnum_code = realty_soup['CadastralNumber']
                cadnum_id = self._t_cadnum.get_id(cadnum_code)
                if not cadnum_id:
                    self._log.print_log(f'Кадастровый номер {cadnum_code} не найден во входящем списке.',
                                        self._log.ERROR)
                    return False
                link_id = self._l_xml_to_cadnum.add(xml_id, cadnum_id)
                spec_cadcost = parser.spec_cadcost(realty_soup)
                self._t_parameter.add(
                    link_id, spec_cadcost[0], spec_cadcost[1])
                cadcost = parser.cadcost(realty_soup)
                self._t_parameter.add(link_id, cadcost[0], cadcost[1])
        return True

    def _fill_cadnum(self) -> None:
        """
        Производит первичное заполнение перечня кадастровых номеров объектов
        """
        cursor = self._conn.cursor()
        cursor.execute(
            f'SELECT cadnum_id, cadnum_code FROM {self._t_cadnum.t_name};')
        for row in cursor.fetchall():
            self._t_cadnum.add_db(row[0], row[1])
        cursor.close()

    def _fill_list_codes(self) -> None:
        """
        Производит первичное заполнение списка перечней и их дат поступления
        """
        cursor = self._conn.cursor()
        cursor.execute(
            f'SELECT list_id, list_code, list_date, start_date FROM {self._t_list.t_name};')
        for row in cursor.fetchall():
            self._t_list.add_db(row[0], row[1], row[2], row[3])
        cursor.close()

    def _insert_data(self, obj) -> None:
        """
        Выполняет запросы для вставки данных в БД
        """
        cursor = self._conn.cursor()
        sql_str: str = f'INSERT INTO {obj.t_name} {obj.fields} VALUES %s; '
        psycopg2.extras.execute_values(
            cursor, sql_str, obj.prepared_data, template=None, page_size=100)
        cursor.close()
        self._log.print_log(
            f"Таблица '{obj.t_name}' подготовлена к загрузке.", self._log.INFO, self._log.IS_ACTION)
