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
        return ['05553d82-ee6a-4403-8d36-5bbca0d0b71a', dictionary.d_parcels[realty_soup.find('Name').get_text()]]
    except (AttributeError, KeyError, TypeError):
        return ['05553d82-ee6a-4403-8d36-5bbca0d0b71a', None]


def area(realty_soup: BeautifulSoup) -> list:
    """
    Площадь
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return ['e5d72f5b-aff1-4e68-9fd0-f18ec505fd3e', realty_soup.find('Area').find('Area').get_text()]
    except (AttributeError, TypeError):
        return ['e5d72f5b-aff1-4e68-9fd0-f18ec505fd3e', None]


def location(realty_soup: BeautifulSoup) -> list:
    """
    Площадь
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return ['7b885d26-3083-499d-bde8-959c08999e00', realty_soup.find('ReadableAddress').get_text()]
    except (AttributeError, TypeError):
        return ['7b885d26-3083-499d-bde8-959c08999e00', None]


def category(realty_soup: BeautifulSoup) -> list:
    """
    Категория земель
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return ['33e95a82-e9f5-483d-870b-4d2574e1d36e',
                dictionary.d_categories[realty_soup.find('Category').get_text()]]
    except (AttributeError, TypeError):
        return ['33e95a82-e9f5-483d-870b-4d2574e1d36e', None]


def utilization(realty_soup: BeautifulSoup) -> list:
    """
    Вид разрешенного использования
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return ['55f94c3f-8685-46f2-999d-4e206ec9a517',
                dictionary.d_util[realty_soup.find('Utilization')['Utilization']]]
    except (AttributeError, TypeError):
        return ['55f94c3f-8685-46f2-999d-4e206ec9a517', None]
    except KeyError:
        try:
            return ['55f94c3f-8685-46f2-999d-4e206ec9a517',
                    dictionary.d_util[realty_soup.find('Utilization')['PermittedUseText']]]
        except KeyError:
            try:
                return ['55f94c3f-8685-46f2-999d-4e206ec9a517',
                        dictionary.d_util[realty_soup.find('Utilization')['ByDoc']]]
            except KeyError:
                return ['55f94c3f-8685-46f2-999d-4e206ec9a517', None]


def cadcost(realty_soup: BeautifulSoup) -> list:
    """
    Кадастровая стоимость
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return ['776b49df-7499-4b89-992e-5adf6d6c7d31', realty_soup.find('CadastralCost')['Value']]
    except (AttributeError, KeyError, TypeError):
        return ['776b49df-7499-4b89-992e-5adf6d6c7d31', None]


def spec_cadcost(realty_soup: BeautifulSoup) -> list:
    """
    Удельный показатель кадастровой стоимости
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return ['4fd24453-7cd8-4378-a212-57870da84d06', realty_soup.find('Specific_CadastralCost')['Value']]
    except (AttributeError, KeyError, TypeError):
        return ['4fd24453-7cd8-4378-a212-57870da84d06', None]


def fond_date(realty_soup: BeautifulSoup) -> list:
    """
    Дата применения кадастровой стоимости
    Возвращает id характеристики и ее значение из XML

    Аргументы:
        realty_soup: soup   - Ссылка на XML объекта недвижимости
    """
    try:
        return ['c71efc65-648d-4429-b1bb-23a62a933285', realty_soup['FoundationDate']]
    except (AttributeError, KeyError, TypeError):
        return ['c71efc65-648d-4429-b1bb-23a62a933285', None]


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
            result[realty_gr.find('ID_Group').get_text()] = realty_gr.find('Name_Group').get_text()
        except (AttributeError, KeyError, TypeError):
            return None
    return result


def group_dict_id() -> UUID:
    """
    Возвращает идентификатор значения группы расчета
    """
    return UUID('05250279-376a-4793-82d4-4ab1ff3b0626')
