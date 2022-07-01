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


def materials_from_subst(subst):
    """Возвращает список с номерами материалов номенклатуры из заданной группы подстановки"""
    result = []
    arr = k3.VarArray(1, 'arr')
    items_number = k3.npgetbywgere(1, '', 'arr', subst)
    arr = k3.VarArray(int(items_number), 'arr')
    items_number = k3.npgetbywgere(1, '', 'arr', subst)
    for member in arr:
        result.append(int(member.value))
    return result


def print_name(object):
    """Возвращает содержимое атрибута ElemName объекта"""
    name = k3.getattr(object, 'ElemName', 'No ElemName')
    print(name)


def select_to_list():
    """Возвращает список из объектов, которые были выбраны через select"""
    result = []
    for selnum in range(int(k3.sysvar(61))):
        result.append(k3.getselnum(selnum+1))
    return result


def body_select(body, stayblink=0, partly=0, byattr=0, filter=''):
    """Возвращает список объектов, имеющих общие точки с заданным телом
        body - тело
        stayblink, partly - режимы для выбора
        byattr - выбор с фильтром по атрибутам
        filter - строка с фильтром по атрибутам"""
    select_parameters = []
    if stayblink:
        select_parameters.append(k3.k_stayblink)
    if partly:
        select_parameters.append(k3.k_partly)
    select_parameters.extend([k3.k_all, k3.k_done])
    if not byattr:
        k3.select(select_parameters)
    else:
        byattr_parameters = [filter]
        byattr_parameters.extend(select_parameters)
        k3.selbyattr(byattr_parameters)
    selected_list = select_to_list()
    return [obj for obj in selected_list if k3.distance(k3.k_object, body, k3.k_object, obj) == 0]
