# coding=cp1251

"""������ ��� ������ � ����������� �����������"""
import k3


def set_global(nam, val):
    """ ����������� ���������� ���������� nam �������� val ���������� 1, ���� ����������"""
    if type(nam) == str and not len(nam) > 12:
        tempvar = k3.GlobalVar(nam)
        tempvar.value = val
        return 1
    else:
        return 0


def get_global(nam):
    """ ���������� �������� �� ���������� ���������� � ������ nam ��� None, ���� ����� ���������� �� ����"""
    tempvar = k3.GlobalVar(nam)
    if k3.isvardef(nam) > 0:
        return tempvar.value
    else:
        return None


def get_global_list(names):
    """�������� ������ ���, ���������� ������ �������� ���������� ���������� � ��� �� �������"""
    result = []
    for name_ in names:
        result.append(get_global(name_))
    return result


def set_global_arr(name_, values_):
    """����������� ����������� ������� � ������ name_ �������� �� ������ values_, ���������� ���������� �����������"""
    temparr = k3.GlobalVarArray(len(values_), name_)
    for posit in range(min(len(temparr), len(values_))):
        temparr[posit].value = values_[posit]
    return min(len(temparr), len(values_))


# ------ ���� ������ ��� �� �������� � ����� ���������

def SetGlobal(nam, val):
    return set_global(nam, val)


def GetGlobal(nam):
    return get_global(nam)
