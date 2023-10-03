import argparse
from vi_controller.viapp import ViApp


def to_bool(obj) -> bool:
    if isinstance(obj, bool):
        return obj
    return obj.lower() in ('yes', 'true', 't', 'y', '1')


parser = argparse.ArgumentParser(
    description='Загрузка результатов оценки в БД')
parser.add_argument('--luid', type=str, required=True,
                    help='Идентификатор перечня, результаты которого загружаются в БД')
parser.add_argument('--tcode', type=str, required=True,
                    help='Регистрационный номер акта оценки кадастровой стоимости')
parser.add_argument('--tdate', type=str, required=True,
                    help='Дата составления акта оценки кадастровой стоимости')
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
parser.add_argument('--updt', type=to_bool, required=True,
                    help='Признак загрузки исправленного перечня')
args = parser.parse_args()

pre_kwargs = dict()
pre_kwargs['luid'] = args.luid
pre_kwargs['tcode'] = args.tcode
pre_kwargs['tdate'] = args.tdate
pre_kwargs['path'] = args.path
pre_kwargs['dbhost'] = args.host
pre_kwargs['dbname'] = args.name
pre_kwargs['dbuser'] = args.user
pre_kwargs['dbpwrd'] = args.pwrd

app = ViApp(**pre_kwargs)
flag: bool = False
if args.updt:
    flag = app.upd_xml()
else:
    flag = app.out_xml()
if flag:
    print('Работа завершена успешно.')
else:
    print('Работа завершена с ошибкой.')
