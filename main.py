from tkinter import *
from tkinter import colorchooser
from tkinter.ttk import * # dùng các Combobox → không dùng có thể ẩn nhưng thư viện này dùng bản mới nhất → làm giao diện trông đẹp hơn
from function import *
from PIL import Image,ImageTk # hiển thị ảnh trên tkinterC

# reset file data_tag for saving new tags in the new initial board
Write(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoardVer2\data_id.json",[[],[]])

#________SIZE_PEN AND COLOR
## SIZE_PEN
size_pen = 5
def increase_decrease_sizePen(n): ## except increase, decrease, now add reset default size with n = 0
    global size_pen
    if (n == 1): 
        size_pen+=1
        print("Đã tăng kích thước pen lên là :",size_pen)
    if (n == 2 and size_pen > 0): 
        size_pen-=1
        print("Đã giảm kích thước pen xuống là :",size_pen)
    if (n == 0 ): 
        size_pen =5
        print("Đã reset kích thước pen  :",size_pen)
    label_show_cur_size.config(text= f"Kích thước hiện tại {size_pen}")

# create main win
root = Tk()
root.geometry("2000x700")
root.title("White board")
root.configure(bg="#00fdfd")

# 1. create canvas
canvas = Canvas(root,bg="white",width=1600,height=660)
canvas.place(x=150,y=0)

## create colorchooser change COLOR
my_color = "black"
def Change_color():
    global my_color, button_change_color
    my_color = colorchooser.askcolor()[1]
    button_change_color.config(bg=my_color)
    print(f"{my_color}")
# button change color
button_change_color = Button(master=root,text="Change color", command=Change_color,width=15)
button_change_color.place(x=20,y=120)

## creat button PEN free draw
img_pen_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\pencil_pic.png")
resize_img_pen = img_pen_path.resize((37,35),resample=Image.Resampling.LANCZOS)
img_pen = ImageTk.PhotoImage(resize_img_pen)
button_pen = Button(master=root,text="draw",background="white",image=img_pen,cursor="circle",command= lambda : setup_draw_pen(0,canvas,size_pen,my_color))
button_pen.place(x=20,y=25)
## creat button click to select and move particular item
img_cursor_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\cursor_pic.png")
resize_img_cursor = img_cursor_path.resize((37,35),resample=Image.Resampling.LANCZOS)
img_cursor = ImageTk.PhotoImage(resize_img_cursor)
button_cursor = Button(master=root,background="white",image=img_cursor,cursor="fleur",command=lambda :setup_move_item(cur_canvas=canvas))
button_cursor.place(x=80,y=25)
## creat button ERASE
img_erase_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\erase_pic.png")
resize_img_erase = img_erase_path.resize((37,35),resample=Image.Resampling.LANCZOS)
img_erase = ImageTk.PhotoImage(resize_img_erase)
button_erase = Button(master=root,text="erase",background="white",image=img_erase, command= lambda : Erase(cur_canvas=canvas))
button_erase.place(x=20,y=75)
## creat button text
button_text = Button(master=root,text="Text",background="white",width=5,height=2,command= lambda : setup_draw_pen(4,canvas,size_pen,my_color))
button_text.place(x=80,y=75)
## creat button increase pen_size
button_increase = Button(master=root,text="+",font=5,background="white",width=4,command= lambda:increase_decrease_sizePen(1))
button_increase.place(x=20,y=155)
## creat button decrease pen_size
button_decrease = Button(master=root,text="-",font=5,background="white",width=4,command= lambda:increase_decrease_sizePen(2))
button_decrease.place(x=80,y=155)

##  LABEL SHOW CURRENT size
label_show_cur_size = Label(master=root, text= f"Kích thước hiện tại {size_pen}",bg = "#bbffff", width=17)
label_show_cur_size.place(x=15,y=205)
## button to reset to default size
button_reset_default_size = Button(master=root,text="set default size",width=14,background="white",command= lambda:increase_decrease_sizePen(0)) # có thêm tính năng reset size ở hàm này
button_reset_default_size.place(x=20,y=240)

# DRAW create draw Draw a PREDEFINED SHAPE
## button draw LINE
img_line_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\line_pic.png")
resize_img_line = img_line_path.resize((25,25),resample=Image.Resampling.LANCZOS)
img_line = ImageTk.PhotoImage(resize_img_line)
button_draw_line = Button(master=root,text="erase",background="white",image=img_line,cursor="circle",command= lambda : setup_draw_pen(1,canvas,size_pen,my_color))
button_draw_line.place(x=20,y=280)
## button draw RECTANGLE
img_rec_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\rectangle_pic.png")
resize_img_rec = img_rec_path.resize((25,25),resample=Image.Resampling.LANCZOS)
img_rec = ImageTk.PhotoImage(resize_img_rec)
button_draw_rec = Button(master=root,text="erase",background="white",image=img_rec,cursor="circle",command= lambda : setup_draw_pen(2,canvas,size_pen,my_color))
button_draw_rec.place(x=60,y=280)
## button draw elip
img_elip_path = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoard\picture_button\elipse_pic.png")
resize_img_elip = img_elip_path.resize((25,25),resample=Image.Resampling.LANCZOS)
img_elip = ImageTk.PhotoImage(resize_img_elip)
button_draw_elip = Button(master=root,text="erase",background="white",image=img_elip,cursor="circle",command= lambda : setup_draw_pen(3,canvas,size_pen,my_color))
button_draw_elip.place(x=100,y=280)

'''Mình thêm cái button release chỉ cần biết điểm đầu và cuối là điểm thả chuột, nếu dùng motion thì nó sẽ theo dỗi và vẽ nhiều khối liên tục'''

# CREATE BUTTON UNDO-REDO-ZOOM-SHRINK( THU NHỎ )
# undo button
button_undo = Button(master=root,text="UNDO",background="white",font=("Times New Roman",12), command= lambda: undo_redo(canvas, 0))
button_undo.place(x = 680, y = 665)
# redo button
button_redo = Button(master=root,text="REDO",background="white",font=("Times New Roman",12), command= lambda: undo_redo(canvas, 1))
button_redo.place(x = 740, y = 665)
# ZOOM button
button_zoom = Button(master=root,text="ZOOM",background="white",font=("Times New Roman",12), command= lambda: zoom_shrink(canvas,"zoom",size_pen))
button_zoom.place(x = 800, y = 665)
# SHRINK button
button_shrink = Button(master=root,text="SHRINK",background="white",font=("Times New Roman",12), command= lambda: zoom_shrink(canvas,"shrink",size_pen))
button_shrink.place(x = 860, y = 665)

# LOGO
# display logo LEODEV
logo = Image.open(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoardVer2\Picture\logo_leo.png")
resize_logo = logo.resize((125,125),resample=Image.Resampling.LANCZOS)
img_logo = ImageTk.PhotoImage(resize_logo)
button_logo = Button(master=root,background="white",image=img_logo)
button_logo.place(x=10,y=355)
# change default (tkinter) to my app's icon
root.iconbitmap(r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoardVer2\Picture\Logo_WhiteBoardVer2.ico")

# follow action 
canvas.bind("<B1-Motion>", handle_drag)
canvas.bind("<Button-1>", on_click)
root.mainloop()

