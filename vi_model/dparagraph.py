from typing import Optional
from uuid import UUID

from vi_service.adapter import prepare_sql
from vi_service.convertor import to_str
from vi_service.convertor import to_uuid


class DParagraph:
    def __init__(self):
        self._fields: tuple = (
            'paragraph_id', 'paragraph_code', 'paragraph_annotation')
        self._types: tuple = (to_uuid, to_str, to_str)
        self._t_name = 'd_paragraph'
        self._data = dict()
        self._cod = dict()
        self._ids = dict()

    def add(self, paragraph_id: str, paragraph_code: str, paragraph_annotation: str) -> None:
        """
        Добавляет статью ФЗ о кадастровой оценке в данные, если она не был добавлен ранее.
        Возвращает идентификатор статьи.
        Если данные приходят в виде строк, то преобразует в соответствующий столбцу тип.

        Аргументы:
            paragraph_id: str           - Идентификатор статьи ФЗ
            paragraph_code: str         - Код статьи ФЗ
            paragraph_annotation: str   - Описание статьи ФЗ
        """
        values = [paragraph_code, paragraph_annotation]
        self._data[paragraph_id] = (self._types[i+1](values[i])
                                    for i in range(len(values)))
        self._cod[paragraph_code] = paragraph_id
        self._ids[paragraph_id] = paragraph_code

    def get_id(self, paragraph_code: str) -> Optional[UUID]:
        """
        Возвращает идентификатор статьи ФЗ о кадастровой оценке по коду.

        Аргументы:
            paragraph_code: str - Код статьи ФЗ о кадастровой оценке
        """
        try:
            return self._cod[to_str(paragraph_code)]
        except KeyError:
            return None

    def get_code(self, paragraph_id: UUID) -> str:
        """
        Возвращает код статьи ФЗ о кадастровой оценке по идентифиикатору.

        Аргументы:
            paragraph_id: UUID  - Идентификатор статьи ФЗ о кадастровой оценке
        """
        return self._ids[to_uuid(paragraph_id)]

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
