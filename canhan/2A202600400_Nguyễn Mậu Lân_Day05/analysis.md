# UX Exercise — Chatbot Neo (VN Airlines)

## Sản phẩm: Chatbot Neo — Vietnam Airlines Assistant

### Khám phá (Discovery)
* **Tra cứu thông tin chuyến bay.**
* **Thông tin về vé máy bay:** bao gồm lịch bay, chương trình ưu đãi, thanh toán, hoàn/đổi vé.
* **Hướng dẫn thủ tục và các loại giấy tờ.**

---

### Thực tế (Current Status)
* **Khả năng:** Hỗ trợ về thông tin hành lý, hướng dẫn thủ tục giấy tờ, giá vé.
* **Hạn chế:** Chỉ đưa ra hướng dẫn chung, **không linh hoạt**. 
* **Vấn đề cốt lõi:** Không tra cứu được các chuyến bay một cách tự nhiên (chỉ tra được khi có số vé hoặc số hiệu chuyến bay cụ thể). Các câu trả lời chủ yếu là kịch bản có sẵn.

---

## Phân tích 4 paths

| Path | Trạng thái hệ thống |
| :--- | :--- |
| **1. AI Đúng** | Đưa ra hướng dẫn chung, sử dụng các câu trả lời có sẵn. |
| **2. AI Không chắc** | Hiện tại chưa có cơ chế xử lý rõ ràng cho trường hợp này. |
| **3. AI Sai** | Người dùng nhận ra khi đối chiếu; hệ thống đưa ra thông tin và hướng dẫn không đúng mong muốn. |
| **4. Mất niềm tin** | Hệ thống cung cấp hotline và email hỗ trợ để người dùng tìm phương án thay thế. |

---

## Path yếu nhất: Path 1 + 3
* **Phân tích:** Hệ thống hiện tại quá cứng nhắc. Khi người dùng cần tra cứu linh hoạt (ví dụ: tìm chuyến bay theo điểm đến), bot chỉ phản hồi được nếu có số hiệu cụ thể.
* **Hệ quả:** Flow xử lý lỗi (recovery flow) chưa tốt, khiến người dùng phải chuyển sang kênh truyền thống (Hotline) thay vì giải quyết được vấn đề ngay trên chatbot.

---

## Gap giữa Marketing & Thực tế
* **Marketing:** Quảng bá là trợ lý thông minh hỗ trợ khách hàng mọi lúc.
* **Thực tế:** Chatbot hoạt động như một hệ thống tra cứu theo mã (code-based) hơn là một AI có khả năng hiểu ngôn ngữ tự nhiên. 
* **Khoảng cách:** Không hỗ trợ được nhu cầu tìm kiếm thông tin ở giai đoạn "khám phá" của hành khách.

---

## Sketch (Kịch bản so sánh)

### 1. As-is (Hiện tại)
* **User gõ:** "Đưa thông tin các chuyến bay đi Đà Nẵng."
* **Neo phản hồi:** Đưa ra 2 lựa chọn cứng:
    * Tra cứu theo Mã đặt chỗ / Số vé.
    * Tra cứu theo Số hiệu chuyến bay.
* **Kết quả:** Không tìm được thông tin nếu user chưa mua vé hoặc chưa biết số hiệu.

### 2. To-be (Mong muốn)
* **User gõ:** (Thông tin tương tự về chuyến bay đi Đà Nẵng).
* **Neo phản hồi:** Trả về danh sách các chuyến bay khả dụng và giá vé tương ứng.
* **Mục tiêu:** Hệ thống nhận diện được ý định (intent) của người dùng và đưa ra thông tin mong muốn thay vì bắt user khớp theo format của máy.