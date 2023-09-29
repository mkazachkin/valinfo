from datetime import date
from typing import Optional
from uuid import uuid4
from uuid import UUID

from vi_service.adapter import prepare_sql
from vi_service.convertor import to_date
from vi_service.convertor import to_int
from vi_service.convertor import to_str
from vi_service.convertor import to_uuid


class TList:
    def __init__(self):
        self._fields: tuple = ('list_id', 'paragraph_id', 'rr_code', 'rr_date', 'in_code', 'in_date',
                               'in_new_objects_num', 'in_old_objects_num', 'found_date_f', 'found_date_l',
                               'act_code', 'act_date', 'out_new_objects_rated', 'out_old_objects_rated',
                               'out_objects_not_rated')
        self._types: tuple = (to_uuid, to_int, to_str, to_date, to_str, to_date,
                              to_int, to_int, to_date, to_date,
                              to_str, to_date, to_int, to_int, to_int)
        self._t_name = 't_list'
        self._data = dict()
        self._cod = dict()
        self._ids = dict()

    def add(self, paragraph_id: int, rr_code: str, rr_date: date, in_code: str, in_date: date,
            in_new_objects_num: int, in_old_objects_num: int, found_date_f: date, found_date_l: date,
            act_code: str = None, act_date: date = None, out_new_objects_rated: int = None,
            out_old_objects_rated: int = None, out_objects_not_rated: int = None) -> UUID:
        """
        Добавляет информацию по перечню, если он не был добавлен ранее.
        Возвращает идентификатор перечня.
        Если данные приходят в виде строк, то преобразует в соответствующий столбцу тип.

        Аргументы:
            paragraph_id: int               - Идентификатор статьи ФЗ о кадастровой оценке
            rr_code: str                    - Исходящий номер сопроводительного письма с входящим перечнем
            rr_date: date                   - Дата сопроводительного письма с входящим перечнем
            in_code: str                    - Входящий номер сопроводительного письма с входящим перечнем
            in_date: date                   - Дата сопроводительного письма с входящим перечнем
            in_new_objects_num: int         - Количество вновь учтенных объектов во входящем перечне
            in_old_objects_num: int         - Количество ранее учтенных объектов во входящем перечне
            found_date_f: date              - Начальная дата периода возникновения основания для определения КС объектов входящего перечня
            found_date_l: date              - Конечная дата периода возникновения основания для определения КС объектов входящего перечня
            act_code: str                   - Номер акта определения КС
            act_date: date                  - Дата составления акта определения КС
            out_new_objects_rated: int      - Количество вновь учтенных объектов, для которых была проведена оценка КС
            out_old_objects_rated: int      - Количество ранее учтенных объектов, для которых была проведена оценка КС
            out_objects_not_rated: int      - Количество объектов, для которых определение кадастровой стоимости не проводилось
        """
        if in_code in self._cod.keys():
            list_id = self._cod[in_code]
        else:
            list_id = uuid4()
        values = [paragraph_id, rr_code, rr_date, in_code, in_date, in_new_objects_num, in_old_objects_num,
                  found_date_f, found_date_l, act_code, act_date, out_new_objects_rated, out_old_objects_rated, out_objects_not_rated]
        self._data[list_id] = tuple(self._types[i+1](values[i])
                                    for i in range(len(values)))
        self._cod[in_code] = list_id
        self._ids[list_id] = in_code
        return list_id

    def add_db(self, list_id: str, in_code: str):
        """
        Составляет словарь существующих в БД перечней.

        Аргументы:
            list_id: str    - Идентификатор кадастрового номера hex у UUID
            in_code: str    - Входящий номер сопроводительного письма с входящим перечнем
        """
        list_id: UUID = to_uuid(list_id)
        self._cod[in_code] = list_id
        self._ids[list_id] = in_code

    def get_id(self, in_code: str, gen_id: bool = True) -> Optional[UUID]:
        """
        Возвращает идентификатор перечня по регистрационному номеру или резервирует идентификатор, если его нет.

        Аргументы:
            in_code: str    - Входящий номер сопроводительного письма с входящим перечнем
            gen_id: bool    - Сгенерировать новый идентификатор, если он отсутствует
        """
        if gen_id:
            if not (in_code in self._cod.keys()):
                list_id = uuid4()
                self._cod[in_code] = list_id
                self._ids[list_id] = in_code
            return self._cod[to_str(in_code)]
        else:
            if not (in_code in self._cod.keys()):
                return None
            else:
                return self._cod[to_str(in_code)]

    def get_code(self, list_id: UUID) -> Optional[str]:
        """
        Возвращает регистрационный номер перечня по идентифиикатору.

        Аргументы:
            list_id: UUID   - Идентификатор входящего перечня
        """
        try:
            return self._ids[to_uuid(list_id)]
        except KeyError:
            return None

    @property
    def data(self) -> dict:
        """
        Возвращает словарь с данными
        """
        return self._data

    @property
    def prepared_data(self) -> list:
        """
        Возвращает список с данными, подготовленными к вставке в БД
        """
        return prepare_sql(self._data)

    @property
    def fields(self) -> str:
        """
        Возвращает строку со списком полей в БД
        """
        return '(' + ','.join(self._fields) + ')'

    @property
    def t_name(self) -> str:
        """
        Возвращает название теблицы в БД
        """
        return self._t_name
