# Individual reflection — Phan Thị Mai Phương (2A202600281)

## 1. Role
Data crawler + QA/editor. Phụ trách thu thập, lọc dữ liệu đầu vào và kiểm tra, hiệu đính các tài liệu (report, spec, format).

## 2. Đóng góp cụ thể
- Crawl và lọc dataset để phục vụ cho việc test prompt (chỉ lấy thời điểm gần nhất).
- Chuẩn hoá dữ liệu đầu vào (format lại để đảm bảo consistency khi test).
- Review và chỉnh sửa các file spec/report (font, format, cách trình bày, wording) để đảm bảo tính rõ ràng và đồng nhất.

## 3. SPEC mạnh/yếu
- Mạnh nhất: tính rõ ràng và nhất quán của tài liệu — spec được chuẩn hoá giúp dễ follow.
- Yếu nhất: Ở user stories, chưa thêm fallback vào các trường hợp AI thiếu thông tin là sẽ cho cách thức liên lạc bên xử lý để được giải quyết vấn đề.

## 4. Đóng góp khác
- Verify output của chatbot bằng cách đối chiếu với policy gốc, phát hiện các câu trả lời sai hoặc thiếu.
- Giới hạn lại một số các feature không cần thiết và không đủ thời gian: như tìm quãng đường ngắn nhất cho tài xế.
- Hỗ trợ đánh giá feedback các nhóm khác.

## 5. Điều học được
Trước đây nghĩ việc crawl data và chỉnh sửa tài liệu chỉ là phần phụ, nhưng trong quá trình làm mới thấy:
Chất lượng và độ rõ ràng của tài liệu data ảnh hưởng trực tiếp đến chất lượng câu trả lời của chatbot, nhiều lỗi của AI không đến từ model mà đến từ dữ liệu đầu vào (thiếu, mơ hồ, hoặc không nhất quán). Data quality và documentation không chỉ là support, mà là nền tảng của bài toán.

## 6. Nếu làm lại
Sẽ thêm vào system prompt fallback - số/email liên lạc của bên xử lý thay vì chỉ trả lại chưa có thông tin này.
Cho thêm vào data link trích dẫn để có tính xác thực hơn (dù về sau sẽ nâng cấp lên thành highlight trên web).
Có thể sẽ thêm data cũ và gắn nhãn lại để xem chatbot có trả lời nhầm thông tin không nếu còn thời gian.

## 7. AI giúp gì / AI sai gì
- **Giúp:** Sử dụng để chuyển ảnh trên các tin tức - không phải text sang dạng text để chuẩn hóa dữ liệu.
- **Sai/mislead:** Mở ra quá nhiều tính năng thừa thãi cho ứng dụng, không cẩn thận sẽ bị ngợp và không biết nên bắt đầu từ đâu. Khi chuyển dữ liệu ảnh sang text, AI có xu hướng sửa lại format thông tin không cần thiết, làm tăng số lượng chunk, và tăng cost mỗi lần hỏi.