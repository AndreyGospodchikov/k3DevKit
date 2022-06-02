# coding=cp1251

# --- Здесь будет класс меню для setvar

# --- Объект держит в себе заголовок, картинку, ключ и текст для окна и словарь для переменных.

# --- Структура словаря - имя: ["Тип", k3.Var, умолчание, "Подсказка"]

# --- Работа со списками: Типы reallist, reallistonly, stringlist, stringlistonly. Пятым элементом в списке стоит [] для списка. 
# --- Если тип list, умолчание - это значение. Если тип listonly, умолчание - это номер сurrent
# --- Наружу выходит только чистый список, без k3.k_current. Задание текущего через отдельный метод, иначе застрелимся.

# --- Пока не работаем с дополнительными кнопками 7 и 8

import k3

class k3menu:

	def __init__(self, capt='', pic='', kwrd='left', text=''):
		''' При вызове получаем заголовок окна, имя файла для картинки, ключевое слово для выравнивания и одну строку для текста'''

		# -- Свойства объекта
		self.capt=capt	# Заголовок окна
		self.pic=pic	# Файл картинки
		
		if kwrd=='center':
			self.kwrd=k3,k_center
		elif kwrd=='right':
			self.kwrd=k3.k_right
		else:
			self.kwrd=k3.k_left
		
		self.text=text	# Текст в окне

		# -- Словарь из позиций меню
		self.content={}

		# -- Упорядоченный список имён. В нём держим порядок позиций
		self.names=[]

	def Show(self):
		''' При вызове отображает меню в k3 и при нажатии Ok заполняет словарь результатами'''
		param=[]					# То, что мы положим в setvar

		# -- Добавляем строки для заголовков
		param.extend([self.capt, self.pic, self.kwrd, self.text, k3.k_done])

		# -- Бежим по списку self.names и добавляем строки в param в зависимости от типа

		for i in range(len(self.names)):
			currname=self.names[i]
			if self.Type(currname)=='real':
				# -- Заполнение для типа real
				param.extend([k3.k_real, k3.k_auto, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='reallist':
				# -- Заполнение для типа reallist
				param.extend([k3.k_real, k3.k_auto, k3.k_default, self.Def(currname), k3.k_list])
				param.extend(self.List(currname))
				param.append(k3.k_done)

			if self.Type(currname)=='reallistonly':
				# -- Заполнение для типа reallistonly
				param.extend([k3.k_real, k3.k_auto, k3.k_listonly])
				param.extend(self.Put_Curr(currname))
				param.append(k3.k_done)

			if self.Type(currname)=='string':
				# -- Заполнение для типа string
				param.extend([k3.k_string, k3.k_auto, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 1':
				# -- Заполнение для типа string
				param.extend([k3.k_string, k3.k_button, 1, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 2':
				# -- Заполнение для типа string
				param.extend([k3.k_string, k3.k_button, 2, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 3':
				# -- Заполнение для типа string
				param.extend([k3.k_string, k3.k_button, 3, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 4':
				# -- Заполнение для типа string
				param.extend([k3.k_string, k3.k_button, 4, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 5':
				# -- Заполнение для типа string
				param.extend([k3.k_string, k3.k_button, 5, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 6':
				# -- Заполнение для типа string
				param.extend([k3.k_string, k3.k_button, 6, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 7':
				# -- Заполнение для типа string
				param.extend([k3.k_string, k3.k_button, 7, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 8':
				# -- Заполнение для типа string
				param.extend([k3.k_string, k3.k_button, 8, k3.k_default, self.Def(currname)])


			
			if self.Type(currname)=='stringlist':
				# -- Заполнение для типа stringlist
				param.extend([k3.k_string, k3.k_auto, k3.k_default, self.Def(currname), k3.k_list])
				param.extend(self.List(currname))
				param.append(k3.k_done)

			if self.Type(currname)=='stringlistonly':
				# -- Заполнение для типа stringlistonly
				param.extend([k3.k_string, k3.k_auto, k3.k_listonly])
				param.extend(self.Put_Curr(currname))
				param.append(k3.k_done)

			if self.Type(currname)=='logical':
				# -- Заполнение для типа logical
				param.extend([k3.k_logical, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='button':
				# -- Заполнение для типа button
				param.append(k3.k_button)

			param.extend([self.Prompt(currname), self.content[self.names[i]][1]])
		
		param.append(k3.k_done)


		res=k3.setvar(param)
		return int(res[0])

	def Add_Real(self, nam='', pr='', d=0):
		''' Добавляет позицию с переменной real именем nam, подсказкой pr и умолчанием d '''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		self.content[nam]=['real', k3.Var(), d, pr]
		self.Setdef(nam, d)
		return 1
	

	def Add_Logical(self, nam='', pr='', d=0):
		''' Добавляет позицию с переменной logical '''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		self.content[nam]=['logical', k3.Var(), d, pr]
		self.Setdef(nam, d)
		return 1

	def Add_String(self, nam='', pr='', d=''):
		''' Добавляет позицию с переменной string '''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		self.content[nam]=['string', k3.Var(), d, pr]
		self.Setdef(nam, d)
		return 1

	def Add_Button(self, nam=''):
		''' Добавляет разделительную линию '''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		self.content[nam]=['button', k3.Var(), 0, '  ']
		self.Setdef(nam, 0)
		return 1

	def Add_String_Code(self, nam='', pr='', d='', cod=0):
		'''Обработка специальных string с номерами. в cod хранится код'''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		if (cod>0) and (cod<8):
			self.content[nam]=['string '+str(int(cod)), k3.Var(), d, pr]
			self.Setdef(nam, d)

		elif cod==8:
			# Запрос нескольких файлов для открытия
			self.content[nam]=['string 8', k3.VarArray(100), d, pr]
		else:
			return 0
		return 1


	
	def Delbyname(self, nam):
		''' Удаляет позицию с именем nam '''
		if not self.Is_Exist(nam):
			return 0
		self.names.remove(nam)
		self.content.pop(nam)
		return 1


	def Prompt(self, nam):
		''' Возвращает подсказку у позиции nam '''
		if not self.Is_Exist(nam):
			return ''
		return self.content[nam][3]

	
	def Type(self, nam):
		''' Возвращает тип у позиции nam '''
		if not self.Is_Exist(nam):
			return ''
		return self.content[nam][0]

	
	def Def(self, nam):
		''' Возвращает умолчание у позиции nam. Если тип only, то вернётся номер у current'''
		if not self.Is_Exist(nam):
			return 0
		return self.content[nam][2]


	def Val(self, nam):
		''' Возвращает значение у позиции nam. Если меню не запускалось, возвращает умолчание если имени нет, возвращает 0 '''
		if not self.Is_Exist(nam):
			return 0
		return self.content[nam][1].value



	def Move(self, n1=0, n2=0):
		'''Переносит номер n1 в позицию n2'''
		if n1>=len(self.names) or n2>=len(self.names):
			return 0
		if n1==n2:
			return 0
		nam=self.names.pop(n1)
		self.names.insert(n2, nam)
		return 1

	def Num(self, nam=''):
		''' Возвращает номер позиции с именем nam. Если такой позиции нет, возвращает номер последней позиции'''
		if not self.Is_Exist(nam):
			return len(self.names)-1
		return self.names.index(nam)

	def Nam(self, n=0):
		'''Возвращает имя у позиции с номером n'''
		if n>=len(self.names):
			return ''
		return self.names[n]

	def Add_Real_List(self, nam='', pr='', l=[], d=0, only=0):
		'''Добавляет real с перечислением. d - значение умолчания для list или позиция current для only'''
		if not self.Can_Add(nam):
			return 0
		if len(l)==0:
			return 0
		self.names.append(nam)
		if only==0:
			self.content[nam]=['reallist', k3.Var(), d, pr, l]
		else:
			self.content[nam]=['reallistonly', k3.Var(), d, pr, l]
		return 1


	def Add_String_List(self, nam='', pr='', l=[], d=0, only=0):
		'''Добавляет string с перечислением. d - значение умолчания для list или позиция current для only'''
		if not self.Can_Add(nam):
			return 0
		if len(l)==0:
			return 0
		self.names.append(nam)
		if only==0:
			self.content[nam]=['stringlist', k3.Var(), d, pr, l]
		else:
			self.content[nam]=['stringlistonly', k3.Var(), d, pr, l]
		return 1

	def List(self, nam=''):
		''' Возвращает список для перечисления у позиции nam '''
		if not self.Is_Exist(nam):
			return []
		possible=['reallist', 'reallistonly', 'stringlist', 'stringlistonly']
		if possible.count(self.Type(nam))==0:
			return []
		return self.content[nam][4]

	def Setlist(self, nam='', l=[]):
		'''устанавливает позиции nam список l'''
		if not self.Is_Exist(nam):
			return 0
		possible=['reallist', 'reallistonly', 'stringlist', 'stringlistonly']
		if possible.count(self.Type(nam))==0:
			return 0
		if len(l)==0:
			return 0
		self.content[nam][2]=l
		return 1
	
	def Is_Exist(self, nam=''):
		'''Возвращает 1, если позиция существует и 0, если nam пустое или позиции нет'''
		if nam=='':
			return 0
		if self.names.count(nam)==0:
			return 0
		return 1

	def Can_Add(self, nam=''):
		'''Возвращает 1, если позицию можно добавить и 0, если nam пустое или такая позиция есть'''
		if nam=='':
			return 0
		if self.names.count(nam)>0:
			return 0
		return 1


	def Curr(self, nam=''):
		'''Возвращает значение текущего элемента списка для listonly'''
		if not self.Is_Exist(nam):
			return 0
		possible=['reallistonly', 'stringlistonly']
		if possible.count(self.Type(nam))==0:
			return 0
		return self.List(nam)[self.Def(nam)]


	def Put_Curr(self, nam=''):
		'''Возвращает список для listonly со встевленным в нужное место k3.k_current'''
		if not self.Is_Exist(nam):
			return []
		possible=['reallistonly', 'stringlistonly']
		if possible.count(self.Type(nam))==0:
			return []
		l=[]
		l.extend(self.List(nam))
		l.insert(int(self.Def(nam)), k3.k_current)
		return l

	def Refresh(self):
		''' Назначает всем умолчаниям текущие значение Надо добавить реакцию на only'''
		for i in range(len(self.names)):
			if not self.Type(self.names[i])=='button':
				if not (self.Type(self.names[i])=='reallistonly' or self.Type(self.names[i])=='stringlistonly'):
					self.Setdef(self.names[i], self.Val(self.names[i]))
				else:
					val=self.Val(self.names[i])
					l=self.List(self.names[i])
					n=l.index(val)
					self.Setdef(self.names[i], n)

	def Setdef(self, nam, d):
		''' Устанавливает позиции nam умолчание d Если тип only, то мы получаем номер, а в переменную нужно положить значение из списка'''
		if not self.Is_Exist(nam):
			return 0
		self.content[nam][2]=d
		if not (self.Type(nam)=='reallistonly' or self.Type(nam)=='stringlistonly'):
			self.content[nam][1].value=d
		else:
			self.content[nam][1].value=self.List[d]
		return 1





	# --- --- --- --- --- --- --- Надо написать --- --- --- --- --- --- ---












# --- Тестируем

if __name__ == '__main__':

	men=k3menu('Я окошко', '', k3.k_left, 'Я менюшко')
	men.Add_Real('real1', 'Первое число', 100)
	men.Add_Real('real2', 'Второе число', 200)
	men.Add_Button('butt')
	men.Add_String('str1', 'Я строка', 'Я строка')
	men.Add_Logical('log1', 'Я галочка', 0)
	men.Add_Button('butt2')
	men.Add_Real_List('list1', 'Я список чисел', [1,2,3,4,5], 3, 0)
	men.Add_Real_List('list2', 'Я тоталитарный список чисел', [10,20,30,40], 1, 1)
	men.Add_String_List('list3', 'Я добрый список строк', ['Улыбка','Веселье','Солнце','Мячики'], 'Облака', 0)
	men.Add_String_List('list4', 'Я грустный список строк', ['Работа','Ещё работа','Тучи','Будильник'], 2, 1)
	men.Show()
	men.Refresh()
	men.Show()
