# coding=cp1251

# --- ����� ����� ����� ���� ��� setvar

# --- ������ ������ � ���� ���������, ��������, ���� � ����� ��� ���� � ������� ��� ����������.

# --- ��������� ������� - ���: ["���", k3.Var, ���������, "���������"]

# --- ������ �� ��������: ���� reallist, reallistonly, stringlist, stringlistonly. ����� ��������� � ������ ����� [] ��� ������. 
# --- ���� ��� list, ��������� - ��� ��������. ���� ��� listonly, ��������� - ��� ����� �urrent
# --- ������ ������� ������ ������ ������, ��� k3.k_current. ������� �������� ����� ��������� �����, ����� �����������.

# --- ���� �� �������� � ��������������� �������� 7 � 8

import k3

class k3menu:

	def __init__(self, capt='', pic='', kwrd='left', text=''):
		''' ��� ������ �������� ��������� ����, ��� ����� ��� ��������, �������� ����� ��� ������������ � ���� ������ ��� ������'''

		# -- �������� �������
		self.capt=capt	# ��������� ����
		self.pic=pic	# ���� ��������
		
		if kwrd=='center':
			self.kwrd=k3,k_center
		elif kwrd=='right':
			self.kwrd=k3.k_right
		else:
			self.kwrd=k3.k_left
		
		self.text=text	# ����� � ����

		# -- ������� �� ������� ����
		self.content={}

		# -- ������������� ������ ���. � �� ������ ������� �������
		self.names=[]

	def Show(self):
		''' ��� ������ ���������� ���� � k3 � ��� ������� Ok ��������� ������� ������������'''
		param=[]					# ��, ��� �� ������� � setvar

		# -- ��������� ������ ��� ����������
		param.extend([self.capt, self.pic, self.kwrd, self.text, k3.k_done])

		# -- ����� �� ������ self.names � ��������� ������ � param � ����������� �� ����

		for i in range(len(self.names)):
			currname=self.names[i]
			if self.Type(currname)=='real':
				# -- ���������� ��� ���� real
				param.extend([k3.k_real, k3.k_auto, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='reallist':
				# -- ���������� ��� ���� reallist
				param.extend([k3.k_real, k3.k_auto, k3.k_default, self.Def(currname), k3.k_list])
				param.extend(self.List(currname))
				param.append(k3.k_done)

			if self.Type(currname)=='reallistonly':
				# -- ���������� ��� ���� reallistonly
				param.extend([k3.k_real, k3.k_auto, k3.k_listonly])
				param.extend(self.Put_Curr(currname))
				param.append(k3.k_done)

			if self.Type(currname)=='string':
				# -- ���������� ��� ���� string
				param.extend([k3.k_string, k3.k_auto, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 1':
				# -- ���������� ��� ���� string
				param.extend([k3.k_string, k3.k_button, 1, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 2':
				# -- ���������� ��� ���� string
				param.extend([k3.k_string, k3.k_button, 2, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 3':
				# -- ���������� ��� ���� string
				param.extend([k3.k_string, k3.k_button, 3, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 4':
				# -- ���������� ��� ���� string
				param.extend([k3.k_string, k3.k_button, 4, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 5':
				# -- ���������� ��� ���� string
				param.extend([k3.k_string, k3.k_button, 5, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 6':
				# -- ���������� ��� ���� string
				param.extend([k3.k_string, k3.k_button, 6, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 7':
				# -- ���������� ��� ���� string
				param.extend([k3.k_string, k3.k_button, 7, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='string 8':
				# -- ���������� ��� ���� string
				param.extend([k3.k_string, k3.k_button, 8, k3.k_default, self.Def(currname)])


			
			if self.Type(currname)=='stringlist':
				# -- ���������� ��� ���� stringlist
				param.extend([k3.k_string, k3.k_auto, k3.k_default, self.Def(currname), k3.k_list])
				param.extend(self.List(currname))
				param.append(k3.k_done)

			if self.Type(currname)=='stringlistonly':
				# -- ���������� ��� ���� stringlistonly
				param.extend([k3.k_string, k3.k_auto, k3.k_listonly])
				param.extend(self.Put_Curr(currname))
				param.append(k3.k_done)

			if self.Type(currname)=='logical':
				# -- ���������� ��� ���� logical
				param.extend([k3.k_logical, k3.k_default, self.Def(currname)])

			if self.Type(currname)=='button':
				# -- ���������� ��� ���� button
				param.append(k3.k_button)

			param.extend([self.Prompt(currname), self.content[self.names[i]][1]])
		
		param.append(k3.k_done)


		res=k3.setvar(param)
		return int(res[0])

	def Add_Real(self, nam='', pr='', d=0):
		''' ��������� ������� � ���������� real ������ nam, ���������� pr � ���������� d '''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		self.content[nam]=['real', k3.Var(), d, pr]
		self.Setdef(nam, d)
		return 1
	

	def Add_Logical(self, nam='', pr='', d=0):
		''' ��������� ������� � ���������� logical '''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		self.content[nam]=['logical', k3.Var(), d, pr]
		self.Setdef(nam, d)
		return 1

	def Add_String(self, nam='', pr='', d=''):
		''' ��������� ������� � ���������� string '''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		self.content[nam]=['string', k3.Var(), d, pr]
		self.Setdef(nam, d)
		return 1

	def Add_Button(self, nam=''):
		''' ��������� �������������� ����� '''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		self.content[nam]=['button', k3.Var(), 0, '  ']
		self.Setdef(nam, 0)
		return 1

	def Add_String_Code(self, nam='', pr='', d='', cod=0):
		'''��������� ����������� string � ��������. � cod �������� ���'''
		if not self.Can_Add(nam):
			return 0
		self.names.append(nam)
		if (cod>0) and (cod<8):
			self.content[nam]=['string '+str(int(cod)), k3.Var(), d, pr]
			self.Setdef(nam, d)

		elif cod==8:
			# ������ ���������� ������ ��� ��������
			self.content[nam]=['string 8', k3.VarArray(100), d, pr]
		else:
			return 0
		return 1


	
	def Delbyname(self, nam):
		''' ������� ������� � ������ nam '''
		if not self.Is_Exist(nam):
			return 0
		self.names.remove(nam)
		self.content.pop(nam)
		return 1


	def Prompt(self, nam):
		''' ���������� ��������� � ������� nam '''
		if not self.Is_Exist(nam):
			return ''
		return self.content[nam][3]

	
	def Type(self, nam):
		''' ���������� ��� � ������� nam '''
		if not self.Is_Exist(nam):
			return ''
		return self.content[nam][0]

	
	def Def(self, nam):
		''' ���������� ��������� � ������� nam. ���� ��� only, �� ������� ����� � current'''
		if not self.Is_Exist(nam):
			return 0
		return self.content[nam][2]


	def Val(self, nam):
		''' ���������� �������� � ������� nam. ���� ���� �� �����������, ���������� ��������� ���� ����� ���, ���������� 0 '''
		if not self.Is_Exist(nam):
			return 0
		return self.content[nam][1].value



	def Move(self, n1=0, n2=0):
		'''��������� ����� n1 � ������� n2'''
		if n1>=len(self.names) or n2>=len(self.names):
			return 0
		if n1==n2:
			return 0
		nam=self.names.pop(n1)
		self.names.insert(n2, nam)
		return 1

	def Num(self, nam=''):
		''' ���������� ����� ������� � ������ nam. ���� ����� ������� ���, ���������� ����� ��������� �������'''
		if not self.Is_Exist(nam):
			return len(self.names)-1
		return self.names.index(nam)

	def Nam(self, n=0):
		'''���������� ��� � ������� � ������� n'''
		if n>=len(self.names):
			return ''
		return self.names[n]

	def Add_Real_List(self, nam='', pr='', l=[], d=0, only=0):
		'''��������� real � �������������. d - �������� ��������� ��� list ��� ������� current ��� only'''
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
		'''��������� string � �������������. d - �������� ��������� ��� list ��� ������� current ��� only'''
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
		''' ���������� ������ ��� ������������ � ������� nam '''
		if not self.Is_Exist(nam):
			return []
		possible=['reallist', 'reallistonly', 'stringlist', 'stringlistonly']
		if possible.count(self.Type(nam))==0:
			return []
		return self.content[nam][4]

	def Setlist(self, nam='', l=[]):
		'''������������� ������� nam ������ l'''
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
		'''���������� 1, ���� ������� ���������� � 0, ���� nam ������ ��� ������� ���'''
		if nam=='':
			return 0
		if self.names.count(nam)==0:
			return 0
		return 1

	def Can_Add(self, nam=''):
		'''���������� 1, ���� ������� ����� �������� � 0, ���� nam ������ ��� ����� ������� ����'''
		if nam=='':
			return 0
		if self.names.count(nam)>0:
			return 0
		return 1


	def Curr(self, nam=''):
		'''���������� �������� �������� �������� ������ ��� listonly'''
		if not self.Is_Exist(nam):
			return 0
		possible=['reallistonly', 'stringlistonly']
		if possible.count(self.Type(nam))==0:
			return 0
		return self.List(nam)[self.Def(nam)]


	def Put_Curr(self, nam=''):
		'''���������� ������ ��� listonly �� ����������� � ������ ����� k3.k_current'''
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
		''' ��������� ���� ���������� ������� �������� ���� �������� ������� �� only'''
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
		''' ������������� ������� nam ��������� d ���� ��� only, �� �� �������� �����, � � ���������� ����� �������� �������� �� ������'''
		if not self.Is_Exist(nam):
			return 0
		self.content[nam][2]=d
		if not (self.Type(nam)=='reallistonly' or self.Type(nam)=='stringlistonly'):
			self.content[nam][1].value=d
		else:
			self.content[nam][1].value=self.List[d]
		return 1





	# --- --- --- --- --- --- --- ���� �������� --- --- --- --- --- --- ---












# --- ���������

if __name__ == '__main__':

	men=k3menu('� ������', '', k3.k_left, '� �������')
	men.Add_Real('real1', '������ �����', 100)
	men.Add_Real('real2', '������ �����', 200)
	men.Add_Button('butt')
	men.Add_String('str1', '� ������', '� ������')
	men.Add_Logical('log1', '� �������', 0)
	men.Add_Button('butt2')
	men.Add_Real_List('list1', '� ������ �����', [1,2,3,4,5], 3, 0)
	men.Add_Real_List('list2', '� ������������ ������ �����', [10,20,30,40], 1, 1)
	men.Add_String_List('list3', '� ������ ������ �����', ['������','�������','������','������'], '������', 0)
	men.Add_String_List('list4', '� �������� ������ �����', ['������','��� ������','����','���������'], 2, 1)
	men.Show()
	men.Refresh()
	men.Show()
