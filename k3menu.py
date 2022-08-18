# coding=cp1251

"""Модуль для создания меню в К3. Меню в К3 - объект класса k3menu.

Методы класса:

Add_Caption(caption) - Задаёт заголовок меню
Add_Picture(picture) - Задаёт путь к файлу картинки для меню
Align_Text(align) - 'right' или 'center' задают выравнивание текста по правому краю или по центру
    В противном случае будет выравнивание по левому краю
Add_Text(text) - добавляет строку пояснительного текста в окно меню

Show() - Отображает меню в К3. Возвращает 1, если в меню нажали Ок или 0, если нажали Отмена или закрыли меню
Add_ - методы для добавления в меню строчек для внесения данных
    Real - ввод числа
    Logical - чекбокс
    String - ввод строки
    Button - разделительная линия
    String_Code - специальный ввод строк, значения кодов смотрите в руководстве по К3
    Real_List - ввод числа с выбором из списка. only = true не даёт ввести своё значение
    String_List - ввод строки с выбором из списка. only = true не даёт ввести своё значение
Val(имя) - возвращает значение из позиции меню с заданным именем.
    Возвращает значение, введённное в меню, если меню отображалось и там нажали Ок
    Возвращает умолчания, если меню ещё не отображалось
Val_From_Subst(имя) - возвращает значение id для позиций типа String 6 без номера подстановки
Delbyname(имя) - удаляет из меню позицию с заданным именем
Move(n1, n2) - Переносит n1-ю позицию в n2
Refresh() - Заносит значения, введённые пользователем у всех позиций меню в их умолчания
"""

import k3


