from typing import Optional
from uuid import uuid4
from uuid import UUID

from vi_service.adapter import prepare_sql
from vi_service.convertor import to_str
from vi_service.convertor import to_uuid


class TCadnum:
    def __init__(self):
        self._fields: tuple = ('cadnum_id', 'realty_id', 'cadnum_code')
        self._types: tuple = (to_uuid, to_uuid, to_str)
        self._t_name = 't_cadnum'
        self._db = dict()
        self._data = dict()
        self._cod = dict()
        self._ids = dict()

    def add(self, realty_id: UUID, cadnum_code: str) -> UUID:
        """
        Добавляет кадастровый номер в данные, если он не был добавлен ранее.
        Возвращает идентификатор кадастрвого номера.
        Если данные приходят в виде строк, то преобразует в соответствующий столбцу тип.

        Аргументы:
            realty_id: UUID     - Идентификатор вида объекта недвижимости
            cadnum_code: str    - Кадастровый номер
            cadnum_id: UUID     - Ранее присвоенный идентификатор объекта недвижимости
        """
        if cadnum_code in self._cod.keys():
            return self._cod[cadnum_code]
        else:
            cadnum_id = uuid4()
            values = [realty_id, cadnum_code]
            self._data[cadnum_id] = tuple(self._types[i+1](values[i])
                                          for i in range(len(values)))
            self._cod[cadnum_code] = cadnum_id
            self._ids[cadnum_id] = cadnum_code
            return cadnum_id

    def add_db(self, cadnum_id: str, cadnum_code: str):
        """
        Составляет словарь существующих в БД идентификаторов кадастровых номеров.

        Аргументы:
            cadnum_id: str      - Идентификатор кадастрового номера hex у UUID
            cadnum_code: str    - Кадастровый номер объекта
        """
        c_id: UUID = self._types[0](cadnum_id)
        self._cod[cadnum_code] = c_id
        self._ids[c_id] = cadnum_code

    def get_id(self, cadnum_code: str) -> Optional[UUID]:
        """
        Возвращает идентификатор кадастрового номера.

        Аргументы:
            cadnum_code: str    - Кадастровый номер
        """
        try:
            return self._cod[to_str(cadnum_code)]
        except KeyError:
            return None

    def get_code(self, cadnum_id: UUID) -> Optional[str]:
        """
        Возвращает кадастровый номер по идентифиикатору.

        Аргументы:
            cadnum_id: UUID - Идентификатор кадастрового номера
        """
        try:
            return self._ids[to_uuid(cadnum_id)]
        except KeyError:
            return None

    @property
    def data(self) -> dict:
        """
        Возвращает словарь с данными
        """
        return self._data

    @property
    def cadnums(self) -> dict:
        """
        Возвращает словарь с кадастровыми номерами и сопоставленными им идентификаторами
        """
        return self._cod

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
