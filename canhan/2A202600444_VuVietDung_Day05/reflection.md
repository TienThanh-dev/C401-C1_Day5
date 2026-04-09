# Individual reflection — Vũ Việt Dũng (2A202600444)

## 1. Role
Developer (Code). Phụ trách xây dựng giao diện tổng thể, luồng nạp dữ liệu (ingest) và triển khai ứng dụng (Streamlit).

## 2. Đóng góp cụ thể
- Phát triển giao diện người dùng (UI) bằng Streamlit (`streamlit.py`), tích hợp hiển thị Markdown và highlight trích dẫn nguồn văn bản trực quan.
- Viết kịch bản xử lý dữ liệu đầu vào (`ingest.py`), biến đổi các tệp chính sách (txt) của XanhSM vào hệ thống Knowledge Graph-enhanced RAG (LightRAG).
- Migrate ứng dụng và setup file cấu hình để deploy lên môi trường Vercel.

## 3. SPEC mạnh/yếu
- **Mạnh nhất:** Trải nghiệm xác minh thông tin (Verifiability) — UI cho phép bôi vàng/trích dẫn chính xác đoạn văn bản gốc trong policy, giải quyết trực tiếp pain point "thiếu minh bạch" giúp tài xế tin tưởng hơn.
- **Yếu nhất:** Xử lý độ trễ (Latency/Performance) — Vì dùng LightRAG sinh đồ thị tri thức và query qua LLM nên thời gian phản hồi chưa tối ưu hoàn toàn cho mobile network yếu. Cần bổ sung cơ chế caching hoặc streaming respose rõ ràng hơn trong Spec kỹ thuật.

## 4. Đóng góp khác
- Trực tiếp dùng Gemini để prompt sinh ra các base code cho giao diện UI, tiết kiệm rất nhiều giờ code tay.
- Debug và fix các lỗi kết nối giữa kết quả trả về của RAG engine với UI (lỗi hiển thị source document back-to-front).

## 5. Điều học được
Trước hackathon, tôi thường nghĩ UI chỉ là vẽ nút bấm. Sau khi làm với AI, tôi nhận ra UI/UX của AI product (như chatbot) phần lớn nằm ở cách "hiển thị sự tin cậy" — ví dụ việc highlight đoạn text đúng chỗ quan trọng hơn là thêm nhiều animation thừa. Ngoài ra, tôi cũng hiểu sâu hơn quy trình setup Graph RAG.

## 6. Nếu làm lại
Sẽ dành thời gian setup pipeline deploy (Vercel) từ sớm hơn thay vì để đến sát giờ nộp bài. Lúc deploy dính nhiều lỗi môi trường Python/Streamlit mất thời gian cấu hình lại `requirements.txt` và `vercel.json`. Gắn caching ngay từ đầu để test nhanh hơn.

## 7. AI giúp gì / AI sai gì
- **Giúp:** Sử dụng Gemini để viết các đoạn code UI Streamlit cực kỳ nhanh chóng. AI cũng giúp viết file cấu hình deploy (Vercel) và fix lỗi syntax.
- **Sai/mislead:** AI nhiều lúc tự bịa ra những thư viện hoặc hàm không có thật/không tương thích trong phiên bản Streamlit hoặc LightRAG mới nhất. Gây ra một số lỗi "Mixed content" hay "Dependency mismatch" làm mất thời gian gỡ rắc rối. Bài học: AI sinh code nhanh nhưng lúc tích hợp (integration) vẫn phải tự chủ động review từng dòng.
