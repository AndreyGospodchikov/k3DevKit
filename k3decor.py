# coding=cp1251

"""Модуль с декораторами для k3

rec_undo - Работа с откаткой
snap - Выделение """

import k3


def rec_undo(rec_name):
    """Декоратор завернёт функцию в откатку k3 с именем команды rec_name"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            k3.macromode(k3.k_undo, k3.k_start)
            func(*args, **kwargs)
            k3.macromode(k3.k_undo, k3.k_stop, rec_name)
        return wrapper
    return decorator


def snap(func):
    """Декоратор завернёт функцию в пару getsnap//resnap"""
    def wrapper(*args, **kwargs):
        k3.getsnap()
        func(*args, **kwargs)
        k3.resnap()
    return wrapper
