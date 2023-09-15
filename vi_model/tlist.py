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
        self._fields: tuple = ('list_id', 'paragraph_id', 'list_code',
                               'list_annotation', 'list_date', 'start_date', 'end_date')
        self._types: tuple = (to_uuid, to_int, to_str,
                              to_str, to_date, to_date, to_date)
        self._t_name = 't_list'
        self._data = dict()
        self._cod = dict()
        self._ids = dict()
        self._dates = dict()

    def add(self, paragraph_id: int, list_code: str, list_annotation: str, list_date: date,
            start_date: date, end_date: str = None) -> UUID:
        """
        Добавляет информацию по перечню, если он не был добавлен ранее.
        Возвращает идентификатор перечня.
        Если данные приходят в виде строк, то преобразует в соответствующий столбцу тип.

        Аргументы:
            paragraph_id: int       - Идентификатор статьи ФЗ о кадастровой оценке
            list_code: str          - Регистрационный номер перечня
            list_annotation: str    - Комментарии к перечню
            list_date: date         - Дата формирования перечня
            start_date: date        - Дата начала работы по перечню
            start_date: date        - Дата окончания работы по перечню
        """
        if list_code in self._cod.keys():
            return self._cod[list_code]
        else:
            list_id = uuid4()
            values = [paragraph_id, list_code, list_annotation,
                      list_date, start_date, end_date]
            self._data[list_id] = tuple(self._types[i+1](values[i])
                                        for i in range(len(values)))
            self._cod[list_code] = list_id
            self._ids[list_id] = list_code
            self._dates[list_id] = list_date
            return list_id

    def add_db(self, list_id: str, list_code: str, list_date: str, start_date: str):
        """
        Составляет словарь существующих в БД перечней.

        Аргументы:
            list_id: str    - Идентификатор кадастрового номера hex у UUID
            list_code: str  - Кадастровый номер объекта
            list_date: str  - Дата составления перечня
            start_date: str - Дата начала работ по перечню
        """
        l_id: UUID = self._types[0](list_id)
        self._cod[list_code] = l_id
        self._ids[l_id] = list_code
        self._dates[l_id] = [self._types[4](
            list_date), self._types[5](start_date)]

    def get_id(self, list_code: str) -> Optional[UUID]:
        """
        Возвращает идентификатор перечня по регистрационному номеру.

        Аргументы:
            cadnum_code: str    - Кадастровый номер
        """
        try:
            return self._cod[to_str(list_code)]
        except KeyError:
            return None

    def get_code(self, list_id: UUID) -> Optional[str]:
        """
        Возвращает регистрационный номер перечня по идентифиикатору.

        Аргументы:
            list_id: UUID   - Идентификатор кадастрового номера
        """
        try:
            return self._ids[to_uuid(list_id)]
        except KeyError:
            return None

    def get_list_date(self, list_id: UUID) -> Optional[date]:
        """
        Возвращает дату составления перечня.

        Аргументы:
            list_id: UUID   - Идентификатор кадастрового номера
        """
        try:
            return self._dates[to_uuid(list_id)]
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
