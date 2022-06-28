# coding=cp1251

"""������ ��� �������� ���� � �3. ���� � �3 - ������ ������ k3menu.

������ ������:

Show() - ���������� ���� � �3. ���������� 1, ���� � ���� ������ �� ��� 0, ���� ������ ������ ��� ������� ����
Add_ - ������ ��� ���������� � ���� ������� ��� �������� ������
    Real - ���� �����
    Logical - �������
    String - ���� ������
    Button - �������������� �����
    String_Code - ����������� ���� �����, �������� ����� �������� � ����������� �� �3
    Real_List - ���� ����� � ������� �� ������. only = true �� ��� ������ ��� ��������
    String_List - ���� ������ � ������� �� ������. only = true �� ��� ������ ��� ��������
Val(���) - ���������� �������� �� ������� ���� � �������� ������.
    ���������� ��������, ��������� � ����, ���� ���� ������������ � ��� ������ ��
    ���������� ���������, ���� ���� ��� �� ������������
Delbyname(���) - ������� �� ���� ������� � �������� ������
Move(n1, n2) - ��������� n1-� ������� � n2
Refresh() - ������� ��������, �������� ������������� � ���� ������� ���� � �� ���������
"""

import k3


class k3menu:

    def __init__(self, capt='', pic='', kwrd='left', text=''):
        """ ��� ������ ��������
        capt - ��������� ����
        pic - ��� ����� ��� ��������
        kwrd - �������� ����� ��� ������������ (left, right, center)
        text - ������ ������"""

        # -- �������� �������
        self.capt = capt  # ��������� ����
        self.pic = pic  # ���� ��������

        if kwrd == 'center':
            self.kwrd = k3.k_center
        elif kwrd == 'right':
            self.kwrd = k3.k_right
        else:
            self.kwrd = k3.k_left

        self.text = text  # ����� � ����

        # -- ������� �� ������� ����
        self.content = {}

        # -- ������������� ������ ���. � �� ������ ������� �������
        self.names = []

    def Show(self):
        """ ��� ������ ���������� ���� � k3 � ��� ������� Ok ��������� ������� ������������"""
        param = []  # ��, ��� �� ������� � setvar

        # -- ��������� ������ ��� ����������
        param.extend([self.capt, self.pic, self.kwrd, self.text, k3.k_done])

        # -- ����� �� ������ self.names � ��������� ������ � param � ����������� �� ����

        for i in range(len(self.names)):
            currname = self.names[i]
            if self.Type(currname) == 'real':
                # -- ���������� ��� ���� real
                param.extend([k3.k_real, k3.k_auto, k3.k_default, self.Def(currname)])

            if self.Type(currname) == 'reallist':
                # -- ���������� ��� ���� reallist
                param.extend([k3.k_real, k3.k_auto, k3.k_default, self.Def(currname), k3.k_list])
                param.extend(self.List(currname))
                param.append(k3.k_done)

            if self.Type(currname) == 'reallistonly':
                # -- ���������� ��� ���� reallistonly
                param.extend([k3.k_real, k3.k_auto, k3.k_listonly])
                param.extend(self.Put_Curr(currname))
                param.append(k3.k_done)

            if self.Type(currname) == 'string':
                # -- ���������� ��� ���� string
                param.extend([k3.k_string, k3.k_auto, k3.k_default, self.Def(currname)])

            if self.Type(currname).startswith('string') and len(self.Type(currname)) == 8:
                # -- ���������� ��� string � �����
                param.extend([k3.k_string, k3.k_button, int(self.Type(currname)[-1]), k3.k_default, self.Def(currname)])

            if self.Type(currname) == 'stringlist':
                # -- ���������� ��� ���� stringlist
                param.extend([k3.k_string, k3.k_auto, k3.k_default, self.Def(currname), k3.k_list])
                param.extend(self.List(currname))
                param.append(k3.k_done)

            if self.Type(currname) == 'stringlistonly':
                # -- ���������� ��� ���� stringlistonly
                param.extend([k3.k_string, k3.k_auto, k3.k_listonly])
                param.extend(self.Put_Curr(currname))
                param.append(k3.k_done)

            if self.Type(currname) == 'logical':
                # -- ���������� ��� ���� logical
                param.extend([k3.k_logical, k3.k_default, self.Def(currname)])

            if self.Type(currname) == 'button':
                # -- ���������� ��� ���� button
                param.append(k3.k_button)

            param.extend([self.Prompt(currname), self.content[self.names[i]][1]])

        param.append(k3.k_done)

        res = k3.setvar(param)
        return int(res[0])

    def Add_Real(self, nam='', pr='', d=0):
        """ ��������� ������� � ���������� real ������ nam, ���������� pr � ���������� d """
        return self.Add_Simple('real', nam, pr, d)

    def Add_Logical(self, nam='', pr='', d=0):
        return self.Add_Simple('logical', nam, pr, d)

    def Add_String(self, nam='', pr='', d=''):
        """ ��������� ������� � ���������� string """
        return self.Add_Simple('string', nam, pr, d)

    def Add_Button(self, nam=''):
        """ ��������� �������������� ����� """
        return self.Add_Simple('button', nam, '  ', 0)

    def Add_Simple(self, type, nam='', pr='', d=''):
        if not self.Can_Add(nam):
            return 0
        self.names.append(nam)
        self.content[nam] = [type, k3.Var(), d, pr]
        self.Setdef(nam, d)
        return 1

    def Add_String_Code(self, nam='', pr='', d='', cod=0):
        """��������� ����������� string � ��������. � cod �������� ���"""
        if not self.Can_Add(nam):
            return 0
        self.names.append(nam)
        if (cod > 0) and (cod < 8):
            self.content[nam] = ['string ' + str(int(cod)), k3.Var(), d, pr]
            self.Setdef(nam, d)
        elif cod == 8:
            # ������ ���������� ������ ��� ��������
            self.content[nam] = ['string 8', k3.VarArray(100), d, pr]
        else:
            return 0
        return 1

    def Delbyname(self, nam):
        """ ������� ������� � ������ nam """
        if not self.Is_Exist(nam):
            return 0
        self.names.remove(nam)
        self.content.pop(nam)
        return 1

    def Prompt(self, nam):
        """ ���������� ��������� � ������� nam """
        if not self.Is_Exist(nam):
            return ''
        return self.content[nam][3]

    def Type(self, nam):
        """ ���������� ��� � ������� nam """
        if not self.Is_Exist(nam):
            return ''
        return self.content[nam][0]

    def Def(self, nam):
        """ ���������� ��������� � ������� nam. ���� ��� only, �� ������� ����� � current"""
        if not self.Is_Exist(nam):
            return 0
        return self.content[nam][2]

    def Val(self, nam):
        """ ���������� �������� � ������� nam.
        ���� ���� �� �����������, ���������� ��������� ���� ����� ���, ���������� 0 """
        if not self.Is_Exist(nam):
            return 0
        return self.content[nam][1].value

    def Move(self, n1=0, n2=0):
        """��������� ����� n1 � ������� n2"""
        if n1 >= len(self.names) or n2 >= len(self.names):
            return 0
        if n1 == n2:
            return 0
        nam = self.names.pop(n1)
        self.names.insert(n2, nam)
        return 1

    def Num(self, nam=''):
        """ ���������� ����� ������� � ������ nam. ���� ����� ������� ���, ���������� ����� ��������� �������"""
        if not self.Is_Exist(nam):
            return len(self.names) - 1
        return self.names.index(nam)

    def Nam(self, n=0):
        """���������� ��� � ������� � ������� n"""
        if n >= len(self.names):
            return ''
        return self.names[n]

    def Add_Real_List(self, nam='', pr='', l=(), d=0, only=0):
        """��������� real � �������������. d - �������� ��������� ��� list ��� ������� current ��� only"""
        if not self.Can_Add(nam):
            return 0
        if len(l) == 0:
            return 0
        self.names.append(nam)
        if only == 0:
            self.content[nam] = ['reallist', k3.Var(), d, pr, l]
        else:
            self.content[nam] = ['reallistonly', k3.Var(), d, pr, l]
        return 1

    def Add_String_List(self, nam='', pr='', l=(), d=0, only=0):
        """��������� string � �������������. d - �������� ��������� ��� list ��� ������� current ��� only"""
        if not self.Can_Add(nam):
            return 0
        if len(l) == 0:
            return 0
        self.names.append(nam)
        if only == 0:
            self.content[nam] = ['stringlist', k3.Var(), d, pr, l]
        else:
            self.content[nam] = ['stringlistonly', k3.Var(), d, pr, l]
        return 1

    def List(self, nam=''):
        """ ���������� ������ ��� ������������ � ������� nam """
        if not self.Is_Exist(nam):
            return []
        possible = ['reallist', 'reallistonly', 'stringlist', 'stringlistonly']
        if possible.count(self.Type(nam)) == 0:
            return []
        return self.content[nam][4]

    def Setlist(self, nam='', l=()):
        """������������� ������� nam ������ l"""
        if not self.Is_Exist(nam):
            return 0
        possible = ['reallist', 'reallistonly', 'stringlist', 'stringlistonly']
        if possible.count(self.Type(nam)) == 0:
            return 0
        if len(l) == 0:
            return 0
        self.content[nam][2] = l
        return 1

    def Is_Exist(self, nam=''):
        """���������� 1, ���� ������� ���������� � 0, ���� nam ������ ��� ������� ���"""
        if nam == '':
            return 0
        if self.names.count(nam) == 0:
            return 0
        return 1

    def Can_Add(self, nam=''):
        """���������� 1, ���� ������� ����� �������� � 0, ���� nam ������ ��� ����� ������� ����"""
        if nam == '':
            return 0
        if self.names.count(nam) > 0:
            return 0
        return 1

    def Curr(self, nam=''):
        """���������� �������� �������� �������� ������ ��� listonly"""
        if not self.Is_Exist(nam):
            return 0
        possible = ['reallistonly', 'stringlistonly']
        if possible.count(self.Type(nam)) == 0:
            return 0
        return self.List(nam)[self.Def(nam)]

    def Put_Curr(self, nam=''):
        """���������� ������ ��� listonly �� ����������� � ������ ����� k3.k_current"""
        if not self.Is_Exist(nam):
            return []
        possible = ['reallistonly', 'stringlistonly']
        if possible.count(self.Type(nam)) == 0:
            return []
        l = []
        l.extend(self.List(nam))
        l.insert(int(self.Def(nam)), k3.k_current)
        return l

    def Refresh(self):
        """ ��������� ���� ���������� ������� �������� ���� �������� ������� �� only"""
        for i in range(len(self.names)):
            if not self.Type(self.names[i]) == 'button':
                if not (self.Type(self.names[i]) == 'reallistonly' or self.Type(self.names[i]) == 'stringlistonly'):
                    self.Setdef(self.names[i], self.Val(self.names[i]))
                else:
                    val = self.Val(self.names[i])
                    l = self.List(self.names[i])
                    n = l.index(val)
                    self.Setdef(self.names[i], n)

    def Setdef(self, nam, d):
        """ ������������� ������� nam ��������� d
        ���� ��� only, �� �� �������� �����, � � ���������� ����� �������� �������� �� ������"""
        if not self.Is_Exist(nam):
            return 0
        self.content[nam][2] = d
        if not (self.Type(nam) == 'reallistonly' or self.Type(nam) == 'stringlistonly'):
            self.content[nam][1].value = d
        else:
            self.content[nam][1].value = self.List(nam)[d]
        return 1


