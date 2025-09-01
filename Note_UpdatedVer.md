## Đã sửa tag ID thành chuỗi thuần không phải chuỗi số thuần ( "0" "1")

> để python k nhầm lẫn giữa tags và ID, nhờ vậy có thể di chuyển cả một nét vẽ tránh một nét vẽ chung tag nhưng chỉ move được nét đứt đầu tiên

## khi click vào empty space dùng tags đặc biệt "all":

> gán move_item = all
> di chuyển full item

## Đã chuyển combobox ( select color) sang colorchooser.askcolor() để nhìn đẹp mắt hơn

## Không debug nữa nên bỏ bớt mấy cái print ở function file, cho đỡ lag khi vẽ

## Đổi icon mặc đinh góc trái của tkinter sang icon ứng dụng mình làm

* [X] Đã xong

- Lưu ý phải convert **.png** or **.jpg** sang **.ico**
- Dùng .iconbitmap(picture_path)

# JSON

- **Cấu trúc một id**

  - data_tag[0][-1] = [tag: str,NameShape,size_pen,color,[list coordinate]]
- Lưu id ( chứa tag trước) vì tag do mình khởi tạo, còn coordinate và loại hình vẽ lưu sau do nó tùy thuộc vào người dùng vẽ
- Lưu id: list ( gồm tag: string, coordinate : int)

  - Có thể nên thêm kiểu hình vào id:list ( ví dụ :type_shape : rectangle )
- file json này gồm một json[0] là danh sách lưu id cho UNDO xử lý
- file json này gồm một json[1] là danh sách lưu id cho REDO xử lý

  > Mà riêng cái entry thì phải add thêm cái nội dung của nó nữa ( ở undo)
  >

## UNDO

* [X] Đã xong

- Lưu lại id: list gồm tag, coordinate vào json[0] ( danh sách chứa các id của item đã vẽ)
- xóa cái id cuối là đc ( xóa theo id[0][0] : tag string)

## REDO

* [ ] Đã xong

- Xóa cái nào thì thêm cái id:list ( gồm tag,  coordinate) vào json[1] (danh sách chứa các id của item đã xóa)
- vẽ lại cái id cuối là đc ( vẽ theo id[1][2:len(id)] : coordinate), phải check id[1][1] là kiểu hình gì để vẽ cho đúng
  - Cần xử lý bước nhảy cho phù hợp để vẽ lại đúng vị trí, đúng tọa độ đó
  - Tận dụng lại hàm vẽ sẵn có chỉ cần vẽ theo tọa độ
- 

# 

# PHẢI TÓM TẮT LẠI CÁCH XỬ LÝ LOGIC CỦA TỪNG TÍNH NĂNG ( QUAN TRỌNG NHẤT)
