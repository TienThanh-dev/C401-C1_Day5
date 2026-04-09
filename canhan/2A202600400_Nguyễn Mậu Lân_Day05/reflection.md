# Individual reflection - Nguyễn Mậu Lân (2A202600400)

## 1. Role
**SPEC + Demo** Chịu trách nhiệm chính trong viêc thiết kế AI Product Canvas, thiết lập tiêu chuẩn kỹ thuật (SPEC).

## 2. Đóng góp cụ thể
* **Xây dựng bộ khung sản phẩm:** Thiết kế AI Product Canvas (Value-Trust-Feasibility) và 4 User Stories chi tiết làm kim chỉ nam cho cả nhóm.
* **Hỗ trợ kỹ thuật (Technical Alignment):** hỗ trơ hiện thực hóa các **Failure Modes**. Thay vì chỉ nêu rủi ro, đề xuất các phương án xử lý (Mitigation) để Dev dễ dàng cài đặt logic retry/fallback.
* **Điều phối liên chức năng:** Tổng hợp feedback từ các buổi chạy thử để chuyển hóa thành Action Items cụ thể cho từng thành viên

## 3. SPEC mạnh/yếu
* **Mạnh nhất:** Cơ chế tạo dựng niềm tin (**Trust mechanism**) rõ ràng, giúp người dùng hiểu rõ giới hạn của AI, từ đó tăng tính minh bạch cho sản phẩm.
* **Yếu nhất:** Giả định về độ trễ (**Latency assumption**) còn cảm tính, chưa bóc tách cụ thể thời gian phản hồi của từng module (RAG, LLM, API).

## 4. Đóng góp khác
* Biên soạn mẫu AI Product Canvas chung cho cả nhóm.
* Hỗ trợ demo, phản biện sản phẩm

## 5. Điều học được
**SPEC không phải là bản tường thuật, mà là một bản hợp đồng.** Nhận ra SPEC phải đảm bảo 4 yếu tố: 
* **Dễ hiểu:** Dựa trên User Story thực tế.
* **Dễ kiểm tra:** Có Failure modes và hướng xử lý rõ ràng.
* **Khả thi:** Các giả định về Latency/Cost phải sát với thực tế Engineering.
* **Trackable:** Eval metrics rõ ràng để biết khi nào sản phẩm đạt yêu cầu.

## 6. Nếu làm lại
* **Validate sớm:** Sẽ thảo luận trực tiếp với Dev ngay từ ngày đầu về các con số Latency thực tế thay vì tự giả định để tránh gây áp lực cho scope.
* **Visual hóa tài liệu:** Thay vì chỉ dùng văn bản, sẽ vẽ các **Sơ đồ luồng xử lý lỗi (Failure flow charts)** để Engineering dễ dàng hình dung và triển khai code chính xác hơn.

## 7. AI giúp gì / AI sai gì
* **Giúp:** Gemini + ChatGPT hỗ trợ brainstorm khung Canvas (Value-Trust-Feasibility) rất hiệu quả và nhanh chóng.
* **Sai/Mislead:** AI thường gợi ý quá nhiều tính năng (Scope creep) không phù hợp với giới hạn thời gian hackathon. Ngoài ra, AI khó nhận diện được các rủi ro mang tính "nghiệp vụ thực tế" (như độ trễ dữ liệu ảnh hưởng đến túi tiền người dùng) so với việc phân tích thủ công.