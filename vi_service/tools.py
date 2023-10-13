import fnmatch
import os
import re

from bs4 import BeautifulSoup
from typing import Optional


def get_xml_list(path: str, masks: list) -> Optional[list]:
    """
    Возвращает список XML файлов в каталоге, соответствующих маске.
    Не чувствителен к регистру.

    Аргументы:
        path: str   - Путь к каталогу
        masks: list - Список масок файлов
    """
    result = list()
    for mask in masks:
        try:
            tmp_list = [file_name for file_name in os.listdir(
                path) if os.path.isfile(os.path.join(path, file_name))]
            tmp_list = [os.path.join(path, xml) for xml in tmp_list if re.match(
                fnmatch.translate(mask), xml, re.IGNORECASE)]
            result += tmp_list
        except FileNotFoundError:
            return None
    if len(result) == 0:
        return None
    return result


def get_soup(path: str) -> Optional[BeautifulSoup]:
    try:
        return BeautifulSoup(open(path, 'r', encoding='utf-8').read(), 'xml')
    except FileNotFoundError:
        return None
    except IOError:
        return None
