import psycopg2

from psycopg2.extensions import adapt
from psycopg2.extras import register_uuid


def prepare_sql(data: dict) -> list:
    """
    Готовит данные к загрузке в PostgreSQL, создавая список кортежей данных

    Аргументы:
        data: словарь с данными
    """
    register_uuid()
    result = list()
    for idx, data_row in data.items():
        val: object
        row = [psycopg2.extensions.adapt(val)
               if val is not None else None for val in data_row]
        row.insert(0, psycopg2.extensions.adapt(idx))
        result.append(tuple(row))
    return result
