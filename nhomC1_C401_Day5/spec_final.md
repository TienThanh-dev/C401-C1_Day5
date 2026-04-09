# SPEC — AI Product Hackathon

**Nhóm:** C401_C1  
**Lĩnh vực:** XanhSM  
**Problem statement:** Tài xế XanhSM gặp khó khăn trong việc tra cứu các chính sách thưởng/phạt phức tạp từ các tệp văn bản dài, dẫn đến việc nắm bắt thông tin sai lệch và gây quá tải cho tổng đài hỗ trợ; AI giúp giải đáp tức thì thông qua hội thoại tự nhiên, thông báo chủ động, trích dẫn chính xác nguồn văn bản, hỗ trợ tính toán thu nhập thực tế và tối ưu lộ trình sạc pin.

---

## 1. AI Product Canvas

| Yếu tố | Câu hỏi | Trả lời |
| :--- | :--- | :--- |
| **Value** | User nào? Pain gì? AI giải gì? | **Tài xế XanhSM:** Ngại đọc PDF, khó tính toán mức thưởng, lo lắng về trạm sạc; **AI:** Tóm tắt chính sách qua giọng nói, chủ động nhắc mốc thưởng và **tìm trạm sạc còn trống** theo thời gian thực. |
| **Trust** | Khi AI sai thì sao? User sửa bằng cách nào? | **Cơ chế đối soát:** Highlight văn bản gốc; Trích dẫn số hiệu văn bản; Tính năng **"Speak"** đọc nguồn; Nút **"Báo cáo trạm lỗi"** để cập nhật tình trạng trụ sạc thực tế. |
| **Feasibility** | Cost/latency bao nhiêu? Risk chính? | **Vận hành:** ~$0.025/request (RAG + Voice + Math Engine + Maps API); Latency <2s; **Risk:** Dữ liệu trụ sạc/chính sách bị delay so với thực tế. |

* **Automation hay augmentation?:** Augmentation.
* **Justify:** AI đóng vai trò "Trợ lý vận hành và tài chính"; các con số cuối cùng vẫn phải đối soát với ứng dụng tài xế và trụ sạc thực tế.
* **Learning signal:** * **User correction:** Lệnh giọng nói "Sai rồi", "Đọc lại nguồn" hoặc "Trạm này hỏng rồi".
    * **Product signal:** Tỷ lệ tài xế di chuyển theo gợi ý trạm sạc; Tỷ lệ sử dụng tính năng tính toán thưởng.

---

## 2. User Stories — 4 paths

### Feature 1: Voice-to-Policy (Tra cứu chính sách rảnh tay)
**Trigger:** Tài xế nhấn nút Micro hoặc đọc từ khóa kích hoạt: *"XanhSM ơi, quy định đồng phục mới thế nào?"*

| Path | Câu hỏi thiết kế | Mô tả |
| :--- | :--- | :--- |
| **Happy Path** | User thấy gì? Flow kết thúc ra sao? | AI chuyển Voice -> Text, tra cứu RAG và **Speak** tóm tắt: "Dạ, anh cần mặc áo polo xanh, quần dài tối màu và đi giày kín mũi ạ." |
| **Low-confidence** | System báo "không chắc" bằng cách nào? | AI nói: "Em thấy có quy định riêng cho mùa hè và mùa đông, anh muốn nghe mục nào ạ?" |
| **Failure** | User biết AI sai bằng cách nào? | AI trả lời về 'thưởng' thay vì 'đồng phục'. Tài xế ra lệnh: "Hủy" hoặc "Sai rồi" để dừng AI. |
| **Correction** | User sửa bằng cách nào? | User nói: "Tôi hỏi về đồng phục cơ mà". Hệ thống ghi nhận lỗi Intent để tinh chỉnh bộ phân loại câu hỏi. |

### Feature 2: Proactive Bonus Calculator (Tính toán mốc thưởng)
**Trigger:** Hệ thống nhận diện tài xế vừa hoàn thành chuyến xe và sắp chạm mốc thưởng mới.

| Path | Câu hỏi thiết kế | Mô tả |
| :--- | :--- | :--- |
| **Happy Path** | User thấy gì? Flow kết thúc ra sao? | Card chữ lớn hiện lên: **"Còn 2 chuyến - Nhận 150k"**. AI Speak: "Cố lên anh, 2 chuyến nữa là đủ mốc thưởng ngày!" |
| **Low-confidence** | System báo "không chắc" bằng cách nào? | AI hiển thị: "Đang tính toán mốc thưởng... Vui lòng chờ 1s để đối soát dữ liệu chuyến xe mới nhất." |
| **Failure** | User biết AI sai bằng cách nào? | Tài xế thấy số tiền thưởng dự kiến thấp hơn thực tế. User bấm vào nút **"Cần đối soát"**. |
| **Correction** | User sửa bằng cách nào? | User chọn: "Thiếu chuyến đã hoàn thành". Data đẩy về Admin để kiểm tra lại pipeline đồng bộ dữ liệu. |

### Feature 3: Policy Change Alert (Thông báo chính sách mới)
**Trigger:** Admin cập nhật văn bản mới vào kho dữ liệu.

