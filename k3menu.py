# coding=cp1251

"""������ ��� �������� ���� � �3. ���� � �3 - ������ ������ k3menu.

������ ������:

Add_Caption(caption) - ����� ��������� ����
Add_Picture(picture) - ����� ���� � ����� �������� ��� ����
Align_Text(align) - 'right' ��� 'center' ������ ������������ ������ �� ������� ���� ��� �� ������
    � ��������� ������ ����� ������������ �� ������ ����
Add_Text(text) - ��������� ������ �������������� ������ � ���� ����

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
Val_From_Subst(���) - ���������� �������� id ��� ������� ���� String 6 ��� ������ �����������
Delbyname(���) - ������� �� ���� ������� � �������� ������
Move(n1, n2) - ��������� n1-� ������� � n2
Refresh() - ������� ��������, �������� ������������� � ���� ������� ���� � �� ���������
"""

import k3


class k3menu:

    def __init__(self, caption='', picture='', align='left', text=''):
        """ ��� ������ ��������
        caption - ��������� ����
        picture - ��� ����� ��� ��������
        align - ������������ (left, right, center)
        text - ������ ������"""

        self.Add_Caption(caption)
        self.Add_Picture(picture)
        self.Align_Text(align)
        self.Add_Text(text)

        # -- ������� �� ������� ����
        self.content = {}
        # -- ������������� ������ ���. � �� ������ ������� �������
        self.names = []

    def Add_Caption(self, caption):
        """����� ��������� ���� � ����"""

        self.capt = caption

    def Add_Picture(self, picture):
        """����� ���� � ����� ��������"""

        self.pic = picture

    def Align_Text(self, align):
        """����� ������������ ������"""

        if align == 'right':
            self.kwrd = k3.k_right
        elif align == 'center':
            self.kwrd = k3.k_center
        else:
            self.kwrd = k3.k_left

    def Add_Text(self, text):
        """����� ����� � ���� ����"""

        self.text = text

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

    def Add_Simple(self, type, nam, pr, d):
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

    def Val_From_Subst(self, name):
        """��� ������� ���� string 6 ���������� ������ �������� ��������, �� ���� id ��� �����������"""
        if self.Type(name) == 'string 6':
            return self.Val(name).split('#')[1]
        else:
            return 0

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

    def Add_Real_List(self, nam='', pr='', contents=(), d=0, only=0):
        """��������� real � �������������. d - �������� ��������� ��� list ��� ������� current ��� only"""
        if not self.Can_Add(nam):
            return 0
        if len(contents) == 0:
            return 0
        self.names.append(nam)
        if only == 0:
            self.content[nam] = ['reallist', k3.Var(), d, pr, contents]
        else:
            self.content[nam] = ['reallistonly', k3.Var(), d, pr, contents]
        return 1

    def Add_String_List(self, nam='', pr='', contents=(), d=0, only=0):
        """��������� string � �������������. d - �������� ��������� ��� list ��� ������� current ��� only"""
        if not self.Can_Add(nam):
            return 0
        if len(contents) == 0:
            return 0
        self.names.append(nam)
        if only == 0:
            self.content[nam] = ['stringlist', k3.Var(), d, pr, contents]
        else:
            self.content[nam] = ['stringlistonly', k3.Var(), d, pr, contents]
        return 1

    def List(self, nam=''):
        """ ���������� ������ ��� ������������ � ������� nam """
        if not self.Is_Exist(nam):
            return []
        possible = ['reallist', 'reallistonly', 'stringlist', 'stringlistonly']
        if possible.count(self.Type(nam)) == 0:
            return []
        return self.content[nam][4]

    def Setlist(self, nam='', contents=()):
        """������������� ������� nam ������ l"""
        if not self.Is_Exist(nam):
            return 0
        possible = ['reallist', 'reallistonly', 'stringlist', 'stringlistonly']
        if possible.count(self.Type(nam)) == 0:
            return 0
        if len(contents) == 0:
            return 0
        self.content[nam][2] = contents
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
        return not self.Is_Exist(nam)

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
        contents = []
        contents.extend(self.List(nam))
        contents.insert(int(self.Def(nam)), k3.k_current)
        return contents

    def Refresh(self):
        """ ��������� ���� ���������� ������� �������� ���� �������� ������� �� only"""
        for i in range(len(self.names)):
            if not self.Type(self.names[i]) == 'button':
                if not (self.Type(self.names[i]) == 'reallistonly' or self.Type(self.names[i]) == 'stringlistonly'):
                    self.Setdef(self.names[i], self.Val(self.names[i]))
                else:
                    val = self.Val(self.names[i])
                    contents = self.List(self.names[i])
                    n = contents.index(val)
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
        Add_Text(text) - ��������� ������ ��� ������ (���� ������� ������ ��� ������) � ���� ����
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
        return int(k3.alternative(cmdpar)[0])

    def Add_Item(self, caption='', picture=''):
        """��������� ������� � ����, ���������
        caption - ������ ��������� � ������ ����
        picture - ������ ���� � �������� ������ ����"""
        self.items.append([caption, picture])

    def Check_Contents(self):
        """������� ���� ��������� � �������� � ����"""
        for item in self.items:
            print(item[0], self.picture_folder+item[1])

    def Add_Folder(self, folder=''):
        self.picture_folder = folder

    def Add_Text(self, text):
        """��������� ������ �� ������ text, ��� ��������� �������� ������ text � ������������� ����� ����"""
        if isinstance(text, str):
            self.text.append(text)
        elif isinstance(text, list) or isinstance(text, tuple):
            self.text.extend(text)


