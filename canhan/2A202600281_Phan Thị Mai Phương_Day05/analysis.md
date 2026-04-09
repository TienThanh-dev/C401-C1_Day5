**Họ và tên:** Phan Thị Mai Phương 
**Mã số sinh viên:** 2A202600281

**Sản phẩm:**  
Vietnam Airlines — Chatbot NEO - Chatbot hỗ trợ khách hàng, tra cứu chuyến bay - vietnamairlines.com hoặc Zalo VNA

# Phần 1 - Khám phá:

1. Tra cứu thông tin chuyến bay, vé máy bay, tìm kiếm giá vé và thông tin hành lý (ví dụ số hành lý ký gửi).

2. Giải đáp thắc mắc liên quan đến mua vé và hành lý: 
* Thông tin mua vé: Lịch bay, chương trình ưu đãi, thanh toán, tra cứu thông tin và điều kiện hoàn/đổi vé.
* Thông tin hành lý: tiêu chuẩn hành lý miễn cước/xách tay/tính cước hay hành lý đặc biệt như thú cưng, xe đạp...
* Hướng dẫn thủ tục và các giấy tờ hoàn thành trước khi bay.

3. Với những câu hỏi chưa được trả lời sẽ được cho gặp tư vấn viên.

4. Khi dùng web - sẽ có nút Chat cùng Neo để bắt đầu chat thông qua hộp thoại.

# Phần 2 - Phân tích 4 paths:

| Path | Câu hỏi |
|------|---------|
| 1. Khi AI **đúng** | Hỏi giới hạn về hành lý ký gửi cho hạng phổ thông đến Trung Quốc, hệ thống trả lời đúng: 1 kiện 23kg/hành khách |
| 2. Khi AI **không chắc** | Hệ thống hỏi lại, yêu cầu các thông tin rõ ràng như ngày bay, giá vé, thời gian bay/hạng vé đối với hành lý |
| 3. Khi AI **sai** | Khi bị hỏi về giá vé đã ra sai so với thông tin trên web, hay cung cấp thông tin đầy đủ lại báo không có, user không biết sửa thế nào tại chỉ cho ra cùng một đáp án là không có thông tin (lặp lại nhiều lần) |
| 4. Khi user **mất tin** | Có fallback (cho cách liên lạc với bên hãng/tư vấn viên) |

- Path sản phẩm xử lý tốt nhất: khi user **mất tin**, vì duy nhất có cách giải quyết hợp lý, đảm bảo
- Path yếu nhất hoặc không tồn tại: Khi AI **sai**, bot gần như bất lực và về sau chỉ lặp đi lặp lại câu trả lời không có thông tin
- Kỳ vọng từ marketing khớp không thực tế: vì ngay thông tin chuyến bay đã không thể nào trả lời - mà đây lại là thông tin quan trọng nhất đối với khách hàng muốn được tư vấn mua vé, gần như AI không xử lý được chút task nào ngoại trừ mấy cái đơn giản, đều phải làm thủ công hoặc với con người

# Phần 3 - "Sketch làm tốt hơn":
Path yếu nhất: Khi AI **sai**
1. **As-is**: User hỏi chuyến bay, cung cấp thông tin đầy đủ (hạng, thời gian khởi hành, điểm đến) -> AI đi tìm -> AI trả: "Hiện chưa có thông tin"/đưa thông tin sai lệch + fallback (thông tin liên lạc của hãng)
* *Điểm gãy*:

Sau khi sử dụng để hỏi nhiều, mất niềm tin về thông tin giá vé chuyến bay

Không suggest phương pháp nào để tự tra cứu lại

Sau nhiều lần sai, trả lời câu giống nhau liên tục

2. **To-be**: User hỏi chuyến bay, cung cấp thông tin đầy đủ -> AI đi tìm -> AI trả theo hai hướng: "Hiện tại chưa tìm thấy chuyến bay phù hợp" và offer thông tin và cách để tra cứu /Show thông tin chuyến bay
* *Thêm*: 

Tra cứu ra được thông tin

Nêu thêm cách để tra cứu nếu AI không tìm thấy
* *Đổi/bỏ*:
Sau nhiều lần hỏi, các câu trả lời lặp đi lặp lại - phải cải thiện