class k3menu:

    def __init__(self, caption='', picture='', align='left', text=''):
        """ При вызове получаем
        caption - заголовок окна
        picture - имя файла для картинки
        align - выравнивание (left, right, center)
        text - строка текста"""

        self.Add_Caption(caption)
        self.Add_Picture(picture)
        self.Align_Text(align)
        self.Add_Text(text)

        # -- Словарь из позиций меню
        self.content = {}
        # -- Упорядоченный список имён. В нём держим порядок позиций
        self.names = []

    def Add_Caption(self, caption):
        """Задаёт заголовок окна с меню"""

        self.capt = caption

    def Add_Picture(self, picture):
        """Задаёт путь к файлу картинки"""

        self.pic = picture

    def Align_Text(self, align):
        """Задаёт выравнивание текста"""

        if align == 'right':
            self.kwrd = k3.k_right
        elif align == 'center':
            self.kwrd = k3.k_center
        else:
            self.kwrd = k3.k_left

    def Add_Text(self, text):
        """Задаёт текст в окне меню"""

        self.text = text

    def Show(self):
        """ При вызове отображает меню в k3 и при нажатии Ok заполняет словарь результатами"""
        param = []  # То, что мы положим в setvar

        # -- Добавляем строки для заголовков
        param.extend([self.capt, self.pic, self.kwrd, self.text, k3.k_done])

        # -- Бежим по списку self.names и добавляем строки в param в зависимости от типа

        for i in range(len(self.names)):
            currname = self.names[i]
            if self.Type(currname) == 'real':
                # -- Заполнение для типа real
                param.extend([k3.k_real, k3.k_auto, k3.k_default, self.Def(currname)])

            if self.Type(currname) == 'reallist':
                # -- Заполнение для типа reallist
                param.extend([k3.k_real, k3.k_auto, k3.k_default, self.Def(currname), k3.k_list])
                param.extend(self.List(currname))
                param.append(k3.k_done)

            if self.Type(currname) == 'reallistonly':
                # -- Заполнение для типа reallistonly
                param.extend([k3.k_real, k3.k_auto, k3.k_listonly])
                param.extend(self.Put_Curr(currname))
                param.append(k3.k_done)

            if self.Type(currname) == 'string':
                # -- Заполнение для типа string
                param.extend([k3.k_string, k3.k_auto, k3.k_default, self.Def(currname)])

            if self.Type(currname).startswith('string') and len(self.Type(currname)) == 8:
                # -- Заполнение для string с типом
                param.extend([k3.k_string, k3.k_button, int(self.Type(currname)[-1]), k3.k_default, self.Def(currname)])

            if self.Type(currname) == 'stringlist':
                # -- Заполнение для типа stringlist
                param.extend([k3.k_string, k3.k_auto, k3.k_default, self.Def(currname), k3.k_list])
                param.extend(self.List(currname))
                param.append(k3.k_done)

            if self.Type(currname) == 'stringlistonly':
                # -- Заполнение для типа stringlistonly
                param.extend([k3.k_string, k3.k_auto, k3.k_listonly])
                param.extend(self.Put_Curr(currname))
                param.append(k3.k_done)

            if self.Type(currname) == 'logical':
                # -- Заполнение для типа logical
                param.extend([k3.k_logical, k3.k_default, self.Def(currname)])

            if self.Type(currname) == 'button':
                # -- Заполнение для типа button
                param.append(k3.k_button)

            param.extend([self.Prompt(currname), self.content[self.names[i]][1]])

        param.append(k3.k_done)

        res = k3.setvar(param)
        return int(res[0])

    def Add_Real(self, nam='', pr='', d=0):
        """ Добавляет позицию с переменной real именем nam, подсказкой pr и умолчанием d """
        return self.Add_Simple('real', nam, pr, d)

    def Add_Logical(self, nam='', pr='', d=0):
        return self.Add_Simple('logical', nam, pr, d)

    def Add_String(self, nam='', pr='', d=''):
        """ Добавляет позицию с переменной string """
        return self.Add_Simple('string', nam, pr, d)

    def Add_Button(self, nam=''):
        """ Добавляет разделительную линию """
        return self.Add_Simple('button', nam, '  ', 0)

    def Add_Simple(self, type, nam, pr, d):
        if not self.Can_Add(nam):
            return 0
        self.names.append(nam)
        self.content[nam] = [type, k3.Var(), d, pr]
        self.Setdef(nam, d)
        return 1

    def Add_String_Code(self, nam='', pr='', d='', cod=0):
        """Обработка специальных string с номерами. в cod хранится код"""
        if not self.Can_Add(nam):
            return 0
        self.names.append(nam)
        if (cod > 0) and (cod < 8):
            self.content[nam] = ['string ' + str(int(cod)), k3.Var(), d, pr]
            self.Setdef(nam, d)
        elif cod == 8:
            # Запрос нескольких файлов для открытия
            self.content[nam] = ['string 8', k3.VarArray(100), d, pr]
        else:
            return 0
        return 1

    def Delbyname(self, nam):
        """ Удаляет позицию с именем nam """
        if not self.Is_Exist(nam):
            return 0
        self.names.remove(nam)
        self.content.pop(nam)
        return 1

    def Prompt(self, nam):
        """ Возвращает подсказку у позиции nam """
        if not self.Is_Exist(nam):
            return ''
        return self.content[nam][3]

    def Type(self, nam):
        """ Возвращает тип у позиции nam """
        if not self.Is_Exist(nam):
            return ''
        return self.content[nam][0]

    def Def(self, nam):
        """ Возвращает умолчание у позиции nam. Если тип only, то вернётся номер у current"""
        if not self.Is_Exist(nam):
            return 0
        return self.content[nam][2]

    def Val(self, nam):
        """ Возвращает значение у позиции nam.
        Если меню не запускалось, возвращает умолчание если имени нет, возвращает 0 """
        if not self.Is_Exist(nam):
            return 0
        return self.content[nam][1].value

    def Val_From_Subst(self, name):
        """Для позиций типа string 6 возвращает вторую половину значение, то есть id без подстановки"""
        if self.Type(name) == 'string 6':
            return self.Val(name).split('#')[1]
        else:
            return 0

    def Move(self, n1=0, n2=0):
        """Переносит номер n1 в позицию n2"""
        if n1 >= len(self.names) or n2 >= len(self.names):
            return 0
        if n1 == n2:
            return 0
        nam = self.names.pop(n1)
        self.names.insert(n2, nam)
        return 1

    def Num(self, nam=''):
        """ Возвращает номер позиции с именем nam. Если такой позиции нет, возвращает номер последней позиции"""
        if not self.Is_Exist(nam):
            return len(self.names) - 1
        return self.names.index(nam)

    def Nam(self, n=0):
        """Возвращает имя у позиции с номером n"""
        if n >= len(self.names):
            return ''
        return self.names[n]

    def Add_Real_List(self, nam='', pr='', contents=(), d=0, only=0):
        """Добавляет real с перечислением. d - значение умолчания для list или позиция current для only"""
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
        """Добавляет string с перечислением. d - значение умолчания для list или позиция current для only"""
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
        """ Возвращает список для перечисления у позиции nam """
        if not self.Is_Exist(nam):
            return []
        possible = ['reallist', 'reallistonly', 'stringlist', 'stringlistonly']
        if possible.count(self.Type(nam)) == 0:
            return []
        return self.content[nam][4]

    def Setlist(self, nam='', contents=()):
        """устанавливает позиции nam список l"""
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
        """Возвращает 1, если позиция существует и 0, если nam пустое или позиции нет"""
        if nam == '':
            return 0
        if self.names.count(nam) == 0:
            return 0
        return 1

    def Can_Add(self, nam=''):
        """Возвращает 1, если позицию можно добавить и 0, если nam пустое или такая позиция есть"""
        if nam == '':
            return 0
        return not self.Is_Exist(nam)

    def Curr(self, nam=''):
        """Возвращает значение текущего элемента списка для listonly"""
        if not self.Is_Exist(nam):
            return 0
        possible = ['reallistonly', 'stringlistonly']
        if possible.count(self.Type(nam)) == 0:
            return 0
        return self.List(nam)[self.Def(nam)]

    def Put_Curr(self, nam=''):
        """Возвращает список для listonly со встевленным в нужное место k3.k_current"""
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
        """ Назначает всем умолчаниям текущие значение Надо добавить реакцию на only"""
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
        """ Устанавливает позиции nam умолчание d
        Если тип only, то мы получаем номер, а в переменную нужно положить значение из списка"""
        if not self.Is_Exist(nam):
            return 0
        self.content[nam][2] = d
        if not (self.Type(nam) == 'reallistonly' or self.Type(nam) == 'stringlistonly'):
            self.content[nam][1].value = d
        else:
            self.content[nam][1].value = self.List(nam)[d]
        return 1


