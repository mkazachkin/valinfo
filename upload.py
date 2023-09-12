import argparse

from vi_php.data4web import Data4Web

parser = argparse.ArgumentParser(
    description='Загрузка информации по кадастровой оценке на сайт')

parser.add_argument('--host', dest='host', type=str, required=True,
                    default=None, help='Адрес сервера СУБД')
parser.add_argument('--name', dest='name', type=str, required=True,
                    default=None, help='Название базы даннных')
parser.add_argument('--user', dest='user', type=str, required=True,
                    default=None, help='Пользователь базы данных')
parser.add_argument('--pwrd', dest='pwrd', type=str, required=True,
                    default=None, help='Пароль доступа к базе данных')
parser.add_argument('--ftphost', dest='ftphost', type=str, required=True,
                    default=None, help='Адрес FTP-сервера')
parser.add_argument('--ftppath', dest='ftppath', type=str, required=True,
                    default=None, help='Каталог хранения данных на FTP-сервере')
parser.add_argument('--ftpuser', dest='ftpuser', type=str, required=True,
                    default=None, help='Пользователь FTP-сервера')
parser.add_argument('--ftppwrd', dest='ftppwrd', type=str, required=True,
                    default=None, help='Пароль доступа к FTP-серверу')
args = parser.parse_args()
pre_kwargs = dict()

pre_kwargs['dbhost'] = args.host
pre_kwargs['dbname'] = args.name
pre_kwargs['dbuser'] = args.user
pre_kwargs['dbpwrd'] = args.pwrd
pre_kwargs['ftphost'] = args.ftphost
pre_kwargs['ftppath'] = args.ftppath
pre_kwargs['ftpuser'] = args.ftpuser
pre_kwargs['ftppwrd'] = args.ftppwrd

upload = Data4Web(**pre_kwargs)
upload.run()
