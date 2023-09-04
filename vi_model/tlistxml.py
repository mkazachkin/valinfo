from uuid import uuid4
from uuid import UUID

from vi_service.adapter import prepare_sql
from vi_service.convertor import to_bool
from vi_service.convertor import to_str
from vi_service.convertor import to_uuid


class TListXml:
    def __init__(self):
        self._fields: tuple = ('xml_id', 'list_id', 'xml_name', 'is_result')
        self._types: tuple = (to_uuid, to_uuid, to_str, to_bool)
        self._t_name = 't_list_xml'
        self._data = dict()

    def add(self, list_id: UUID, xml_name: str, is_result: bool) -> UUID:
        """
        Добавляет XML файл в список обработанных файлов, возвращает идентификатор файла.
        Если данные приходят в виде строк, то преобразует в соответствующий столбцу тип.

        Аргументы:
            list_id: UUID       - Идентификатор перечня, по которому сформирован файл
            xml_name: str  - Имя файла
        """
        xml_id = uuid4()
        values = [list_id, xml_name, is_result]
        self._data[xml_id] = tuple(self._types[i + 1](values[i])
                                   for i in range(len(values)))
        return xml_id

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
