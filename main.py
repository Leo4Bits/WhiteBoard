from tkinter import *
from tkinter.ttk import *
from function import *
from PIL import Image,ImageTk # hiển thị ảnh trên tkinterC

#________SIZE_PEN AND COLOR
## SIZE_PEN
size_pen = 5
def increase_decrease_sizePen(n):
    global size_pen
    if (n == 1): 
        size_pen+=1
        print("Đã tăng kích thước pen xuống là :",size_pen)
    if (n == 2 and size_pen > 0): 
        size_pen-=1
        print("Đã giảm kích thước pen xuống là :",size_pen)

# create main win
root = Tk()
root.geometry("2000x500")
root.title("White board")
root.configure(bg="gray")

# 1. create canvas
canvas = Canvas(root,bg="white",width=1600,height=500)
canvas.place(x=200,y=0)

## creat combobox change color
lst = []
with open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\data_color.txt") as data:
    for line in data:
        lst += [color.strip() for color in line.strip().split(",") if color.strip()]
combobox_change_color = Combobox(root,width=15,height=2,state="readonly",values=lst)
combobox_change_color.current(7)
combobox_change_color.place(x=50,y=125)
## creat button PEN free draw
img_pen_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\pencil_pic.png")
resize_img_pen = img_pen_path.resize((37,35),resample=Image.Resampling.LANCZOS)
img_pen = ImageTk.PhotoImage(resize_img_pen)
button_pen = Button(root,text="draw",background="white",image=img_pen, command= lambda : setup_draw_pen(0,canvas,size_pen,combobox_change_color.get()))
button_pen.place(x=50,y=25)
## creat button click to select and move particular item
img_cursor_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\cursor_pic.png")
resize_img_cursor = img_cursor_path.resize((37,35),resample=Image.Resampling.LANCZOS)
img_cursor = ImageTk.PhotoImage(resize_img_cursor)
button_cursor = Button(root,background="white",image=img_cursor,command=lambda :setup_move_item(cur_canvas=canvas))
button_cursor.place(x=110,y=25)
## creat button erase
img_erase_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\erase_pic.png")
resize_img_erase = img_erase_path.resize((37,35),resample=Image.Resampling.LANCZOS)
img_erase = ImageTk.PhotoImage(resize_img_erase)
button_erase = Button(root,text="erase",background="white",image=img_erase, command= lambda : setup_draw_pen(0,canvas,size_pen,"white"))
button_erase.place(x=50,y=75)
## creat button text
button_text = Button(root,text="Text",background="white",width=5,height=2,command= lambda : setup_draw_pen(4,canvas,size_pen,combobox_change_color.get()))
button_text.place(x=110,y=75)
## creat button increase pen_size
button_increase = Button(root,text="+",font=7,background="white",width=5,height=2,command= lambda:increase_decrease_sizePen(1))
button_increase.place(x=50,y=225)
## creat button decrease pen_size
button_decrease = Button(root,text="-",font=7,background="white",width=5,height=2,command= lambda:increase_decrease_sizePen(2))
button_decrease.place(x=110,y=225)

# DRAW create draw Draw a PREDEFINED SHAPE
## button draw LINE
img_line_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\line_pic.png")
resize_img_line = img_line_path.resize((25,25),resample=Image.Resampling.LANCZOS)
img_line = ImageTk.PhotoImage(resize_img_line)
button_draw_line = Button(root,text="erase",background="white",image=img_line,command= lambda : setup_draw_pen(1,canvas,size_pen,combobox_change_color.get()))
button_draw_line.place(x=50,y=355)
## button draw RECTANGLE
img_rec_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\rectangle_pic.png")
resize_img_rec = img_rec_path.resize((25,25),resample=Image.Resampling.LANCZOS)
img_rec = ImageTk.PhotoImage(resize_img_rec)
button_draw_rec = Button(root,text="erase",background="white",image=img_rec,command= lambda : setup_draw_pen(2,canvas,size_pen,combobox_change_color.get()))
button_draw_rec.place(x=100,y=355)
## button draw elip
img_elip_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\elipse_pic.png")
resize_img_elip = img_elip_path.resize((25,25),resample=Image.Resampling.LANCZOS)
img_elip = ImageTk.PhotoImage(resize_img_elip)
button_draw_elip = Button(root,text="erase",background="white",image=img_elip,command= lambda : setup_draw_pen(3,canvas,size_pen,combobox_change_color.get()))
button_draw_elip.place(x=150,y=355)

'''Mình thêm cái button release chỉ cần biết điểm đầu và cuối là điểm thả chuột, nếu dùng motion thì nó sẽ theo dỗi và vẽ nhiều khối liên tục'''

# display logo LEODEV
logo = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\LeoDevText.png")
resize_logo = logo.resize((125,50),resample=Image.Resampling.LANCZOS)
img_logo = ImageTk.PhotoImage(resize_logo)
button_logo = Button(root,background="white",image=img_logo)
button_logo.place(x=50,y=405)

# follow action 
canvas.bind("<B1-Motion>", handle_drag)
root.mainloop()
