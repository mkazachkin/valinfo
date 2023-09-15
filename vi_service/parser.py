from bs4 import BeautifulSoup
from typing import Optional
from uuid import UUID

from vi_model import dictionary


def parcels(realty_soup: BeautifulSoup) -> list:
    """
    Вид земельного участка
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return [1000, dictionary.d_parcels[realty_soup.find('Name').get_text()]]
    except (AttributeError, KeyError, TypeError):
        return [1000, None]


def area(realty_soup: BeautifulSoup) -> list:
    """
    Площадь
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return [2000, realty_soup.find('Area').find('Area').get_text()]
    except (AttributeError, TypeError):
        return [2000, None]


def location(realty_soup: BeautifulSoup) -> list:
    """
    Площадь
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return [3000, realty_soup.find('ReadableAddress').get_text()]
    except (AttributeError, TypeError):
        return [3000, None]


def category(realty_soup: BeautifulSoup) -> list:
    """
    Категория земель
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return [4000,
                dictionary.d_categories[realty_soup.find('Category').get_text()]]
    except (AttributeError, TypeError):
        return [4000, None]


def utilization(realty_soup: BeautifulSoup) -> list:
    """
    Вид разрешенного использования
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return [5000, dictionary.d_util[realty_soup.find('Utilization')['Utilization']]]
    except (AttributeError, TypeError):
        return [5000, None]
    except KeyError:
        try:
            return [5000, dictionary.d_util[realty_soup.find('Utilization')['PermittedUseText']]]
        except KeyError:
            try:
                return [5000, dictionary.d_util[realty_soup.find('Utilization')['ByDoc']]]
            except KeyError:
                return [5000, None]


def spec_cadcost(realty_soup: BeautifulSoup) -> list:
    """
    Удельный показатель кадастровой стоимости
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return [6000, realty_soup.find('Specific_CadastralCost')['Value']]
    except (AttributeError, KeyError, TypeError):
        return [6000, None]


def cadcost(realty_soup: BeautifulSoup) -> list:
    """
    Кадастровая стоимость
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return [7000, realty_soup.find('CadastralCost')['Value']]
    except (AttributeError, KeyError, TypeError):
        return [7000, None]


def group_dict(realty_soup: BeautifulSoup) -> Optional[dict]:
    """
    Составляет словарь групп оценки в FD-файле XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML
    """
    result = dict()
    gr_soup = realty_soup.select('Group_Real_Estate')
    for realty_gr in gr_soup:
        try:
            result[realty_gr.find('ID_Group').get_text()] = realty_gr.find(
                'Name_Group').get_text()
        except (AttributeError, KeyError, TypeError):
            return None
    return result


def group_dict_id() -> UUID:
    """
    Возвращает идентификатор значения группы расчета
    """
    return 8000


def fond_date(realty_soup: BeautifulSoup) -> list:
    """
    Дата применения кадастровой стоимости
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return [9000, realty_soup['FoundationDate']]
    except (AttributeError, KeyError, TypeError):
        return [9000, None]
