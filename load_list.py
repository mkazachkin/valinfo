import argparse
from vi_controller.viapp import ViApp

parser = argparse.ArgumentParser(
    description='Загрузка перечня оценки в БД')
parser.add_argument('--puid', type=int, required=True,
                    help='Идентификатор статьи ФЗ, по которой производится оценка')
parser.add_argument('--rcode', type=str, required=True,
                    help='Исходящий номер сопроводительного письма с входящим перечнем')
parser.add_argument('--rdate', type=str, required=True,
                    help='Исходящая дата сопроводительного письма с входящим перечнем')
parser.add_argument('--icode', type=str, required=True,
                    help='Входящий номер сопроводительного письма с входящим перечнем')
parser.add_argument('--idate', type=str, required=True,
                    help='Входящая дата сопроводительного письма с входящим перечнем')
parser.add_argument('--fdate_f', type=str,
                    help='Начальная дата возникновения основания для определения КС ОН')
parser.add_argument('--fdate_l', type=str,
                    help='Конечная дата возникновения основания для определения КС ОН')
parser.add_argument('--adate', type=str,
                    help='Дата начала применения КС')
parser.add_argument('--path', type=str, required=True,
                    help='Путь к XML-файлам')
parser.add_argument('--host', dest='host', type=str, required=True,
                    default=None, help='Адрес сервера СУБД')
parser.add_argument('--name', dest='name', type=str, required=True,
                    default=None, help='Название базы даннных')
parser.add_argument('--user', dest='user', type=str, required=True,
                    default=None, help='Пользователь базы данных')
parser.add_argument('--pwrd', dest='pwrd', type=str, required=True,
                    default=None, help='Пароль доступа к базе данных')
args = parser.parse_args()

pre_kwargs = dict()
pre_kwargs['puid'] = args.puid
pre_kwargs['rcode'] = args.rcode
pre_kwargs['rdate'] = args.rdate
pre_kwargs['icode'] = args.icode
pre_kwargs['idate'] = args.idate
pre_kwargs['adate'] = args.adate
pre_kwargs['fdate_f'] = args.fdate_f
pre_kwargs['fdate_l'] = args.fdate_l
pre_kwargs['path'] = args.path
pre_kwargs['dbhost'] = args.host
pre_kwargs['dbname'] = args.name
pre_kwargs['dbuser'] = args.user
pre_kwargs['dbpwrd'] = args.pwrd

app = ViApp(**pre_kwargs)
if app.in_xml():
    print('Работа завершена успешно.')
else:
    print('Работа завершена с ошибкой.')
