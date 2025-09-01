from tkinter import *
from FuncDataProcessing import *

'''ALL GLOBAL variable'''
tags_id = "TAG_1_" # không đặt chuỗi số thuần làm tag như "0" "1" vì python sẽ hiểu nhầm là ID | khi đó mình chỉ có thể di chuyển một đoạn của nét vẽ tự do mặc do full đoạn đều có cùng tag
selected_id_item = None
selected_tag_item = None
object_id = None
start_x, start_y = None, None
prev_x, prev_y = None , None
''' file data cần xử lý để UNDO-REDO '''
filePath = r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoardVer2\data_id.json"

''' xử lý click '''
def on_click(event): # 1 for draw, 0 for erase ( erase not need update tag)
    global start_x, start_y
    global tags_id 
    #update tag một lần duy nhất khi click
    tags_id += "1_"

    # add TAG:list to DATA_id for "BUTTON UNDO" processing
    AddNewData(filePath,[tags_id],0) # Add tag
    
    # khởi tạo lại vị trí, theo mouse cursor tại vị trí click mà event cập nhật
    start_x, start_y = event.x,event.y
    # print("Bạn đã click tại:",event.x, event.y)

''' xử lý kéo '''
def handle_drag(event, cur_canvas: Canvas) : # just for debuggingg
    # print("Đang kéo tại:", event.x, event.y) 
    pass
    

'''xử lý enter, để done cái text and chuyển nó sang hiển thị text'''
'''DRAW'''
def handle_enter(event,entry_text):
    # print("Bạn đã enter khi trỏ đang ở vị trí: ",event.x, event.y)
    entry_text.destroy()


# THIS FUNC JUST FOR UNDO (NOT FOR REDO) ( function REDO CAN not REUSUSE THIS FUNCTION draw)
def draw(event,n:int,cur_canvas:Canvas,size_pen,pen_color = "black"): # 1 -> line | 2 -> rectangle | 3 -> elipse, oval |
    global start_x, start_y
    cur_canvas.config(cursor="circle") # config display of Mouse cursor

    # print(f"TAgs_id hiện tại {tags_id}, {type(tags_id)}")
    # for item in cur_canvas.find_all():
    #     print("Item:", item, "-> tags:", cur_canvas.gettags(item))

    # Nếu typeName đó có trong data_id jsson rồi thì ko add lại typeDraw, typeDraw chỉ add 1 lần duy nhất
    TypeDraw = "line" if (n == 1) else ("rectangle" if (n == 2) else ("oval" if (n == 3) else ("freeHand" if (n == 0) else "text")))
    cur_data = Read(filePath)[0][-1] 
    if  TypeDraw not in cur_data :
        AddNewData(filePath,TypeDraw,0,-1) # add NameShape into id
        AddNewData(filePath,size_pen,0,-1) # add size_pen into id
        AddNewData(filePath,pen_color,0,-1) # add color into id

    if (n == 1):
        # ID
        object_id = cur_canvas.create_line(start_x,start_y,event.x,event.y,width=size_pen,smooth=True,fill=pen_color,tags=tags_id)
    elif (n == 2):
        # ID
        object_id = cur_canvas.create_rectangle(start_x,start_y,event.x,event.y,width=size_pen,outline = pen_color,tags=tags_id)
    elif (n == 3):
        # ID
        object_id = cur_canvas.create_oval(start_x,start_y,event.x,event.y,width=size_pen,outline = pen_color,tags=tags_id)
    elif (n == 0): # freehand
        x, y = event.x, event.y  
        # ID          
        object_id = cur_canvas.create_line(start_x,start_y,x,y,width=size_pen,smooth=True, fill=pen_color,tags=tags_id)
        start_x,start_y = x, y

    elif (n == 4):
        entry_text = Entry(cur_canvas,width=size_pen+2,font=("Times New Roman",size_pen))
        entry_text.place(x = start_x, y = start_y)
        entry_text.focus_set()

        def on_enter_key(event):
            global object_id 
            text_value = entry_text.get()
            if text_value.strip() != "":
                # ID
                object_id = cur_canvas.create_text(start_x, start_y, fill=pen_color, font=("Times New Roman", size_pen), text=text_value,tags=tags_id)
            
            entry_text.destroy()
            if text_value != None:
                AddNewData(filePath,f"{text_value}",0,-1) # add paragraph into ID
                AddNewData(filePath,[start_x,start_y],0,-1)
        
        entry_text.bind("<Return>", on_enter_key)
        
    if TypeDraw != "text":
        AddNewData(filePath,cur_canvas.coords(object_id),0,-1) # add coordinate into ID
            
