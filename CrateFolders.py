from tkinter import *
import os


class Application(Frame):
	def __init__(self, master):
		super(Application, self).__init__(master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		self.inst_lbl = Label(self, text ='Input main folder')
		self.inst_lbl.grid(row = 0, column = 0, columnspan = 2, sticky = W)

		self.pw_lbl = Label(self, text = 'Folder: ')
		self.pw_lbl.grid(row = 1, column = 0, sticky = W)

		self.pw_ent = Entry(self, bd = 2)
		self.pw_ent.grid(row = 3, column = 0, sticky = N)

		self.submit_bttn = Button(self)
		self.submit_bttn.configure( text = 'Create folder', width = 16, height = 1, bd = 3,command = self.reveal)
		self.submit_bttn.grid(row = 3, column = 0, sticky = S)

		self.root_lbl = Label(self)
		self.root_lbl.grid(row = 3, column = 0, sticky = W)
		self.root_lbl.configure(text = '''
Правило ввода:
Вводите папки через
табуляцию. Если 
она стоит перед
папкой, то эта 
папка будет поме-
щена в пред. папку.''')

		self.secret_txt = Text(self, width = 66, height = 2, wrap = WORD)
		self.secret_txt.grid(row = 5, column = 0, columnspan = 2, sticky = W)

		self.inst_lbl1 = Label(self, text ='Input isnside folders:')
		self.inst_lbl1.grid(row = 0, column = 1, sticky = W)

		self.pw1_ent = Text(self, height= 20, width = 50, wrap=WORD )
		self.pw1_ent.grid(row = 3, column = 1, sticky = W)

	def reveal(self):
		main = Main()
		read_pw1_ent = self.pw1_ent.get(0.0, END)
		read = main.fixAndOpen('w')
		read.write(read_pw1_ent)
		read.close()


		projectname = self.pw_ent.get()
		self.secret_txt.delete(0.0, END)
		self.secret_txt.insert(0.0, 'Folder ' + str(projectname) + ' create')

		path = r'C:\Users\EasyAdmin\AppData\Roaming\ProjectPy\ProjectName'		
		fullPath = os.path.join(path, projectname) 
		folders = main.createList()
		main.createFolder(fullPath)										
		main.build(fullPath, folders)



class Main():
	def fixAndOpen(self, n):
		scriptpath = os.path.dirname(__file__)
		filename = os.path.join(scriptpath, 'Folder.txt')
		read = open(filename, n)
		return read
	
	
	def divisionNumAndWord(self, line):
		global digits
		
		word = ''
		for k in range(len(line) -1, -1, -1):
			word += line[k]
	
		fullWord = word
		while word[-1].isdigit():
			word = word[:-1]
		digits = fullWord.replace(word, '')
		digits = len(digits)
		line = ''
		
		for k in range(len(word) -1, -1, -1):
			line += word[k]
		
	
	def createList(self):
		try:
			folders = []
			read = self.fixAndOpen('r')
			lines = read.readlines()
			for line in lines:
				line = line.replace('\n', '')
				line = line.replace('\t', '1')
				self.divisionNumAndWord(line)
				line = line.replace('1', '')
	
				if digits == 0:
					high_folder = [line, []]
					folders.append(high_folder)
		
				elif digits == 1:
					average_folder = [line, []]
					high_folder[1].append(average_folder)
			
				elif digits == 2:
					low_folder = [line, []]
					average_folder[1].append(low_folder)


			read.close()
			return folders
		
		except UnboundLocalError:
			print('You made mistake of tabulation in file')
	
	def createFolder(self, path):
		if not os.path.exists(path): 								# Проверяет есть ли путь path
			os.mkdir(path) 											#создаёт папку по пути который мы создали выше  
	
	def build(self, root, data):
		if data:													#Если не пустые данные
			for d in data: 											#Запускаем цикл по элементам 
				name = d[0]										 	#Имя папки нулевой элемент, d это весь список
				path = os.path.join(root, name) 					#Собираем полный путь 
				self.createFolder(path) 							#Запускаем функцую
				self.build(path, d[1])
	

root = Tk()
root.title('CreateFolder')
root.geometry('550x450')
root.maxsize(550, 450)
app = Application(root)
root.mainloop()
