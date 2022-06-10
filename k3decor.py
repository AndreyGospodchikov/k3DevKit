# coding=cp1251

"""������ � ������������ ��� k3

rec_undo - ������ � ��������
snap - ��������� """

import k3


def rec_undo(rec_name):
    """��������� ������� ������� � ������� k3 � ������ ������� rec_name"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            k3.macromode(k3.k_undo, k3.k_start)
            func(*args, **kwargs)
            k3.macromode(k3.k_undo, k3.k_stop, rec_name)
        return wrapper
    return decorator


def snap(func):
    """��������� ������� ������� � ���� getsnap//resnap"""
    def wrapper(*args, **kwargs):
        k3.getsnap()
        func(*args, **kwargs)
        k3.resnap()
    return wrapper
