# -*- coding: cp1251 -*-
"""Вспомогательные утилиты для работы с к3"""
import k3


def check_furntype(object, target):
    """Проверяет по Furntype, является ли переданный объект тем, что написано в target

    checks - словарь проверок. Ключ - название типа, значение - строка с проверкой по значению атрибута furntype."""

    checks = {
        'panel': 'furntype[:2] == \'01\' and not furntype[2:] == \'0000\'',
        'profile': 'furntype[:2] == \'02\'',
        'long': 'furntype[:2] == \'03\'',
        'accessory': 'furntype[:2] == \'04\'',
        'hand': 'furntype[:4] == \'0401\'',
        'leg': 'furntype[:4] == \'0402\'',
        'guide': 'furntype[:4] == \'0403\''
    }

    furntype = k3.getattr(object, 'FurnType', '')
    return eval(checks.get(target, 'False'))


def msgwin(text_list=(), caption='', button=''):
    """Выводит окно k3 с строками текста из text_list, заголовком caption и кнопкой для закрытия с надписью button"""
    param = [caption, k3.k_msgbox, k3.k_text]
    param.extend(text_list)
    param.append(k3.k_done)
    param.append(button)
    param.append(k3.k_done)
    return k3.alternative(param)


def errwin(text=''):
    """Выводит сообщение с заголовком Ошибка и заданной строкой текста"""
    return msgwin([text], 'Ошибка', 'Ok')


def current_folder():
    """Возвращает строку с полным путём к папке, в которой находится текущий открытый файл k3"""
    result = ''
    path_list = k3.sysvar(2).split('\\')
    path_list.pop(-1)
    for entry in path_list:
        result = result + entry + '\\'
    return result[0:-1]
