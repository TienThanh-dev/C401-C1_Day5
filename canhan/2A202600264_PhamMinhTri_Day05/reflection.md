# Individual reflection — Phạm Minh Trí (2A202600264)

## 1. Role
UX designer + prompt engineer. Phụ trách thiết kế flow chatbot và viết system prompt.

## 2. Đóng góp cụ thể
- Thiết kế chatbot conversation flow
- Xây dựng system prompt để định nghĩa rõ vai trò AI là trợ lý tra cứu chính sách nội bộ
- Thiết kế trust UX layer

## 3. SPEC mạnh/yếu
- Mạnh nhất: Trải nghiệm xác minh thông tin vì UI cho phép highlight trích dẫn chính xác đoạn văn bản gốc trong chính sách, giải quyết được pain point "thiếu minh bạch" giúp tài xế tin tưởng hơn.
- Yếu nhất: Xử lý độ trễ do dùng LightRAG sinh đồ thị tri thức và query qua LLM nên thời gian phản hồi chưa được tối ưu. 

## 4. Đóng góp khác
- Tạo các file data txt
- Rà soát consistency giữa SPEC, prototype và demo script

## 5. Điều học được
Một sản phẩm AI tốt không chỉ là model trả lời đúng, mà còn phải thiết kế được trust cho người dùng. Trước đây tôi thường nghĩ prompt tốt là đủ, nhưng qua hackathon tôi hiểu rằng:citation, confidence fallback,recovery flow, feedback loop mới là phần quyết định user có tiếp tục tin dùng AI hay không. Đặc biệt với domain policy nội bộ, UX còn quan trọng không kém model.

## 6. Nếu làm lại
Sẽ test prompt sớm hơn thì prompt sẽ tốt hơn nhiều.

## 7. AI giúp gì / AI sai gì
- **Giúp:** brainstorm failure modes thực tế, hỗ trợ viết nhanh system prompt base version, giúp team iterate nhiều version flow trong thời gian ngắn.
- **Sai/mislead:** đôi lúc gợi ý flow quá lý tưởng, chưa sát hành vi thật của tài xế, một số prompt suggestion thiên về chatbot FAQ chung chung, chưa đủ domain-specific