class k3picbox:
    """Класс для меню из картинок
    Методы класса:
        Add_Item(caption, picture) - Добавляет пункт меню
        Add_Folder(folder) - Добавляет путь к папкам с картнками. Все картинки будут искаться в этой папке
        Add_Text(text) - Добавляет строку или строки (если передан список или кортеж) в окно меню
        Check_Contents() - Выводит в консоль пары caption, picture. Картинки с учётом заданной папки
        Show() - Выводит меню в К3 и возвращает номер выбранного пункта или 0, если нажата отмена или не заданы пункты
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
        """Выводит меню, возвращает номер выбранного пункта или 0, если нажата Отмена"""
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
        """Добавляет позицию в меню, принимает
        caption - строка подсказки к пункту меню
        picture - полный путь к картинке пункта меню"""
        self.items.append([caption, picture])

    def Check_Contents(self):
        """Выводит пары подсказок и картинок в меню"""
        for item in self.items:
            print(item[0], self.picture_folder+item[1])

    def Add_Folder(self, folder=''):
        self.picture_folder = folder

    def Add_Text(self, text):
        """Добавляет строку из строки text, или построчно элементы списка text в пояснительный текст меню"""
        if isinstance(text, str):
            self.text.append(text)
        elif isinstance(text, list) or isinstance(text, tuple):
            self.text.extend(text)


class K3Menu2:
    """Класс для меню К3 редакция 2.
        Предполагает пункты меню как объекты отдельных классов"""

    def __init__(self, caption='', picture='', align_keyword=k3.k_left):
        self.caption = caption
        self.picture = picture
        self.align_keyword = align_keyword
        self.text = ['']
        self.items = []

    def add_caption(self, caption):
        """Задать заголовок окна"""
        self.caption = caption

    def add_picture(self, picture):
        """Задать путь к файлу картинки"""
        self.picture = picture

    def align(self, align):
        """Задать выравнивание текста 'left', 'right' или 'center' """
        if align == 'center':
            self.align_keyword = k3.k_center
        elif align == 'right':
            self.align_keyword = k3.k_right
        else:
            self.align_keyword = k3.k_left

    def add_text(self, text):
        """Добавить строку или множество строк к тексту"""
        if len(self.text) == 1 and self.text[0] == '':
            self.text = []
        if isinstance(text, list or tuple):
            self.text.extend(text)
        elif isinstance(text, str):
            self.text.append(text)

    def clear_text(self):
        """Очистить текст"""
        self.text = ['']

    def add_item(self, item):
        """Добавить позицию (объект подкласса класса K3MenuItem)"""
        if isinstance(item, K3MenuItem):
            self.items.append(item)

    def show(self):
        """Отобразить меню, вернуть 1, если нажато Ok, или 0, если Отмена"""
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
        """Подставить в умолчание каждому пункту его текущее значение"""
        for item in self.items:
            item.refresh()


class K3MenuItem:
    """Родительский класс для пункта меню К3"""
    types = ('real', 'real_list', 'real_list_on')

    def __init__(self):
        self.prompt = ''
        self.type = ''
        self.default = 0
        self.size = 0

    def refresh(self):
        """Подставляет в умолчание текущее значение"""
        self.default = self.value()

    def value(self):
        """Возвращает текущее значение"""
        pass

    def cmd_line(self):
        """Возвращает подстановку в командную строку для вызова setvar"""
        pass

    def set_default(self, default):
        self.default = default

    def set_prompt(self, prompt):
        self.prompt = prompt

    def set_size(self, size):
        self.size = size


class ItemSimple(K3MenuItem):
    """Простые вводы в строку с возвратом одного значения"""

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
    """Ввод числа"""

    def __init__(self, prompt='', default=0, size=0):
        super().__init__(prompt=prompt, default=default, size=size)
        self.type = 'real'


class ItemString(ItemSimple):
    """Ввод Строки"""

    def __init__(self, prompt='', default='', size=0):
        super().__init__(prompt=prompt, default=default, size=size)
        self.type = 'string'


class ItemLogical(ItemSimple):
    """Чекбокс"""
    def __init__(self, prompt='', default=0, size=0):
        super().__init__(prompt=prompt, default=default, size=size)
        self.type = 'logical'


# class ItemFile


if __name__ == '__main__':
    men = k3menu('Я окошко', '', k3.k_left, 'Я менюшко')
    men.Add_Real('real1', 'Первое число', 100)
    men.Add_Real('real2', 'Второе число', 200)
    men.Add_Button('butt')
    men.Add_String('str1', 'Я строка', 'Я строка')
    men.Add_Logical('log1', 'Я галочка', 0)
    men.Add_Button('butt2')
    men.Add_Real_List('list1', 'Я список чисел', [1, 2, 3, 4, 5], 3, 0)
    men.Add_Real_List('list2', 'Я тоталитарный список чисел', [10, 20, 30, 40], 1, 1)
    men.Add_String_List('list3', 'Я добрый список строк', ['Улыбка', 'Веселье', 'Солнце', 'Мячики'], 'Облака', 0)
    men.Add_String_List('list4', 'Я грустный список строк', ['Работа', 'Ещё работа', 'Тучи', 'Будильник'], 2, 1)
    men.Show()
    men.Refresh()
    men.Show()
