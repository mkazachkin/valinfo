import dateutil.parser
import re
from datetime import datetime
from datetime import date
from typing import Optional
from uuid import UUID


def to_date(obj) -> Optional[date]:
    """
    Преобразует строку формата '%Y-%m-%d' в дату, если объект имеет тип данных str.
    Оставляет значение, если объект типа datetime.
    Возвращает дату в формате datetime или None, если преобразование не получилось.

    Аргументы:
        obj - объект для преобразования
    """
    if isinstance(obj, date):
        return obj
    elif isinstance(obj, datetime):
        return obj.date()
    else:
        try:
            return dateutil.parser.parse(re.sub(r'[^\d-]+', '', obj)[:10]).date()
        except (ValueError, TypeError):
            return None


def to_float(obj) -> Optional[float]:
    """
    Преобразует строку в число с плавающей точкой, если объект имеет тип данных str.
    Оставляет значение, если объект типа float.
    Возвращает целое число float или None, если преобразование не получилось.

    Аргументы:
        obj - объект для преобразования
    """
    if isinstance(obj, float):
        return obj
    try:
        return float(obj)
    except ValueError:
        return None
    except TypeError:
        return None


def to_int(obj) -> Optional[int]:
    """
    Преобразует строку в целое число, если объект имеет тип данных str.
    Оставляет значение, если объект типа int.
    Возвращает целое число int или None, если преобразование не получилось.

    Аргументы:
        obj - объект для преобразования
    """
    if isinstance(obj, int):
        return obj
    try:
        return int(obj)
    except ValueError:
        return None
    except TypeError:
        return None


def to_str(obj) -> Optional[str]:
    """
    Возвращает строковое представление объекта или None,
    если объект не имеет типа или строковое представление пустое.

    Аргументы:
        obj - объект для преобразования
    """
    if obj and str(obj) != '':
        return str(obj)
    else:
        return None


def to_uuid(obj) -> Optional[UUID]:
    """
    Преобразует строку идентификатор формата uuid, если объект имеет тип данных str.
    Оставляет значение, если объект типа float.
    Возвращает класс UUID или None, если преобразование не получилось.

    Аргументы:
        obj - объект для преобразования
    """
    if isinstance(obj, UUID):
        return obj
    try:
        return UUID(obj)
    except ValueError:
        return None
    except TypeError:
        return None


def to_bool(obj) -> Optional[bool]:
    """
    Преобразует строку вида '0' или '1' в bool, если объект имеет тип данных str.
    Оставляет значение, если объект типа bool.
    Возвращает класс bool или None, если преобразование не получилось.

    Аргументы:
        obj - объект для преобразования
    """
    if isinstance(obj, bool):
        return obj
    try:
        return str(obj) == '1'
    except TypeError:
        return None
