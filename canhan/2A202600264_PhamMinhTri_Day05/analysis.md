# UX exercise — Vietnam Airlines — Chatbot NEO

## Sản phẩm: Vietnam Airlines — Chatbot NEO

## 4 paths

### 1. AI đúng
- User hỏi: "Hành lý được ký gửi bao nhiêu kg?" → NEO đưa ra thông tin hành lý ký gửi theo từng hạng vé và chuyến bay
- User thấy tag đúng, không cần làm gì thêm
- UI: hiện tag + icon category, không hỏi confirm

### 2. AI không chắc
- User yêu cầu "Hiển thị tất cả các chuyến bay Hà Nội - Đà Nẵng" → NEO không liệt kê danh sách chuyến bay trực tiếp mà phải hỏi lại bằng các nút bấm lựa chọn tra cứu.
- UI: không hiện gợi ý nào
- Vấn đề: không có cơ chế xem danh sách các chuyến bay

### 3. AI sai
- User muốn đặt vé → NEO đưa ra 2 lựa chọn không liên quan là "Tra cứu theo Mã đặt chỗ/Số vé" và "Tra cứu theo số hiệu chuyến bay"
- UI: không hiện gợi ý nào, user phải tự vào tìm kiếm
- Vấn đề: không trả lời đúng câu hỏi

### 4. User mất niềm tin
- Sau nhiều trả lời sai, user không tin tưởng nữa mà tự tìm kiếm
- Có exit: có nút gặp tư vấn viên, có email và hotline ở cuối
- Có fallback gặp tư vấn viên nhưng phản hồi rất lâu 

## Path yếu nhất: Path 3
- Khi AI sai, recovery flow mất quá nhiều bước
- Không có feedback loop rõ — user sửa nhưng không biết AI có học không
- Đã có fallback/exit cho user mất niềm tin nhưng thời gian phản hồi rất lâu

## Gap marketing vs thực tế
- Marketing: Được giới thiệu là "Trợ lý ảo thông minh", sử dụng AI tiên tiến để hiểu ý định khách hàng và tương tác tự động như người thật.
- Thực tế: NEO hoạt động tốt nhất dựa trên các kịch bản có sẵn. Khi người dùng nhập văn bản tự do phức tạp, NEO đôi khi không hiểu đúng ngữ cảnh hoặc trả về câu trả lời chung chung. Hãng cũng phải đưa ra lời khuyên: "Hãy hỏi câu hỏi ngắn, rõ ràng" để NEO có thể hiểu tốt nhất.
- Gap lớn nhất: marketing không nói về khi AI sai — user kỳ vọng 100% chính xác

## Sketch
(Ảnh đính kèm: sketch.jpg)
- As-is: User hỏi → AI nhận diện sai → Kết quả không liên quan → User bế tắc → User phải tự tìm thủ công (Exit) → User mất niềm tin.
- To-be: User hỏi → AI nhận diện (độ tin cậy thấp) → Hiện gợi ý: "Ý bạn là đặt vé hay tra cứu?" → User chọn "Đặt vé" → AI ghi nhận lỗi & sửa kết quả