class K3Menu2:
    """����� ��� ���� �3 �������� 2.
        ������������ ������ ���� ��� ������� ��������� �������"""

    def __init__(self, caption='', picture='', align_keyword=k3.k_left):
        self.caption = caption
        self.picture = picture
        self.align_keyword = align_keyword
        self.text = ['']
        self.items = []

    def add_caption(self, caption):
        """������ ��������� ����"""
        self.caption = caption

    def add_picture(self, picture):
        """������ ���� � ����� ��������"""
        self.picture = picture

    def align(self, align):
        """������ ������������ ������ 'left', 'right' ��� 'center' """
        if align == 'center':
            self.align_keyword = k3.k_center
        elif align == 'right':
            self.align_keyword = k3.k_right
        else:
            self.align_keyword = k3.k_left

    def add_text(self, text):
        """�������� ������ ��� ��������� ����� � ������"""
        if len(self.text) == 1 and self.text[0] == '':
            self.text = []
        if isinstance(text, list or tuple):
            self.text.extend(text)
        elif isinstance(text, str):
            self.text.append(text)

    def clear_text(self):
        """�������� �����"""
        self.text = ['']

    def add_item(self, item):
        """�������� ������� (������ ��������� ������ K3MenuItem)"""
        if isinstance(item, K3MenuItem):
            self.items.append(item)

    def show(self):
        """���������� ����, ������� 1, ���� ������ Ok, ��� 0, ���� ������"""
        setvar_parameters = [self.caption, self.picture, self.align_keyword]
        setvar_parameters.extend(self.text)
        setvar_parameters.append(k3.k_done)
        for item in self.items:
            if item(type):
                setvar_parameters.extend(item.cmd_line())
        setvar_parameters.append(k3.k_done)
        res = k3.setvar(setvar_parameters)
        return res[0]

    def refresh(self):
        """���������� � ��������� ������� ������ ��� ������� ��������"""
        for item in self.items:
            item.refresh()


class K3MenuItem:
    """������������ ����� ��� ������ ���� �3"""
    types = ('real', 'real_list', 'real_list_on')

    def __init__(self):
        self.prompt = ''
        self.type = ''
        self.default = 0
        self.size = 0

    def refresh(self):
        """����������� � ��������� ������� ��������"""
        self.default = self.value()

    def value(self):
        """���������� ������� ��������"""
        pass

    def cmd_line(self):
        """���������� ����������� � ��������� ������ ��� ������ setvar"""
        pass

    def set_default(self, default):
        self.default = default

    def set_prompt(self, prompt):
        self.prompt = prompt

    def set_size(self, size):
        self.size = size


class ItemSimple(K3MenuItem):
    """������� ����� � ������ � ��������� ������ ��������"""

    def __init__(self, prompt='', default=0, size=0):
        super().__init__()
        self.set_size(size)
        self.set_default(default)
        self.set_prompt(prompt)
        self.type = ''
        self.k3var = k3.Var()
        self.k3var.value = self.default

    def value(self):
        return self.k3var.value

    def cmd_line(self):
        cmd_line = [self.type]
        if not self.type == 'logical':
            if self.size == 0:
                cmd_line.append(k3.k_auto)
            elif self.size > 0:
                cmd_line.extend([k3.k_size, int(self.size)])
        cmd_line.extend([k3.k_default, self.default])
        cmd_line.append(self.prompt)
        cmd_line.append(self.k3var)


class ItemReal(ItemSimple):
    """���� �����"""

    def __init__(self, prompt='', default=0, size=0):
        super().__init__(prompt=prompt, default=default, size=size)
        self.type = 'real'


class ItemString(ItemSimple):
    """���� ������"""

    def __init__(self, prompt='', default='', size=0):
        super().__init__(prompt=prompt, default=default, size=size)
        self.type = 'string'


class ItemLogical(ItemSimple):
    """�������"""
    def __init__(self, prompt='', default=0, size=0):
        super().__init__(prompt=prompt, default=default, size=size)
        self.type = 'logical'


# class ItemFile


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
