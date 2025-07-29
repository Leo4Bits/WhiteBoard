from tkinter import *

tags_id = "__0" # không đặt chuỗi số thuần làm tag như "0" "1" vì python sẽ hiểu nhầm là ID | khi đó mình chỉ có thể di chuyển một đoạn của nét vẽ tự do mặc do full đoạn đều có cùng tag
selected_item = None
move_item = None
# xử lý click
def on_click(event):
    global start_x, start_y

    global tags_id # update tag một lần duy nhất khi click
    tags_id += "1_"

    start_x, start_y = event.x,event.y
    print("Bạn đã click tại:",event.x, event.y)

# xử lý kéo 
def handle_drag(event):
    print("Đang kéo tại:", event.x, event.y)
    

# xử lý enter, để done cái text and chuyển nó sang hiển thị text
# DRAW
def handle_enter(event,entry_text):
    print("Bạn đã enter khi trỏ đang ở vị trí: ",event.x, event.y)
    entry_text.destroy()

def draw(event,n:int,cur_canvas:Canvas,size_pen,pen_color = "black"): # 1 -> line | 2 -> rectangle | 3 -> elipse, oval |
    global start_x, start_y
    
    print(f"TAgs_id hiện tại {tags_id}, {type(tags_id)}")
    for item in cur_canvas.find_all():
        print("Item:", item, "-> tags:", cur_canvas.gettags(item))


    if (n == 1):
        cur_canvas.create_line(start_x,start_y,event.x,event.y,width=size_pen,smooth=True,fill=pen_color,tags=tags_id)
    elif (n == 2):
        cur_canvas.create_rectangle(start_x,start_y,event.x,event.y,width=size_pen,outline = pen_color,tags=tags_id)
    elif (n == 3):
        cur_canvas.create_oval(start_x,start_y,event.x,event.y,width=size_pen,outline = pen_color,tags=tags_id)
    elif (n == 0):
        x, y = event.x, event.y            
        free = cur_canvas.create_line(start_x,start_y,event.x,event.y,width=size_pen,smooth=True, fill=pen_color,tags=tags_id)
        start_x,start_y = x, y
    elif (n == 4):
        entry_text = Entry(cur_canvas,width=size_pen+2,font=("Times New Roman",size_pen))
        entry_text.place(x = start_x, y = start_y)
        entry_text.focus_set()

        def on_enter_key(event):
            text_value = entry_text.get()
            if text_value.strip() != "":
                cur_canvas.create_text(start_x, start_y, fill=pen_color, font=("Times New Roman", size_pen), text=text_value,tags=tags_id)
            entry_text.destroy()

        entry_text.bind("<Return>", on_enter_key)
        
        
def setup_draw_pen(n:int,cur_canvas:Canvas,size_pen, pen_color):
    
    cur_canvas.unbind("<B1-Motion>")
    cur_canvas.unbind("<ButtonRelease-1>")
    cur_canvas.bind("<Button-1>", on_click)
    if (n != 0) :
        cur_canvas.bind("<ButtonRelease-1>", lambda event: draw(event, n, cur_canvas, size_pen,pen_color))
    else:
        cur_canvas.bind("<B1-Motion>", lambda event: draw(event, n, cur_canvas, size_pen,pen_color))



# DRAG-MOVE-DROP 
selected_item = None  

def on_select(event, canvas: Canvas):
    global selected_item, move_item
    # Lấy item gần nhất tại vị trí click, find_overlapping return lst ID, gettags return tuple tags
    items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if items:
        selected_item = items[-1]  # Lấy ID item trên cùng (cuối danh sách)
        move_item = canvas.gettags(selected_item)[0]
        print(f"item's tags selecting : {move_item}")
    else:
        selected_item = None
        move_item = "all" # move all item when click at empty space


prev_x, prev_y = 0, 0  # lưu vị trí chuột trước đó

def set_prev(event):  # khởi tạo vị trí ban đầu của chuột
    global prev_x, prev_y
    prev_x, prev_y = event.x, event.y

def on_drag(event, canvas: Canvas):
    global prev_x, prev_y, move_item
    
    if move_item:
        dx = event.x - prev_x
        dy = event.y - prev_y
        canvas.move(move_item, dx, dy) # move(tags:str|ID:int, x, y)
    prev_x, prev_y = event.x, event.y

def setup_move_item(cur_canvas:Canvas):
    cur_canvas.unbind("<B1-Motion>")
    cur_canvas.unbind("<ButtonRelease-1>")
    cur_canvas.bind("<Button-1>", lambda event: [on_select(event, cur_canvas), set_prev(event)])
    cur_canvas.bind("<B1-Motion>", lambda event: on_drag(event, cur_canvas))






