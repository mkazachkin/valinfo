from uuid import uuid4
from uuid import UUID

from vi_service.adapter import prepare_sql
from vi_service.convertor import to_str
from vi_service.convertor import to_uuid


class TParameter:
    def __init__(self):
        self._fields: tuple = ('param_id', 'link_id', 'param_typ_id', 'value')
        self._types: tuple = (to_uuid, to_uuid, to_uuid, to_str)
        self._t_name = 't_parameter'
        self._data = dict()

    def add(self, link_id: UUID, param_typ_id: UUID, value: str) -> UUID:
        """
        Добавляет характеристику объекта из исходящего XML файла COST.
        Возвращает идентификатор характеристики.
        Если данные приходят в виде строк, то преобразует в соответствующий столбцу тип.

        Аргументы:
            link_id: UUID       - Идентификатор связи XML файла и объекта
            param_typ_id: UUID  - Идентификатор вида характеристики
            value: str          - Значение характеристики
        """
        param_id = uuid4()
        values = [link_id, param_typ_id, value]
        self._data[param_id] = tuple(self._types[i+1](values[i])
                                     for i in range(len(values)))
        return param_id

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
