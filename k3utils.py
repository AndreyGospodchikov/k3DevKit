# -*- coding: cp1251 -*-
"""��������������� ������� ��� ������ � �3"""
import k3


def check_furntype(object, target):
    """��������� �� Furntype, �������� �� ���������� ������ ���, ��� �������� � target

    checks - ������� ��������. ���� - �������� ����, �������� - ������ � ��������� �� �������� �������� furntype."""

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
    """������� ���� k3 � �������� ������ �� text_list, ���������� caption � ������� ��� �������� � �������� button"""
    param = [caption, k3.k_msgbox, k3.k_text]
    param.extend(text_list)
    param.append(k3.k_done)
    param.append(button)
    param.append(k3.k_done)
    return k3.alternative(param)


def errwin(text=''):
    """������� ��������� � ���������� ������ � �������� ������� ������"""
    return msgwin([text], '������', 'Ok')


def current_folder():
    """���������� ������ � ������ ���� � �����, � ������� ��������� ������� �������� ���� k3"""
    result = ''
    path_list = k3.sysvar(2).split('\\')
    path_list.pop(-1)
    for entry in path_list:
        result = result + entry + '\\'
    return result[0:-1]