''' SET UP DRAW '''
def setup_draw_pen(n:int,cur_canvas:Canvas,size_pen, pen_color):
    cur_canvas.unbind("<B1-Motion>")
    cur_canvas.unbind("<ButtonRelease-1>")
    cur_canvas.bind("<Button-1>", on_click)

    if (n != 0) :
        cur_canvas.bind("<ButtonRelease-1>", lambda event: draw(event, n, cur_canvas, size_pen,pen_color))
    else:
        cur_canvas.bind("<B1-Motion>", lambda event: draw(event, n, cur_canvas, size_pen,pen_color))

'''SET UP ALLL ERASE_FUNc'''

'''Delete Founded Object'''
def DeleteFoundedObject(event,cur_canvas:Canvas) : # xóa object tìm được theo tag ha
    items = cur_canvas.find_overlapping(event.x,event.y,event.x,event.y)
    if items:
        selected_id_item = items[-1]  # Lấy ID item trên cùng (cuối danh sách)
        selected_tag_item = cur_canvas.gettags(selected_id_item)[0]
        RemoveFromData(filePath,selected_tag_item)
        cur_canvas.delete(selected_tag_item)

'''ERASE'''
def Erase(cur_canvas:Canvas):
    cur_canvas.unbind("<B1-Motion>")
    cur_canvas.unbind("<Button-1>")
    cur_canvas.unbind("<ButtonRelease-1>")
    cur_canvas.bind("<B1-Motion>",lambda event: DeleteFoundedObject(event,cur_canvas))
    


''' DRAG-MOVE-DROP ''' 
selected_id_item = None  

def on_select(event, canvas: Canvas): 
    global selected_id_item, selected_tag_item
    # Lấy item gần nhất tại vị trí click, find_overlapping return lst ID, gettags return tuple tags
    items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if items:
        selected_id_item = items[-1]  # Lấy ID item trên cùng (cuối danh sách)
        selected_tag_item = canvas.gettags(selected_id_item)[0]
        print(f"item's tags selecting: {selected_tag_item}") 
    else:
        selected_id_item = None
        selected_tag_item = "all" # move all item when click at empty space



prev_x, prev_y = 0, 0  # lưu vị trí chuột trước đó

''' SET UP FUNCTION '''
def set_prev(event):  # khởi tạo vị trí ban đầu của chuột
    global prev_x, prev_y
    prev_x, prev_y = event.x, event.y

def on_drag(event, canvas: Canvas):
    global prev_x, prev_y, selected_tag_item
    
    if selected_tag_item:
        dx = event.x - prev_x
        dy = event.y - prev_y
        canvas.move(selected_tag_item, dx, dy) # move(tags:str|ID:int, x, y)
    prev_x, prev_y = event.x, event.y

''' SET UP MOVE '''
def setup_move_item(cur_canvas:Canvas):
    cur_canvas.config(cursor="fleur")
    cur_canvas.unbind("<B1-Motion>")
    cur_canvas.unbind("<Button-1>")
    cur_canvas.unbind("<ButtonRelease-1>")
    cur_canvas.bind("<Button-1>", lambda event: [on_select(event, cur_canvas), set_prev(event)])
    cur_canvas.bind("<B1-Motion>", lambda event: on_drag(event, cur_canvas))



''' THIS FUNC JUST FOR REDO '''
def ReDraw(cur_canvas:Canvas,TypeDraw: str,coords:list,AttributeOfObject:list, Tag_Object:str): # n : type to draw
    size_pen = AttributeOfObject[0]
    pen_color = AttributeOfObject[1]
    print("Thỏa gốc")
    print(TypeDraw)
    if TypeDraw != "freeHand" and TypeDraw != "text":
        coords = coords[0] # vì coords truyền vô ở dạng [[]], còn ở dạng [[],..,[]] khi là danh sách tọa độ của vẽ tự do
        # ép sang int
        coords = list(map(int,coords))
        # print(type(coords))
        # print(coords)

        x1, y1 = coords[0], coords[1]
        x2, y2 = coords[2], coords[3]

        if (TypeDraw == "line"):
            # ID
            object_id = cur_canvas.create_line(x1,y1,x2,y2,width=size_pen,smooth=True,fill=pen_color,tags=Tag_Object)
        elif (TypeDraw == "rectangle"):
            # ID
            object_id = cur_canvas.create_rectangle(x1,y1,x2,y2,width=size_pen,outline = pen_color,tags=Tag_Object)
        elif (TypeDraw == "oval"):
            # ID
            object_id = cur_canvas.create_oval(x1,y1,x2,y2,width=size_pen,outline = pen_color,tags=Tag_Object)

    elif TypeDraw == "freeHand":
        # vì coords truyền vô ở dạng [[]], còn ở dạng [[],..,[]] khi là danh sách tọa độ của vẽ tự do
        
        print(type(coords))
        print(coords," ___-")
        print("Thỏa")
        for i in coords:
            # ép sang int
            i = list(map(int,i))
            
            x1, y1 = i[0], i[1]
            x2, y2 = i[2], i[3]
            cur_canvas.create_line(x1,y1,x2,y2,width=size_pen,smooth=True,fill=pen_color,tags=Tag_Object)
    elif TypeDraw == "text":
        coords = coords[0] # vì coords truyền vô ở dạng [[]], còn ở dạng [[],..,[]] khi là danh sách tọa độ của vẽ tự do
        # ép sang int
        coords = list(map(int,coords))
        x1, y1 = coords[0], coords[1]
        print(AttributeOfObject)
        print(AttributeOfObject[2])
        object_id = cur_canvas.create_text(x1, y1,text=AttributeOfObject[2], fill=pen_color, font=("Times New Roman", size_pen), tags=tags_id)


