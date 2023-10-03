from uuid import UUID
from uuid import uuid4

from vi_service.adapter import prepare_sql
from vi_service.convertor import to_uuid


class LXmlToCadnum:
    def __init__(self):
        self._fields: tuple = ('link_id', 'xml_id',
                               'cadnum_id')
        self._types: tuple = (to_uuid, to_uuid, to_uuid)
        self._t_name = 'l_xml_to_cadnum'
        self._data = dict()

    def add(self, xml_id: UUID, cadnum_id: UUID) -> UUID:
        """
        Добавляет идентификаторы кадастрового номера и XML файла в таблицу связи.
        Возвращает идентификатор связи.
        Если данные приходят в виде строк, то преобразует в соответствующий столбцу тип.

        Аргументы:
            xml_id: UUID        - Идентификатор XML файла
            cadnum_id: UUID     - Идентификатор кадастрового номера
        """
        link_id = uuid4()
        values = [xml_id, cadnum_id]
        self._data[link_id] = tuple(self._types[i+1](values[i])
                                    for i in range(len(values)))
        return link_id

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
