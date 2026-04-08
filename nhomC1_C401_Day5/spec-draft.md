# SPEC — AI Product Hackathon

**Nhóm:** C401_C1
**Track:** XanhSM

**Problem statement:** Tài xế XanhSM gặp khó khăn trong việc tra cứu các chính sách thưởng/phạt phức tạp từ các tệp văn bản dài, dẫn đến việc nắm bắt thông tin sai lệch và gây quá tải cho tổng đài hỗ trợ; AI giúp giải đáp tức thì các quy định nội bộ thông qua hội thoại tự nhiên và **trích dẫn chính xác nguồn văn bản**.

---

## 1. AI Product Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi** | User nào? Pain gì? AI giải gì? | Khi AI sai thì sao? User sửa bằng cách nào? | Cost/latency bao nhiêu? Risk chính? |
| **Trả lời** | Tài xế XanhSM ngại đọc thông báo dài; AI tóm tắt chính sách thưởng/phạt và quy trình vận hành theo yêu cầu. | Highlight trực tiếp đoạn văn bản gốc trong tài liệu PDF/Thông báo; Trích dẫn số văn bản; User có nút "Xem văn bản gốc". | ~$0.015/request; Latency <1.5s; Risk: AI nhầm lẫn giữa các mốc thời gian của chính sách cũ và mới. |

**Automation hay augmentation?:** **Augmentation**

**Justify:** Augmentation — AI đóng vai trò trợ lý thông tin; tài xế tham khảo để thực hiện đúng quy trình, mọi quyết định khiếu nại cuối cùng vẫn qua bộ phận quản lý.

**Learning signal:**
1. **User correction đi vào đâu?** Nút phản hồi "Thích/Không thích" (Thumbs up/down) sau mỗi câu trả lời và ghi chú chỉnh sửa từ đội ngũ admin nội bộ.
2. **Product thu signal gì để biết tốt lên hay tệ đi?** Tỷ lệ câu hỏi được giải quyết ngay (Self-service rate) và số lượng cuộc gọi hỏi về chính sách lên hotline giảm xuống.
3. **Data thuộc loại nào?** Domain-specific, Real-time, Human-judgment.
**Có marginal value không?** Có, model được tối ưu để hiểu các thuật ngữ chuyên môn như "cuốc tối thiểu", "điểm tin cậy", "tỷ lệ chấp nhận đơn".

---

## 2. User Stories — 4 paths

### Feature: Policy Assistant (Trợ lý Chính sách Tài xế)

**Trigger:** Tài xế gửi text/voice: "Mức thưởng cho 10 chuyến hoàn thành trong khu vực nội thành hôm nay là bao nhiêu?"

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| Happy - AI đúng, tự tin | User thấy gì? Flow kết thúc ra sao? | AI liệt kê chi tiết mức thưởng hiện tại. **Highlight đoạn văn bản gốc** đính kèm phía dưới câu trả lời. |
| Low-confidence - AI không chắc | System báo "không chắc" bằng cách nào? User quyết thế nào? | AI hiển thị: "Có 2 chính sách thưởng tại Hà Nội và TP.HCM, anh đang hoạt động ở khu vực nào ạ?" |
| Failure - AI sai | User biết AI sai bằng cách nào? Recover ra sao? | Tài xế thấy phần **Highlight văn bản gốc** không liên quan đến câu trả lời của AI → Nhấn nút "Báo cáo sai". |
| Correction - user sửa | User sửa bằng cách nào? Data đó đi vào đâu? | User chọn "Chưa hài lòng" → Hệ thống lưu log câu hỏi và đoạn trích dẫn bị sai vào kho dữ liệu tinh chỉnh cho admin. |

---

## 3. Eval metrics + threshold

**Optimize precision hay recall?** **Precision**
**Tại sao?** Thông tin về quyền lợi tài chính cần chính xác tuyệt đối. Thà AI báo "Tôi chưa cập nhật thông tin này" còn hơn trả lời sai gây thiệt hại cho tài xế.

| Metric | Threshold | Red flag (dừng khi) |
|--------|-----------|---------------------|
| Độ chính xác trả lời chính sách | ≥98% | <90% |
| Tỷ lệ trích dẫn & Highlight đúng nguồn | 100% | <98% |
| Tỷ lệ tài xế hài lòng | ≥85% | <70% trong 3 ngày liên tiếp |

---

## 4. Top 3 failure modes

| # | Trigger | Hậu quả | Mitigation |
|---|---------|---------|------------|
| 1 | Văn bản chính sách mới đè lên cái cũ | AI nhầm lẫn và đưa thông tin cũ cho tài xế | Gắn nhãn "Hết hiệu lực" cho tài liệu cũ; AI ưu tiên highlight văn bản có ngày ban hành mới nhất. |
| 2 | Văn bản gốc trình bày dạng bảng phức tạp | AI trích dẫn (highlight) bị đứt đoạn hoặc thiếu hàng/cột | Sử dụng công nghệ Document AI để OCR và giữ nguyên cấu trúc bảng khi highlight. |
| 3 | Tài xế dùng từ lóng hoặc từ địa phương | AI không hiểu ngữ cảnh và trả lời lạc đề | Xây dựng bộ từ điển thuật ngữ tài xế thường dùng nạp vào Model. |

---

## 5. ROI 3 kịch bản

|   | Conservative | Realistic | Optimistic |
|---|-------------|-----------|------------|
| **Assumption** | 10% tài xế dùng, 70% hài lòng | 40% tài xế dùng, 85% hài lòng | 80% tài xế dùng, thay thế hoàn toàn FAQ |
| **Benefit** | Giảm 10% cuộc gọi support | Giảm 40% tải hotline; Tài xế ít vi phạm | Giảm 80% support; Tăng retention tài xế |

**Kill criteria:** Dừng dự án nếu tỷ lệ khiếu nại do AI trả lời sai/highlight sai văn bản gốc tăng đột biến (>5%).

---

## 6. Mini AI spec

**XanhSM Policy Assistant** là một chatbot thông minh dựa trên công nghệ LLM và RAG (Retrieval-Augmented Generation).
- **Mục tiêu:** Trở thành "cuốn sổ tay số" luôn sẵn sàng hỗ trợ tài xế giải đáp mọi thắc mắc về quy định vận hành một cách chính xác nhất.
- **Cơ chế:** Khi nhận câu hỏi, hệ thống thực hiện tìm kiếm ngữ nghĩa (Semantic Search) trong kho dữ liệu văn bản pháp lý nội bộ. AI không chỉ tóm tắt mà còn **tự động cắt lớp (chunking) và Highlight đoạn văn bản gốc** chứa thông tin đó để tài xế đối chiếu trực tiếp.
- **Flywheel dữ liệu:** Mọi phản hồi từ tài xế sẽ giúp admin lọc ra các văn bản gây nhầm lẫn, từ đó cập nhật dữ liệu đầu vào hoặc tinh chỉnh lại prompt cho AI.
- **Cam kết:** Luôn đi kèm bằng chứng trực quan (Highlight văn bản gốc) để xây dựng niềm tin (Trust) tuyệt đối với tài xế và đảm bảo tính minh bạch.