''' SET UP UNDO REDO FUNCTION ''' 
def undo_redo(cur_canvas:Canvas, n : int): # n == 1 -> undo | n == 2 -> redo
    cur_canvas.unbind("<B1-Motion>")
    cur_canvas.unbind("<Button-1>")
    cur_canvas.unbind("<ButtonRelease-1>")
    data_id = Read(filePath) # data_root from data_id.json
    SeparateID = None # chứa các phần đã đc chia sẵn để truyền đối số vào hàm Redraw

    if n == 0 and data_id[0] != []: # execute UNDO
        print("OK UNDO")

        # khôi phục nếu "erase"
        if "erase" in data_id[0][-1]:# là object bị xóa thì thêm erased = True 
            SeparateID = GetEachInfo(data_root=data_id,ReadFromLst=0,erasedObject=True)
            ReDraw(cur_canvas,TypeDraw=SeparateID["TypeDraw"],coords=SeparateID["lst_coords"],AttributeOfObject=SeparateID["AttriBute_OfObject"],Tag_Object=SeparateID["Tag_Object"])
            RemoveThenRewrite(RawFilePath=filePath,data_root=data_id,LstIndex=0,cur_canvas=cur_canvas)
        # ngc lại xóa
        else: # ngược lại k cần thêm
            SeparateID = GetEachInfo(data_root=data_id,ReadFromLst=0)
        # xóa khỏi ds UNDO xong ghi lại dữ liệu mới vào  danh sách REDO json
            RemoveThenRewrite(RawFilePath=filePath,data_root=data_id,LstIndex=0,cur_canvas=cur_canvas,DeleteObject=True)

    elif data_id[1] != [] and len(data_id[1][-1]) == 1: # xử lí một số trường hợp lưu object nhưng mà k lưu vị trí ( tức chẳng vẽ gì)| nhưng có lưu tag nên ta xóa luôn
        cur_canvas.delete(data_id[1][-1][0] )

    elif n == 1 and data_id[1] != []  : # execute REDO
        
        # print(SeparateID["lst_coords"])
        # Khi ta undo object bị xóa (ở danh sách undo sẽ thực hiện vẽ lại và xóa ID của object này rồi chuyển qua cho danh sách REDO)
        # nếu nhấn REDO ta thực hiện ngược lại, gặp "erase" sẽ xóa
        if "erase" in data_id[1][-1]:# là object bị xóa thì thêm erased = True 
            SeparateID = GetEachInfo(data_root=data_id,ReadFromLst=1,erasedObject=True)
            # xóa khỏi ds REDO xong ghi lại dữ liệu mới vào  danh sách UNDO json
            RemoveThenRewrite(RawFilePath=filePath,data_root=data_id,LstIndex=1,cur_canvas=cur_canvas,DeleteObject=True)

        # ngược lại khôi phục
        else: # ngược lại k cần thêm
            SeparateID = GetEachInfo(data_root=data_id,ReadFromLst=1)
            ReDraw(cur_canvas,TypeDraw=SeparateID["TypeDraw"],coords=SeparateID["lst_coords"],AttributeOfObject=SeparateID["AttriBute_OfObject"],Tag_Object=SeparateID["Tag_Object"])
            # xóa khỏi ds REDO xong ghi lại dữ liệu mới vào  danh sách UNDO json
            RemoveThenRewrite(RawFilePath=filePath,data_root=data_id,LstIndex=1,cur_canvas=cur_canvas)       
        

'''SET UP ZOOM-SHRINK FUNCTION'''
def zoom_shrink(cur_canvas:Canvas, choice:str, cur_size: int): # "zoom","shrink"
        if choice == "zoom":
            cur_canvas.scale("all",0,0,2,2)
        elif choice == "shrink":
            cur_canvas.scale("all",0,0,0.5,0.5)
