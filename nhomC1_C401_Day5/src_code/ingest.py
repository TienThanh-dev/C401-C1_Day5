"""
Ingest Pipeline — Tự động Nạp dữ liệu các file chính sách (.txt) vào LightRAG (Knowledge Graph).

Công dụng: 
- Lấy đường dẫn thư mục hiện tại, tìm các file đuôi txt, và đưa vào kho kiến thức.
- Nên chạy thủ công file này một lần (python ingest.py) mỗi khi có bản cập nhật quy định chính sách mới,
  hoặc được gọi thông qua endpoint /ingest trên FastAPI.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List

from rag_manager import get_rag_instance

# Cấu hình hiển thị log chi tiết dạng: Thời gian - LOG LEVEL - Thông báo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Thư mục gốc chứa các file văn bản dữ liệu (TXT) là root project (1 thư mục bên trên backend)
POLICY_DIR = Path(__file__).resolve().parent.parent


async def ingest_policies(directory: Path = POLICY_DIR) -> None:
    """
    Hàm đọc và nạp toàn bộ danh sách các tập tin *.txt trong `directory` vào LightRAG.
    """
    
    # 1. Quét tìm danh sách các file .txt có trong thư mục, sắp xếp thứ tự từ A->Z
    policy_files: List[Path] = sorted(directory.glob("*.txt"))

    # Kiểm tra nếu thư mục rỗng, không có tài liệu thì dừng chương trình
    if not policy_files:
        logger.error(f"Không tìm thấy file .txt nào tại {directory}")
        sys.exit(1)

    logger.info(f"Đã phát hiện {len(policy_files)} file chính sách tại {directory}")

    # 2. Khởi tạo kho kiến thức RAG thông qua class Singleton
    rag = get_rag_instance()

    # 3. Duyệt vòng lặp qua từng file để đọc văn bản và nạp lên hệ thống vector DB
    for filepath in policy_files:
        logger.info(f"Đang Ingest: {filepath.name} ({filepath.stat().st_size} bytes)")
        
        try:
            # Đọc toàn bộ chuỗi ký tự bên trong file, bắt buộc xử lý qua định dạng Unicode UTF-8
            content = filepath.read_text(encoding="utf-8")
            
            # Đính kèm một thẻ Header (đánh dấu tên tệp) để đồ thị trí thức (Graph) 
            # ghi nhận thông tin và LLM dễ dàng tham chiếu nguồn hơn
            header = f"\n--- TÀI LIỆU: {filepath.name} ---\n"
            
            # Gọi hàm nhúng nạp vào LightRAG (sẽ gọi tốn API Tokens của LLM OpenAI)
            await rag.ingest_text(header + content)
            
            logger.info(f"✓ Hoàn tất Ingest file: {filepath.name}")
            
        except UnicodeDecodeError:
            # Bắt lỗi file bị hỏng encoding (vd: tải tử excel utf-16) thay vì sập script
            logger.warning(f"⚠ Bỏ qua {filepath.name} — File không đúng chuẩn UTF-8")
        except Exception as e:
            # Bắt toàn bộ lỗi bất ngờ khác (ví dụ rớt mạng Internet)
            logger.exception(f"✗ Ingest thất bại {filepath.name} do lỗi: {e}")

    logger.info("=== Toàn bộ tiến trình INGEST hoàn tất ===")


if __name__ == "__main__":
    # Chỉ chạy block code này khi script này được gõ lệnh "python ingest.py" trực tiếp.
    # Khởi động Event Loop của Asyncio để thực thi coroutine ingest_policies
    asyncio.run(ingest_policies())
