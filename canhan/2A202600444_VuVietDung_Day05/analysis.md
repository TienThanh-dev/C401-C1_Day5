# UX exercise — MoMo Moni AI

## Sản phẩm: MoMo — Moni AI Assistant (phân loại chi tiêu)

---

## 4 paths

### 1. AI đúng

* User thanh toán tiền điện 1 triệu qua MoMo

* Moni tự động phân loại “Hóa đơn”

* User thấy hợp lý, không cần chỉnh

Thực tế:

* Các giao dịch có category rõ như điện, nước, internet được MoMo map sẵn → độ chính xác cao

UI:

* Hiển thị category ngay trong transaction
* Không yêu cầu confirm

---

### 2. AI không chắc

* User chuyển khoản 500k cho bạn với nội dung “ăn uống tuần trước”
* Moni không phân loại hoặc để “Khác”

Thực tế:

* Giao dịch P2P (chuyển tiền) thiếu merchant và metadata rõ → hệ thống khó phân loại chính xác

UI hiện tại:

* Không có gợi ý
* Không hỏi lại user

Vấn đề:

* Bỏ lỡ cơ hội thu thập intent
* User phải tự nhớ để phân loại sau

---

### 3. AI sai

* User chuyển 2 triệu cho người thân với nội dung “đóng học phí”
* Moni phân loại “Chuyển tiền” thay vì “Giáo dục”

Thực tế:

* AI ưu tiên loại giao dịch (transfer) hơn nội dung semantic (mục đích)
* Không tận dụng tốt text note

Flow sửa hiện tại:

* Vào lịch sử giao dịch
* Chọn giao dịch
* Đổi category

Vấn đề:

* Nhiều bước
* Không có gợi ý sửa nhanh ngay tại thời điểm giao dịch
* Không rõ hệ thống có ghi nhớ hay không

---

### 4. User mất niềm tin

* User thường xuyên:

  * chuyển tiền
  * chia tiền
  * thanh toán hộ

→ Moni không phân loại đúng phần lớn giao dịch

Hệ quả:

* Báo cáo chi tiêu sai lệch
* User không còn dùng dashboard phân tích

Thực tế:

* Nhóm user có nhiều giao dịch “không chuẩn merchant” là nhóm bị fail nhiều nhất

Vấn đề:

* Không có cơ chế:

  * ưu tiên user-defined logic
  * hoặc manual override mặc định

---

## Path yếu nhất: Path 3 + 4

* Sai ở các giao dịch phổ biến (chuyển tiền)
* Flow sửa không thuận tiện
* Không có learning feedback visible

---

## Gap marketing vs thực tế

Marketing:

* “AI tự động phân loại chi tiêu thông minh”

Thực tế:

* Hoạt động tốt với:

  * hóa đơn
  * dịch vụ có merchant

* Hoạt động kém với:

  * chuyển tiền
  * giao dịch có mục đích cá nhân

Nguyên nhân:

* AI phân loại theo loại giao dịch
* User kỳ vọng theo mục đích sử dụng tiền

---

## Sketch

As-is:

* Giao dịch → auto-tag theo type → user xem → nếu sai phải vào sửa

To-be:

* Giao dịch → auto-tag + đọc nội dung chuyển tiền
* Nếu phát hiện keyword (học phí, ăn uống, tiền nhà):

  * gợi ý category ngay
* User chọn nhanh → hệ thống lưu preference


