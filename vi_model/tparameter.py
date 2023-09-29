from uuid import uuid4
from uuid import UUID

from vi_service.adapter import prepare_sql
from vi_service.convertor import to_int
from vi_service.convertor import to_str
from vi_service.convertor import to_uuid
from vi_service.convertor import to_date


class TParameter:
    def __init__(self):
        self._fields: tuple = ('param_id', 'link_id', 'param_typ_id', 'value')
        self._types: tuple = (to_uuid, to_uuid, to_int, to_str)
        self._t_name = 't_parameter'
        self._data = dict()
        self._fdate_f = to_date('2099/01/01')
        self._fdate_l = to_date('1800/01/01')

    def add(self, link_id: UUID, param_typ_id: int, value: str) -> UUID:
        """
        Добавляет характеристику объекта из исходящего XML файла COST.
        Возвращает идентификатор характеристики.
        Если данные приходят в виде строк, то преобразует в соответствующий столбцу тип.

        Аргументы:
            link_id: UUID       - Идентификатор связи XML файла и объекта
            param_typ_id: int   - Идентификатор вида характеристики
            value: str          - Значение характеристики
        """
        param_id = uuid4()
        values = [link_id, param_typ_id,
                  value.replace('\t', ' ').replace('\n', ' ').replace('&', '_amp;').strip()]
        self._data[param_id] = tuple(self._types[i+1](values[i])
                                     for i in range(len(values)))
        # Если у нас характеристика - это дата добавления в ЕГРН, то запоминаем ее
        if param_typ_id == 9000 and to_date(value) < self._fdate_f:
            self._fdate_f = to_date(value)
        if param_typ_id == 9000 and to_date(value) > self._fdate_l:
            self._fdate_l = to_date(value)
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

    @property
    def found_dates(self) -> list:
        """
        Возвращает список с первой и последней датой периода возникновения основания для определения КС
        """
        return [self._fdate_f, self._fdate_l]
