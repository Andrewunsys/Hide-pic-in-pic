import os

from PIL import Image, ImageDraw
from tkinter import Tk, Button, Label, Entry, Checkbutton, filedialog, IntVar, END
# from tkinter import *


def show_color_component(in_color):
	"""Функция получает компонент цвета in_color - целое числа от 0 до 255. 
	Пять последних битов ставит на место первых пять, три последних бита заменяются нулями.
	12345678 -> 45678000
	Возвращвет компонент цвет цвета - целое числа от 0 до 255."""

	color_bin_0=bin(in_color)
	color_bin = color_bin_0[2:]
	while len(color_bin)<8:
		color_bin=f"0{color_bin}"
	new_color_bin=f"{color_bin[3:8]}0000"
	new_color=int(new_color_bin, base=2)

	return(new_color)	


def new_color_component(base_color, hide_color):
	"""Функция получает компоненты цвета base_color (от изображения где прячем) и hide_color (от изображения что прячем)
	Получаемые компоненты (base_color, hide_color) - целые числа от 0 до 255. 
	Пять последних битов цвета base_color меняются на пять первых бита цвета hide_color: 
	b1b2b3b4b5b6b7b8 + h1h2h3h4h5h6h7h8 = b1b2b3h1h2h3h4h5.
	Возвращвет компонент цвет цвета - целое числа от 0 до 255."""

	base_color_bin_0=bin(base_color)
	base_color_bin=base_color_bin_0[2:]
	while len(base_color_bin)<8:
		base_color_bin=f"0{base_color_bin}"

	hide_color_bin_0=bin(hide_color)
	hide_color_bin=hide_color_bin_0[2:]
	while len(hide_color_bin)<8:
		hide_color_bin=f"0{hide_color_bin}"

	new_color_bin=f"{base_color_bin[0:3]}{hide_color_bin[0:5]}"
	new_color=int(new_color_bin, base=2)

	return(new_color)


def show_about():
	""" Краткая справка о программе	в отдельном окне"""

	window_about = Tk()
	window_about.geometry("400x310")
	window_about.title("About 'Hide pics'")

	all_font='Arial 9'

	text1="\tПрограмма 'Hide pics'\n"
	text1+="Версия:\t\t\t0.02\n"
	text1+="Дата последнего изменения:\t19.11.2021\n"
	text1+="Дата создания:\t\t17.11.2021\n"
	text1+="Автор:\t\t\tА\n"

	text2="Программа позволяет:\n\t-Скрывать одно изображение в другом\n\t с помощью цифровой стеганографии.\n"
	text2+="\t-Показывать ранее скрытое изображение.\n\n"
	text2+="- Соктытие происходить путем замены двух последних битов \nкаждого канала RGB в пикселе изображения 'где прячем'\n"
	text2+="на два первых бита скрываемого изображения.\n"
	text2+="- Скрываемое изображение теряет качество.\n\n"
	text2+="- На вход должны выбираться файлы графических форматов.\n"
	text2+="- Скрываемое изображение должно иметь меньшие \nили равные размеры (высота и ширина в пикселях) \nчем изображения 'где прячем'.\n"

	lbl_about1=Label(window_about, text = text1, anchor='nw', justify='left', font=(all_font))
	lbl_about1.place(x = 10, y = 10, width = 380, height = 70)
	lbl_about2=Label(window_about, text = text2, anchor='nw', justify='left', font=(all_font))
	lbl_about2.place(x = 10, y = 90, width = 380, height = 210)

	window_about.mainloop()


def choose_file():
	""" Получение пути к выбранному файлу в вызываемом диалоговом окне. 
	Возвращает путь."""
	
	# filetypes = ("Изображение", "*.bmp *.jpg *.gif *.png")
	initial_dir=os.getcwd()	# "/"
	filename = filedialog.askopenfilename(initialdir=initial_dir, title="Select An Image", filetypes=(("jpeg files", "*.jpg"), ("bmp files", "*.bmp"), ("gif files", "*.gif*"), ("png files", "*.png")))
	if filename:
		return(filename)


