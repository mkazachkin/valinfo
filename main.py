import argparse
from vi_controller.viapp import ViApp

parser = argparse.ArgumentParser(
    description='Добавление информации по перечням оценки')
parser.add_argument('inout', choices=['IN', 'OUT'],
                    help='Загрузка входящего (IN) или исходящих (OUT) перечней')
parser.add_argument('--puid', type=str,
                    help='Идентификатор статьи ФЗ, по которой производится оценка')
parser.add_argument('--luid', type=str,
                    help='Идентификатор перечня оценки')
parser.add_argument('--lcode', type=str,
                    help='Входящий номер перечня оценки')
parser.add_argument('--lanno', type=str,
                    help='Описание входящего перечня оценки')
parser.add_argument('--adate', type=str,
                    help='Дата применения кадастровой стоимости')
parser.add_argument('--sdate', type=str,
                    help='Дата начала работ по оценке перечня')
parser.add_argument('--edate', type=str,
                    help='Дата окончания работ по оценке перечня')
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
if args.inout == 'IN':
    if not args.puid:
        argparse.ArgumentError('the following arguments are required: --puid')
    if not args.lcode:
        argparse.ArgumentError('the following arguments are required: --lcode')
    if not args.sdate:
        argparse.ArgumentError('the following arguments are required: --sdate')
    pre_kwargs['path'] = args.path
    pre_kwargs['puid'] = args.puid
    pre_kwargs['luid'] = args.luid
    pre_kwargs['lcode'] = args.lcode
    pre_kwargs['lanno'] = args.lanno
    pre_kwargs['adate'] = args.adate
    pre_kwargs['sdate'] = args.sdate
    pre_kwargs['dbhost'] = args.host
    pre_kwargs['dbname'] = args.name
    pre_kwargs['dbuser'] = args.user
    pre_kwargs['dbpwrd'] = args.pwrd
    app = ViApp(**pre_kwargs)
    if app.in_xml():
        print('Работа завершена успешно.')
    else:
        print('Работа завершена с ошибкой.', 'Error')
if args.inout == 'OUT':
    if not args.luid:
        argparse.ArgumentError('the following arguments are required: --luid')
    if not args.edate:
        argparse.ArgumentError('the following arguments are required: --edate')
    pre_kwargs['path'] = args.path
    pre_kwargs['luid'] = args.luid
    pre_kwargs['edate'] = args.edate
    pre_kwargs['dbhost'] = args.host
    pre_kwargs['dbname'] = args.name
    pre_kwargs['dbuser'] = args.user
    pre_kwargs['dbpwrd'] = args.pwrd

    app = ViApp(**pre_kwargs)
    if app.out_xml():
        print('Работа завершена успешно.')
    else:
        print('Работа завершена с ошибкой.', 'Error')
