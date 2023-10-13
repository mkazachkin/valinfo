import os
import shutil
import ssl
import urllib.request
import urllib.error

import csv
import ftplib
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
        self._unzip = 'https://www.rkbti.ru/assessment/nfind/scripts/unzip.php'
        self._path = os.path.dirname(os.path.realpath(__file__))
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
        self._log.set_total_actions(6666)
        cursor = self._conn.cursor()
        for level1 in range(10):
            for level2 in range(10):
                for level3 in range(10):
                    select_str: str = f'''
                    SELECT
                        tc.cadnum_code,
                        tl.act_code,
                        dpt.param_annotation,
                        tp.value,
                        du.unit_annotation
                    FROM
                        t_parameter tp
                    LEFT JOIN t_parameter_annulment tpa ON
                        tp.param_id = tpa.param_id                        
                    LEFT JOIN l_xml_to_cadnum lxc ON
                        tp.link_id = lxc.link_id
                    LEFT JOIN t_cadnum tc ON
                        lxc.cadnum_id = tc.cadnum_id
                    LEFT JOIN t_list_xml tlx ON
                        lxc.xml_id = tlx.xml_id
                    LEFT JOIN t_list tl ON
                        tlx.list_id = tl.list_id
                    LEFT JOIN d_parameter_type dpt ON
                        tp.param_typ_id = dpt.param_typ_id
                    LEFT JOIN d_unit du ON
                        dpt.unit_id = du.unit_id
                    WHERE right(replace(tc.cadnum_code, ':', ''), 3) = '{level1}{level2}{level3}'
                        AND tpa.annulment_id IS NULL
                    ORDER BY
                        tc.cadnum_code,
                        tl.act_date,
                        dpt.param_typ_id;
                    '''
                    self._log.print_log("Запрос подготовлен",
                                        self._log.INFO, self._log.IS_ACTION)
                    cursor.execute(select_str)
                    self._log.print_log("Запрос выполнен",
                                        self._log.INFO, self._log.IS_ACTION)
                    result = cursor.fetchall()
                    self._log.print_log("Данные получены",
                                        self._log.INFO, self._log.IS_ACTION)
                    with open(os.path.join(self._path,
                                           'upload', 'db',
                                           str(level1), str(
                                               level2), str(
                                               level3),
                                           'data.csv'), 'w', newline='', encoding='utf-8') as csv_file:
                        writer = csv.writer(csv_file, delimiter='&')
                        writer.writerow(
                            tuple(['Кадастровый номер', 'Тур оценки', 'Характеристика', 'Значение',
                                   'Единица измерения']))
                        for row in result:
                            writer.writerow(row)
                    csv_file.close()
        cursor.close()
        self._conn.close()
        self._log.set_total_actions(21)
        self._log.set_current_action(round(10, 0))
        self._log.print_log("Данные сохранены",
                            self._log.INFO, self._log.IS_ACTION)    # 52 %
        try:
            os.remove(os.path.join(self._path, 'upload.zip'))
        except OSError:
            pass
        shutil.make_archive(os.path.join(self._path, 'upload', 'upload'), 'zip',
                            os.path.join(self._path, 'upload', 'db'))
        self._log.print_log("Данные подготовлены к загрузке",
                            self._log.INFO, self._log.IS_ACTION)    # 57 %

    def _send_to_web(self) -> None:
        """
        Отправляет на сайт сформированный файл с данными
        """
        zip_file = open(os.path.join(self._path, 'upload', 'upload.zip'), 'rb')
        f_blocksize = 1024
        total_size = os.path.getsize(os.path.join(
            self._path, 'upload', 'upload.zip'))
        actions = int(total_size / f_blocksize) + 1
        self._log.set_current_action(int(round(actions * 1.5, 0)))  # 60 %
        self._log.set_total_actions(actions + self._log.get_current_action())
        self._session.storbinary('STOR upload.zip', zip_file,
                                 callback=self._handle, blocksize=f_blocksize)
        self._log.print_log("Данные переданы")
        zip_file.close()
        self._session.quit()

    def _req_url(self, url: str) -> str:
        """
        Вызывает адрес в сети интернет и возвращает ответ
        Аргументы:
            url: str    - адрес в сети интернет
        """
        sert = ssl.create_default_context()
        sert.check_hostname = False
        sert.verify_mode = ssl.CERT_NONE
        try:
            with urllib.request.urlopen(url, context=sert) as answer:
                return answer.read().decode('utf-8')
        except urllib.error.URLError:
            self._log.print_log(
                'Вызов архиватора закончился ошибкой', self._log.ERROR)
            return 'failed'

    def _handle(self) -> None:
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
        url_answer = self._req_url(self._unzip)
        self._log.print_log(url_answer)
        if url_answer == 'success':
            self._log.print_log("ALL DONE")
        else:
            self._log.print_log(
                "Переданный файл не был разархивирован", self._log.ERROR)