def choose_file_to_hide():
	""" Предварительно очищает, а затем заполняет Entry Box (скрываемого файла) 
	путем к выбранному к сокрытию файлу  """

	entry_file_to_hide.delete(0, END)
	filename = choose_file()
	entry_file_to_hide.insert(0, filename)


def choose_file_where_hide():
	""" Предварительно очищает, а затем заполняет Entry Box (файла, где прячем изображение) 
	путем к выбранному для сохранения инфорации файлу  """

	entry_file_where_hide.delete(0, END)
	filename = choose_file()
	entry_file_where_hide.insert(0, filename)


def choose_file_to_show():
	""" Предварительно очищает, а затем заполняет Entry Box (файла, который надо расшифровать) 
	путем к выбранному для расшифровке файлу  """

	entry_file_to_show.delete(0, END)
	filename = choose_file()
	entry_file_to_show.insert(0, filename)
	# print(chk.get())


def hide_and_save():
	""" Функция скрытия одного файла в другом файл  """

	### Что прячем
	img_hide_path=entry_file_to_hide.get()
	img_hide = Image.open(img_hide_path)
	width_hide = img_hide.size[0] 	# Определяем ширину.
	height_hide = img_hide.size[1] 	# Определяем высоту.
	pix_hide = img_hide.load() 		# Выгружаем значения пикселей.
	# pix_hide_hex=[[0] * height_hide for i in range(width_hide)]	# Создание двумерного списка

	### Где прячем
	img_base_path=entry_file_where_hide.get()
	img_base = Image.open(img_base_path)
	width_base = img_base.size[0] #Определяем ширину.
	height_base = img_base.size[1] #Определяем высоту.
	pix_base = img_base.load() #Выгружаем значения пикселей.
	# pix_base_hex=[[0] * height_base for i in range(width_base)]

	### Итог Пряток
	image = Image.new("RGB", (width_base, height_base))
	draw = ImageDraw.Draw(image)
	for i in range(width_base):
		for j in range(height_base):
			# color_base=pix_base_hex[i][j]
			if i<width_hide and j<height_hide:
				a = new_color_component(pix_base[i, j][0], pix_hide[i, j][0])
				b = new_color_component(pix_base[i, j][1], pix_hide[i, j][1])
				c = new_color_component(pix_base[i, j][2], pix_hide[i, j][2])
				pix_new_hex=(a, b, c)	#'#{:02x}{:02x}{:02x}'.format(a, b, c) #convert rgb to hex
			else:
				pix_new_hex=(pix_base[i, j][0], pix_base[i, j][1], pix_base[i, j][2]) #'#{:02x}{:02x}{:02x}'.format(pix_base[i, j][0], pix_base[i, j][1], pix_base[i, j][2])
			draw.point((i, j), pix_new_hex)

	fname = f"{entry_new_file_where_hide.get()}"
	image.save(fname)
	image.show()
	

def show_and_save():
	""" Функция расшифровки файла со скрытым по определенному алгоритму изображению """

	### Расшифровка спрятоанного
	### Откуда извлекам
	img_base_path=entry_file_to_show.get()
	img_base = Image.open(img_base_path)
	width_base = img_base.size[0] #Определяем ширину.
	height_base = img_base.size[1] #Определяем высоту.
	pix_base = img_base.load() #Выгружаем значения пикселей.
	# pix_base_hex=[[0] * height_base for i in range(width_base)]

	### Итог Пряток
	image1 = Image.new("RGB", (width_base, height_base))
	draw1 = ImageDraw.Draw(image1)
	for i in range(width_base):
		for j in range(height_base):
			a = show_color_component(pix_base[i, j][0])
			b = show_color_component(pix_base[i, j][1])
			c = show_color_component(pix_base[i, j][2])
			pix_new_hex=(a, b, c) # '#{:02x}{:02x}{:02x}'.format(a, b, c) #convert rgb to hex
			draw1.point((i, j), pix_new_hex)

	fname = f"{entry_new_file_show_and_save.get()}"
	image1.save(fname)
	image1.show()
	

