# coding=cp1251

"""Модуль для работы с глобальными переменными"""
import k3


def set_global(nam, val):
    """ Присваиваем глобальной переменной nam значение val возвращаем 1, если получилось"""
    if type(nam) == str and not len(nam) > 12:
        tempvar = k3.GlobalVar(nam)
        tempvar.value = val
        return 1
    else:
        return 0


def get_global(nam):
    """ Возвращает значение из глобальной переменной с именем nam или None, если такой переменной не было"""
    tempvar = k3.GlobalVar(nam)
    if k3.isvardef(nam) > 0:
        return tempvar.value
    else:
        return None


def get_global_list(names):
    """Получает список имён, возвращает список значений глобальных переменных в том же порядке"""
    result = []
    for name_ in names:
        result.append(get_global(name_))
    return result


def set_global_arr(name_, values_):
    """Присваиваем глобальному массиву с именем name_ значения из списка values_, возвращает количество заполненных"""
    temparr = k3.GlobalVarArray(len(values_), name_)
    for posit in range(min(len(temparr), len(values_))):
        temparr[posit].value = values_[posit]
    return min(len(temparr), len(values_))


# ------ Блок старых имён до перехода в новую конвенцию

def SetGlobal(nam, val):
    return set_global(nam, val)


def GetGlobal(nam):
    return get_global(nam)
