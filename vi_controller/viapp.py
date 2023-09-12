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
            self._conn = psycopg2.connect(host=dbhost, dbname=dbname, user=dbuser, password=dbpwrd)
        except psycopg2.OperationalError:
            self._log.print_log('Ошибка подключения к БД.', self._log.ERROR)
            raise Exception()
        self._log.print_log('База данных подключена.')

        self._path = kwargs.get('path', None)
        self._lcode = kwargs.get('lcode', None)
        self._lanno = kwargs.get('lanno', None)
        self._adate = kwargs.get('adate', None)
        self._puid = convertor.to_uuid(kwargs.get('puid', None))
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
            self._log.print_log('Перечень с указанным номером уже был ранее загружен.', self._log.ERROR)
            return False
        self._log.print_log('Загрузка входящего перечня начата.')
        # Находим все входящие XML
        xml_files = get_xml_list(self._path, 'listinfo_*.xml')
        if xml_files is None:
            self._log.print_log('Входящие XML-файлы не найдены.', self._log.ERROR)
            return False

        flag: bool = False
        list_date: date = datetime.now().date()

        self._log.set_total_actions(len(xml_files) + 6)  # В обработке после всех файлов 6 таблиц
        self._log.print_log('Общее количество файлов для обработки: ' + str(self._log.get_total_actions() - 6))
        # Начинаем обработку каждого XML
        for xml in xml_files:
            self._log.print_log(f'Обработка файла {xml}', self._log.INFO, self._log.IS_ACTION)
            xml_soup: BeautifulSoup = get_soup(xml)
            if not xml_soup:
                return False

            xml_list_date = convertor.to_date(xml_soup.find('ListInfo')['DateForm'])
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
                self._log.print_log('Не найдена информация по перечню (ListInfo).', self._log.ERROR)
                return False
            xml_id = self._t_list_xml.add(self._luid, os.path.basename(xml), False)

            # Обрабатываем каждый из видов недвижимости и заполняем кадастровые номера
            for o_type in self._d_realty.keys():
                for realty_soup in xml_soup.select(o_type):
                    cadnum_id = self._t_cadnum.add(self._d_realty[o_type], realty_soup['CadastralNumber'])
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

    def out_xml(self) -> bool:
        """
        Считывает исходящие FD и COST XML файлы и парсит характеристики объектов недвижимости.
        Возвращает True, если операция завершилась успешно, False, если возникла ошибка.
        """
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
        self._log.set_total_actions(len(fd_files) + len(cost_files) + 5)  # В обработке после всех файлов 5 таблиц
        self._log.print_log('Общее количество файлов для обработки: ' + str(self._log.get_total_actions()-5))
        self._log.print_log('Загрузка исходящего FD перечня начата.')
        if not self._fd_xml(fd_files):
            return False
        self._log.print_log('Загрузка исходящего COST перечня начата.')
        if not self._cost_xml(cost_files):
            return False

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
            self._log.print_log(f'Обработка файла {xml}', self._log.INFO, self._log.IS_ACTION)
            xml_soup: BeautifulSoup = get_soup(xml)
            if not xml_soup:
                self._log.print_log(f'Не могу считать файл {xml}', self._log.ERROR)
                return False

            realty_groups = parser.group_dict(xml_soup)
            if not realty_groups:
                self._log.print_log(f'Не могу считать группы недвижимости в файле {xml}', self._log.ERROR)
                return False
            xml_id = self._t_list_xml.add(self._luid, os.path.basename(xml), True)
            for realty_soup in xml_soup.select('Real_Estate'):
                cadnum_code = realty_soup.find('CadastralNumber').get_text()
                cadnum_id = self._t_cadnum.get_id(cadnum_code)
                if not cadnum_id:
                    self._log.print_log(f'Кадастровый номер {cadnum_code} не найден во входящем списке.',
                                        self._log.ERROR)
                    return False
                link_id = self._l_xml_to_cadnum.add(xml_id, cadnum_id)
                self._t_parameter.add(link_id, parser.group_dict_id(), realty_groups[realty_soup['ID_Group']])
        return True

    def _cost_xml(self, xml_files: list) -> bool:
        """
        Считывает исходящий COST XML файлы и парсит характеристики объектов недвижимости.
        Возвращает True, если операция завершилась успешно, False, если возникла ошибка.

        арг
        """
        for xml in xml_files:
            self._log.print_log(f'Обработка файла {xml}', self._log.INFO, self._log.IS_ACTION)
            xml_soup: BeautifulSoup = get_soup(xml)
            if not xml_soup:
                return False
            xml_id = self._t_list_xml.add(self._luid, os.path.basename(xml), True)
            for realty_soup in xml_soup.select('Parcel'):
                cadnum_code = realty_soup['CadastralNumber']
                cadnum_id = self._t_cadnum.get_id(cadnum_code)
                if not cadnum_id:
                    self._log.print_log(f'Кадастровый номер {cadnum_code} не найден во входящем списке.',
                                        self._log.ERROR)
                    return False
                link_id = self._l_xml_to_cadnum.add(xml_id, cadnum_id)
                spec_cadcost = parser.spec_cadcost(realty_soup)
                self._t_parameter.add(link_id, spec_cadcost[0], spec_cadcost[1])
                cadcost = parser.cadcost(realty_soup)
                self._t_parameter.add(link_id, cadcost[0], cadcost[1])
        return True

    def _fill_cadnum(self) -> None:
        """
        Производит первичное заполнение перечня кадастровых номеров объектов
        """
        cursor = self._conn.cursor()
        cursor.execute(f'SELECT cadnum_id, cadnum_code FROM {self._t_cadnum.t_name};')
        for row in cursor.fetchall():
            self._t_cadnum.add_db(row[0], row[1])
        cursor.close()

    def _fill_list_codes(self) -> None:
        """
        Производит первичное заполнение перечня кадастровых номеров объектов
        """
        cursor = self._conn.cursor()
        cursor.execute(f'SELECT list_id, list_code FROM {self._t_list.t_name};')
        for row in cursor.fetchall():
            self._t_list.add_db(row[0], row[1])
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
        self._log.print_log(f"Таблица '{obj.t_name}' подготовлена к загрузке.", self._log.INFO, self._log.IS_ACTION)
