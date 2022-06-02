# k3DevKit
English
---
Package of some Python modules useful in pythoning K3 software

*For K3 software compatibility all files are in cyrillic cp1251 so GitHub site can not show them correctly*
## Contents

### k3menu module
Provides k3menu class for creating menus in K3. Pythonizing of 'setvar' K3 function
An instance of this class counts as single menu. You are able to add positions to it using '.Add_' methods, 
show it using '.Show()' and collect user data with '.Val'

### k3global module
Provides connections to K3 global variables. Main functions are:
set_global(name, value) and get_global(name)

### k3utils module
Provides various useful functions
check_furntype(object, target) checking if object is of target kind via furntype attribute
msgwin creates simple window with user defined caption, text and text on single button
current_folder() returns full path to folder containing current opend file

Русский
---
Набор различных модулей, полезных при написании макросов К3 на python

*Для совместимости с К3 все файлы сохранены в кодировке cp1251, поэтому GitHub имеет проблемы с их отображением*
## Содержание

### Модуль k3menu
Объявляет класс k3meny для создания пользовательских меню в К3. Представляет собой оболочку для функции К3 setvar.
Экземпляр этого класса содержит одно меню. С помощью методов класса '.Add_' в меню добавляются позиции, метод '.Show()' отображает меню и даёт пользователю ввести данные, введённые данные можно получить методом '.Val'

### Модуль k3global
Позволяет работать с глобальными перемнными К3. Основные функции:
set_global(name, value) и get_global(name)

### Модуль k3utils
Содержит различные полезные функции
check_furntype(object, target) проверяет, относится ли объект к типу target, по значению его атрибута furntype
msgwin создаёт простое окно с заголовком, текстом и подписью кнопки для закрытия
errwin создаёт окошко с заголовком "Ошибка" и кнопкой "Ок"
current_folder() возвращает полный путь к папке, в которой находится текущий открытый файл