############### main 

window = Tk()
window.geometry("550x280")
window.resizable(width=0, height=0)	# не позволяет изменять размер как ширину, так и высоту
window.title('Hide pics')

all_font='Arial 9'
btn_x = 430
btn_width = 110

### 
lbl_file_to_hide=Label(window, text = "Что прячем:", anchor='e', justify='left', font=(all_font)) 
lbl_file_to_hide.place(x = 10, y = 10, width = 110, height = 25)

entry_file_to_hide = Entry (window, text = "")
entry_file_to_hide.place(x = 120 , y = 10, width = 300, height = 25)

but_file_to_hide = Button(window, text = "Выбрать файл...", background="gray90", font=(all_font), command = choose_file_to_hide)
but_file_to_hide.place(x = btn_x, y = 10, width = btn_width, height = 25)

###
lbl_file_where_hide=Label(window, text = "В чем прячем:", anchor='e', justify='left', font=(all_font))
lbl_file_where_hide.place(x = 10, y = 40, width = 110, height = 25)

entry_file_where_hide = Entry (window, text = "")
entry_file_where_hide.place(x = 120 , y = 40, width = 300, height = 25)

but_file_where_hide = Button(window, text = "Выбрать файл...", background="gray90", font=(all_font), command = choose_file_where_hide)
but_file_where_hide.place(x = btn_x, y = 40, width = btn_width, height = 25)

###
lbl_new_file_where_hide=Label(window, text = "Имя файла в котором прячем:", anchor='e', justify='right', font=(all_font))
lbl_new_file_where_hide.place(x = 10, y = 70, width = 240, height = 25)

entry_new_file_where_hide = Entry (window, text = "")
entry_new_file_where_hide.place(x = 250 , y = 70, width = 170, height = 25)
entry_new_file_where_hide.insert(0, 'hide_pic.jpg')

but_new_file_where_hide = Button(window, text = "Спрятать", background="gray90", font=(all_font), command = hide_and_save)
but_new_file_where_hide.place(x = btn_x, y = 70, width = btn_width, height = 25)

###
###
lbl_file_to_show=Label(window, text = "Откуда извлекаем:", anchor='e',justify='left', font=(all_font))
lbl_file_to_show.place(x = 10, y = 120, width = 110, height = 25)

entry_file_to_show = Entry (window, text = "")
entry_file_to_show.place(x = 120 , y = 120, width = 300, height = 25)

but_file_to_show = Button(window, text = "Выбрать файл...", background="gray90", font=(all_font), command = choose_file_to_show)
but_file_to_show.place(x = btn_x, y = 120, width = btn_width, height = 25)

###
lbl_new_file_show_and_save=Label(window, text = "Имя файла где показаываем спрятанное:", anchor='e',justify='right', font=(all_font))
lbl_new_file_show_and_save.place(x = 10, y = 150, width = 240, height = 25)

entry_new_file_show_and_save = Entry (window, text = "")
entry_new_file_show_and_save.place(x = 250 , y = 150, width = 170, height = 25)
entry_new_file_show_and_save.insert(0, 'show_pic.jpg')

but_new_file_show_and_save = Button(window, text = "Расшифровать", background="gray90", font=(all_font), command = show_and_save)
but_new_file_show_and_save.place(x = btn_x, y = 150, width = btn_width, height = 25)

# # chk_state1 = BooleanVar()  
# var_chk=IntVar()
# chk_state=(False)  # задайте проверку состояния чекбокса  
# chk = Checkbutton(window, text='Показать расшифрованный файл', font=('Arial 9'), anchor='w',  variable =var_chk, var=chk_state)  
# chk.place(x = 250, y = 180, width = 220, height = 25)

###
###
but_about = Button(window, text = "О программе ...", background="gray90", font=(all_font), command = show_about)
but_about.place(x = btn_x, y = 240, width = btn_width, height = 25)

window.mainloop()