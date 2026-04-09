# Individual reflection — Vũ Tiến Thành (2A202600443)

## 1. Role
Developer (Code). Phụ trách xây dựng giao diện ban đầu, mock data để xác định những chức năng cần làm. Xây dựng RAG pipeline.

## 2. Đóng góp cụ thể
- Phát triển giao diện cơ bản với mock data.
- Viết RAG pipline sử dụng LightRAG
- Test end-to-end luồng demo
- Cùng nhóm xây dựng spec, spec draft, canvas,...

## 3. SPEC mạnh/yếu
- **Mạnh nhất:** Chọn đúng chiến lược với tài liệu chính sách nội bộ, thà không trả lời còn hơn trả lời sai và hignlight được tài liệu gốc chứng minh được câu trả lời đúng và tại sao nó đúng.
- **Yếu nhất:** RAG pipline còn miêu tả chung chung, thiếu nhiều chi tiết. Chưa có "confidence scoring" rõ ràng khiến việc đánh giá sự "không chắc" cảu AI trở nên khó khăn.

## 4. Đóng góp khác
- Xem xét các task, verify lại kết quả của các thành viên.
- Craw dữ liệu từ xanh SM
- Phản biện lại các câu hỏi phần demo.

## 5. Điều học được

Trước đó luôn code đi trước tài liệu rảo bước theo sau. Bây giờ mới học cách xác định và clear toàn bộ vấn đề và phác thảo trước khi bắt đầu xây dựng chương trình. Điều này khiến việc xây dựng trở lên dễ dàng hơn khi biết rõ bài toán cần phải giải quyết và tập trung giải quyết chứ không còn lan man ra các chức năng không cần thiết, lạc lối với UX không bám sát để phục vụ người dùng mục tiêu.

## 6. Nếu làm lại

Viết tốt hơn spec và nhận định lại bài toán và các vấn đề, dành nhiều thời gian hơn để tìm hiểu bài toán và phác thảo spec, canvas chính xác và clear hơn.

## 7. AI giúp gì / AI sai gì
- **Giúp:** Sử dụng Gemini để viết các đoạn code và xây dựng RAG pipline.
- **Sai/mislead:** AI sửa theo ý mình nhưng lại lỗi một phần nhỏ của chức năng nếu không để ý kĩ và test lại thì ko dễ phát hiện. Đáng lẽ cần đặt log nhiều và chi tiết hơn để monitor và debug dễ hơn.
