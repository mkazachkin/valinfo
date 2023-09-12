import configparser
import csv
import ftplib
import os
import psycopg2

from vi_service.vilogger import ViLogger


class Data4Web:
    def __init__(self, **kwargs) -> None:
        self._log = ViLogger('upload.log')

        dbhost = kwargs.get('dbhost', None)
        dbname = kwargs.get('dbname', None)
        dbuser = kwargs.get('dbuser', None)
        dbpwrd = kwargs.get('dbpwrd', None)

        ftphost = kwargs.get('ftphost', None)
        ftppath = kwargs.get('ftppath', None)
        ftpuser = kwargs.get('ftpuser', None)
        ftppwrd = kwargs.get('ftppwrd', None)

        path_bak: str = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'data.bak')
        self._data: str = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'data.csv')

        if os.path.exists(path_bak):
            os.remove(path_bak)
            self._log.print_log('Старая резервная копия удалена.')
        if os.path.exists(self._data):
            os.rename(self._data, path_bak)
            self._log.print_log('Новая резервная копия создана.')

        self._log.print_log('Инициализация успешна.')

        self._conn = psycopg2.connect(host=dbhost, dbname=dbname,
                                      user=dbuser, password=dbpwrd)
        self._log.print_log('Соединение с БД установлено.')

        self._session = ftplib.FTP(ftphost, ftpuser, ftppwrd)
        self._session.cwd(ftppath)
        self._log.print_log("Соединение с FTP-сервером установлено")

    def _get_data(self) -> None:
        """
        Формирует файл с данными
        """
        select_str: str = '''
        select
            tc.cadnum_code,
            tl.list_code,
            dpt.param_annotation,
            tp.value,
            du.unit_annotation
        from
            t_parameter tp
        left join l_xml_to_cadnum lxc on
            tp.link_id = lxc.link_id
        left join t_cadnum tc on
            lxc.cadnum_id = tc.cadnum_id
        left join t_list_xml tlx on
            lxc.xml_id = tlx.xml_id
        left join t_list tl on
            tlx.list_id = tl.list_id
        left join d_parameter_type dpt on
            tp.param_typ_id = dpt.param_typ_id
        left join d_unit du on
            dpt.unit_id = du.unit_id
        order by
            tc.cadnum_code,
            tl.end_date,
            dpt.param_code;
        '''
        self._log.set_total_actions(11)
        cursor = self._conn.cursor()
        self._log.print_log("Запрос подготовлен",
                            self._log.INFO, self._log.IS_ACTION)
        cursor.execute(select_str)
        self._log.print_log("Запрос выполнен",
                            self._log.INFO, self._log.IS_ACTION)
        result = cursor.fetchall()
        self._log.print_log("Данные получены",
                            self._log.INFO, self._log.IS_ACTION)
        cursor.close()
        self._conn.close()

        with open(self._data, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter='&')
            writer.writerow(
                tuple(['Кадастровый номер', 'Тур оценки', 'Характеристика', 'Значение', 'Единица измерения']))
            for row in result:
                writer.writerow(row)
        csv_file.close()
        self._log.print_log("Данные сохранены",
                            self._log.INFO, self._log.IS_ACTION)

    def _send_to_web(self) -> None:
        """
        Отправляет на сайт сформированный файл с данными
        """
        csv_file = open(self._data, 'rb')
        f_blocksize = 1048576
        total_size = os.path.getsize(self._data)
        actions = int(total_size / f_blocksize) + 1
        self._log.set_current_action(round(actions / 1.5, 0))  # 40 %
        self._log.set_total_actions(actions + self._log.get_current_action())
        self._session.storbinary('STOR data.csv', csv_file,
                                 callback=self._handle, blocksize=f_blocksize)
        self._log.print_log("Данные переданы")
        csv_file.close()
        self._session.quit()

    def _handle(self, block) -> None:
        """
        Отправляет в лог-файл информацию о переданных блоках на сайт
        """
        self._log.print_log(
            f"Блок передан на сайт.", self._log.INFO, self._log.IS_ACTION)

    def run(self) -> None:
        """
        Выполняет всю последовательность действий для формирования файла с данными и передачи его на сайт
        """
        self._get_data()
        self._send_to_web()
        self._log.print_log("ALL DONE")
