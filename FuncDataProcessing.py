import json
from tkinter import *
# data processing from data_tags.json
# r"C:\Users\Lenovo\Desktop\Nhatnam\WorkSpace\HelloPython\HelloTkinter\ProjectTkinter\WhiteBoardVer2\data_tags.json"

def Read(RawfilePath:str) -> list:
    with open(RawfilePath,mode="r") as f:
        data_tag = json.load(f)
    return data_tag

def Write(RawfilePath:str,data):
    with open(RawfilePath,mode="w") as f:
        json.dump(data,f,indent=4)

def AddNewData(RawFilePath:str,AddedData,Index,AddAtIdx = None):
    cur_data = Read(RawFilePath)
    if AddAtIdx != None: # này là thêm dữ liệu vào list con, như là thêm tọa độ hay thêm tên
        cur_data[Index][AddAtIdx].append(AddedData)
    else: # này là thêm id của một object mới hoàn toàn
        cur_data[Index].append(AddedData)
    print(cur_data)
    Write(RawFilePath,data=cur_data)


def RemoveThenRewrite(RawFilePath:str,data_root:list, LstIndex:int, cur_canvas:Canvas,DeleteObject = False) : # xóa khỏi cửa sổ canvas và xóa id khỏi undo, sau đó add vô redo
    
    if data_root[LstIndex] != []:
        print(data_root[LstIndex][-1])
        if DeleteObject: # True for deleting Object
            if data_root[LstIndex][-1][0] == "erase": # nếu là object đã bị xóa thì các phần tử thuộc lst ID của object đó sẽ bị lùi lại 1 vị trí, chừa vị trí đầu cho thông tin "erase"
               Addtmp = 1
            else:
                Addtmp = 0
            cur_canvas.delete(data_root[LstIndex][-1][0+Addtmp]) # xóa  HÌNH (OBJECT ) theo tag

        deleted_tag = data_root[LstIndex].pop() # pop (cái cuối là đc) cái nào ở lst UNDO thì thêm cái đó vào lst redo VÀ NGƯỢC LẠI
        data_root[1 if LstIndex == 0 else 0].append(deleted_tag) # append again a object into the other ( lst UNDO or REDO)
        
        Write(RawFilePath,data_root)

'''Only Remove for erase button and update data for UNDO REDO'''
# chỉ xóa ở undo thôi
def RemoveFromData(FilePath,DeletedData_Tag): # Deleted data theo tags, checkDeletedData_Tag_in : kiểm tra DeletedData_Tag trong danh sách đó
    DataRoot = Read(FilePath)
    print(DataRoot)
    for i in DataRoot[0]:
        print("_______",i)
        if DeletedData_Tag in i:
            IdCopy = None
             # nhớ là thêm "erase" để biết là nó đã từng bị xóa
            IdCopy = i # move xuống cuối để khi undo vẽ lại hành động mới nhất
            if "erase" not in IdCopy: # trường hợp xóa lại chính object đó nhiều lần thì chỉ thêm 1 "erase" thôi
                IdCopy[:0]+= ["erase"]
            DataRoot[0][-1:] += [IdCopy]
            DataRoot[0].remove(i) # xóa cái ID object gốc
            break
    Write(FilePath,DataRoot)

'''Only for redo undo '''

# get each information (tag_object, TypeDraw, lst_coords, attribute_ofobject) from ID object


def GetEachInfo(data_root:list,ReadFromLst:int,erasedObject = False) -> list: # ReadFromLst:int : đọc từ danh sách UNDO thì 0 còn từ REDO thì 1
    if erasedObject: # nếu là object đã bị xóa thì các phần tử thuộc lst ID của object đó sẽ bị lùi lại 1 vị trí, chừa vị trí đầu cho thông tin "erase"
        Addtmp = 1
    else:
        Addtmp = 0
    Tag_Object = data_root[ReadFromLst][-1][0+Addtmp] # 1 → danh sách redo _ -1 : ID latest in lst redo _ 0 → tag of that object
    TypeDraw = data_root[ReadFromLst][-1][1+Addtmp] # # 1 → danh sách redo _ -1 : ID latest in lst redo _ 1 → TypeDraw of that object
    if TypeDraw != "text":
        lst_coords = data_root[ReadFromLst][-1][4+Addtmp:]  # này trả về dạng [[]]
        AttriBute_OfObject = data_root[ReadFromLst][-1][2+Addtmp:4+Addtmp] # this list contain size_pen and color
    else:
        lst_coords = data_root[ReadFromLst][-1][5+Addtmp:] # này trả về dạng [[]]
        AttriBute_OfObject = data_root[ReadFromLst][-1][2+Addtmp:5+Addtmp] # this list contain size_pen and color and paragraph
    
    return {"Tag_Object":Tag_Object,
            "TypeDraw":TypeDraw,
            "lst_coords":lst_coords,
            "AttriBute_OfObject":AttriBute_OfObject
            }