class k3picbox:
    """����� ��� ���� �� ��������
    ������ ������:
        Add_Item(caption, picture) - ��������� ����� ����
        Add_Folder(folder) - ��������� ���� � ������ � ���������. ��� �������� ����� �������� � ���� �����
        Check_Contents() - ������� � ������� ���� caption, picture. �������� � ������ �������� �����
        Show() - ������� ���� � �3 � ���������� ����� ���������� ������ ��� 0, ���� ������ ������ ��� �� ������ ������
        """

    def __init__(self, caption='', default=1, text_pos='left'):
        self.caption = caption
        self.default = default
        self.text = []
        self.text_pos = k3.k_left
        if text_pos == 'center':
            self.text_pos = k3.k_center
        elif text_pos == 'right':
            self.text_pos = k3.k_right
        self.picture_folder = ''
        self.items = []

    def Show(self):
        """������� ����, ���������� ����� ���������� ������ ��� 0, ���� ������ ������"""
        if len(self.items) == 0:
            return 0
        cmdpar = [self.caption, k3.k_picbox, k3.k_default, self.default]
        if len(self.text) > 0:
            cmdpar.append(k3.k_text)
            cmdpar.append(self.text_pos)
            cmdpar.extend(self.text)
            cmdpar.append(k3.k_done)
        for item in self.items:
            caption = item[0]
            picture = self.picture_folder+item[1]
            cmdpar.append(caption)
            cmdpar.append(picture)
        cmdpar.append(k3.k_done)
        return k3.alternative(cmdpar)

    def Add_Item(self, caption='', picture=''):
        """��������� ������� � ����, ���������
        caption - ������ ��������� � ������ ����
        picture - ������ ���� � �������� ������ ����"""
        self.items.append(caption)
        self.items.append(picture)

    def Check_Contents(self):
        """������� ���� ��������� � �������� � ����"""
        for item in self.items:
            print(item[0], self.picture_folder+item[1])

    def Add_Folder(self, folder=''):
        self.picture_folder = folder


if __name__ == '__main__':
    men = k3menu('� ������', '', k3.k_left, '� �������')
    men.Add_Real('real1', '������ �����', 100)
    men.Add_Real('real2', '������ �����', 200)
    men.Add_Button('butt')
    men.Add_String('str1', '� ������', '� ������')
    men.Add_Logical('log1', '� �������', 0)
    men.Add_Button('butt2')
    men.Add_Real_List('list1', '� ������ �����', [1, 2, 3, 4, 5], 3, 0)
    men.Add_Real_List('list2', '� ������������ ������ �����', [10, 20, 30, 40], 1, 1)
    men.Add_String_List('list3', '� ������ ������ �����', ['������', '�������', '������', '������'], '������', 0)
    men.Add_String_List('list4', '� �������� ������ �����', ['������', '��� ������', '����', '���������'], 2, 1)
    men.Show()
    men.Refresh()
    men.Show()
