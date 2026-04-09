## Phần 2 — Phân tích 4 Paths

**1. Khi AI đúng:**

- **User thấy:** Các thông tin về tài chính cá nhân, phân loại danh mục,... được cập nhật realtime.
- Có hiển thị danh mục thay đổi ngân sách, phân loại dòng tiền,... Có thể check ngay lập tức được.

    Tốt: Rõ ràng, delightful, khuyến khích tiếp tục dùng.

**2. Khi AI không chắc:**

- Hệ thống: Moni hỏi lại người dùng, hoặc nói rằng không hỗ trợ hoặc chưa thực hiện được.

**3. Khi AI sai:**
- Có bảo lại về các phần đã sửa, user phải tự check đã đúng chưa, chỉnh sửa thủ công hoặc nói lại với chat để sửa.
**4. Khi user mất tin (AI sai nhiều lần hoặc không hiểu):**
- Có hotline , và quản lý chi tiêu thủ công khá là dễ dùng. Toàn bộ message và action đều có thể feedback lại bằng like hoặc dislike.

**Tự phân tích:**

- **Path xử lý tốt nhất:** Path 1 (AI đúng) — vì có Big Data +AI nên rất tự tin vào dữ liệu được cá nhân hóa, phân tích và tổng hợp tốt về dòng tiền cá nhân trong nội bộ app, gợi ý chi tiêu và phân loại danh mục tài chính tốt, dễ quản lý.
- **Path yếu nhất:** Path 4 (mất tin) hoặc Path 3 (AI sai) — fallback con người chưa seamless, sửa đôi khi nhiều bước nếu chat không hiểu, thiếu "confidence score" rõ ràng.
- **Gap marketing vs thực tế:** Marketing hứa "thông minh như quản gia", thực tế tốt cho user mới nhưng với user power user, AI vẫn generic và chưa dự báo sâu (ví dụ dự báo cashflow tháng tới). Gap ở độ sâu cá nhân hóa & error recovery.