| Path | Câu hỏi thiết kế | Mô tả |
| :--- | :--- | :--- |
| **Happy Path** | User thấy gì? Flow kết thúc ra sao? | Push notification hiện tóm tắt. Tài xế ra lệnh: "Đọc tin mới". AI tóm tắt nội dung thay đổi cốt lõi trong 20s. |
| **Low-confidence** | System báo "không chắc" bằng cách nào? | AI nói: "Có thông báo mới về thiết bị, nhưng có vẻ chỉ áp dụng cho XanhSM Bike. Anh có muốn nghe thử không?" |
| **Failure** | User biết AI sai bằng cách nào? | AI thông báo một chính sách cũ đã hết hạn. User nhấn nút **"Báo cáo lỗi thời"**. |
| **Correction** | User sửa bằng cách nào? | Hệ thống gắn tag `Flag_Outdated` cho văn bản đó trong Vector DB để bộ phận vận hành cập nhật lại nguồn. |

### Feature 4: Smart Station Finder (Tìm trạm sạc thông minh)
**Trigger:** Pin xe < 20% hoặc tài xế ra lệnh: *"XanhSM ơi, tìm trạm sạc gần nhất"*

| Path | Câu hỏi thiết kế | Mô tả |
| :--- | :--- | :--- |
| **Happy Path** | User thấy gì? Flow kết thúc ra sao? | AI check GPS và Real-time API, phản hồi: "Trạm sạc Vincom cách 1km còn 3 trụ trống, tôi đã mở bản đồ cho anh." |
| **Low-confidence** | System báo "không chắc" bằng cách nào? | AI nói: "Trạm gần nhất đang mất tín hiệu dữ liệu trụ trống. Anh có muốn đổi sang trạm cách 2km chắc chắn còn chỗ không?" |
| **Failure** | User biết AI sai bằng cách nào? | Tài xế đến nơi nhưng trạm đang bảo trì hoặc hết trụ thực tế. User nhấn nút **"Báo cáo trạm lỗi"**. |
| **Correction** | User sửa bằng cách nào? | Hệ thống gắn tag `Station_Issue` để AI tạm thời không gợi ý trạm đó cho các tài xế khác trong 30p. |

---

## 3. Eval metrics + threshold

**Optimize precision hay recall?** **Precision** 

**Lí do:** Do đây là thông tin về chính sách công ty nên cần cung cấp chính xác cho tài xế, nếu thông tin tràn lan nhưng sai thì sẽ gây ảnh hưởng cho cả tài xế và công ty

| Metric | Threshold (Ngưỡng) | Red flag (Dừng khi) |
| :--- | :--- | :--- |
| **Độ chính xác tính toán** | 100% | < 99% (Sai tiền là lỗi nghiêm trọng) |
| **Độ chính xác trạng thái trạm sạc** | ≥ 95% | < 85% |
| **Độ chính xác trả lời chính sách** | ≥ 98% | < 90% |
| **Độ trễ phản hồi (Latency)** | < 2s | > 5s |

---

## 4. Top 3 failure modes

| # | Trigger | Hậu quả | Mitigation (Giảm thiểu) |
| :--- | :--- | :--- | :--- |
| **1** | Logic tính thưởng đa tầng phức tạp | AI tính sai tổng tiền thưởng | Kết hợp **Deterministic Code** để xử lý toán học sau khi LLM trích xuất các tham số. |
| **2** | Dữ liệu trụ sạc thời gian thực bị delay | Tài xế đến trạm nhưng hết chỗ | Ưu tiên gợi ý trạm có **biên an toàn** (còn >2 trụ trống) và tích hợp nút báo cáo nhanh. |
| **3** | Tiếng ồn môi trường làm sai lệch lệnh | AI thực hiện sai hành động | Hiển thị tóm tắt câu lệnh lên màn hình và chờ 1.5s xác nhận trước khi thực hiện. |

---

## 5. ROI 3 kịch bản

| Kịch bản | Assumption | Benefit |
| :--- | :--- | :--- |
| **Conservative** | 10% tài xế dùng | Giảm nhẹ tải hotline; Giảm tình trạng tài xế chạy lòng vòng tìm trạm sạc. |
| **Realistic** | 45% tài xế dùng | Tài xế tăng hiệu suất chạy mốc thưởng; Giảm 40% thắc mắc thu nhập; Tối ưu hóa hạ tầng trạm sạc. |
| **Optimistic** | 85% tài xế dùng | AI trở thành "Quản lý vận hành" toàn diện; Tối ưu hóa chi phí hỗ trợ và tăng mức độ hài lòng của tài xế. |

---

## 6. Mini AI spec

**XanhSM Policy Assistant** là trợ lý đa phương thức tích hợp RAG, Voice AI, Math Engine và Geo-Spatial API.

* **Cơ chế Kỹ thuật:**
    * **Math & Reasoning:** Sử dụng **Chain-of-Thought** để giải thích cách tính thưởng.
    * **Real-time EV Integration:** Kết nối API hệ thống trạm sạc VinFast để lấy trạng thái trụ trống theo GPS.
    * **Voice Interaction (STT & TTS):** Tương tác 100% rảnh tay khi xe đang di chuyển.
    * **Proactive Notification:** Tự động nhắc sạc pin khi xuống mức nguy hiểm hoặc nhắc mốc thưởng ngay khi kết thúc chuyến xe.

* **Giao diện báo cáo nhanh:** Thẻ Card font lớn, tương phản cao: **[Pin %] - [Số trụ trống gần nhất] - [Mốc thưởng kế tiếp]**.

* **Cam kết:** An toàn là trên hết. Giao diện tối giản, giảm thiểu tối đa thao tác chạm vào màn hình khi đang thực hiện chuyến xe.