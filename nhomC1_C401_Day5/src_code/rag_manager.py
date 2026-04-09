"""
RAG Manager — Khởi tạo và Quản lý LightRAG cho Trợ lý XanhSM.

Module này đóng vai trò kết nối tới OpenAI (sử dụng GPT-4o-mini cho suy luận LLM 
và text-embedding-3-small cho nhúng từ/vector). 
Nó cung cấp một lớp quản lý phiên bản (XanhSMRAG) và duy trì sự hoạt động duy nhất (Singleton).
"""

import os
import logging
from pathlib import Path
from typing import Any, List, Optional
from dotenv import load_dotenv

# Import các thành phần tử cốt lõi của thư viện LightRAG
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc

# Khởi tạo logger để ghi log hệ thống
logger = logging.getLogger(__name__)

# Tải biên môi trường (.env) từ chính thư mục backend/
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

# Định nghĩa thư mục mặc định lưu trữ cơ sở dữ liệu Vector và Knowledge Graph 
# (sẽ lưu ngoài thư mục backend một cấp để tránh lộn xộn code)
DEFAULT_WORKING_DIR = str(Path(__file__).resolve().parent.parent / "xanhsm_storage")


async def llm_model_func(prompt: str, system_prompt: Optional[str] = None, history_messages: Optional[List[Any]] = None, **kwargs) -> str:
    """
    Hàm giao tiếp nội bộ LLM dành cho LightRAG.
    Mỗi khi LightRAG cần phân tích ngữ nghĩa, nó sẽ gọi hàm này.
    Ở đây cấu hình cứng dùng model 'gpt-4o-mini' để tối ưu chi phí và tốc độ.
    """
    return await openai_complete_if_cache(
        model="gpt-4o-mini",
        prompt=prompt,
        system_prompt=system_prompt,
        history_messages=history_messages or [],
        api_key=os.getenv("OPENAI_API_KEY"),  # Lấy key từ file .env
        **kwargs,
    )


async def embedding_func(texts: List[str]) -> List[List[float]]:
    """
    Hàm tạo Embedding (mã hóa văn bản thành Vector ngữ nghĩa) phục vụ tìm kiếm.
    Mỗi khi có tài liệu mới hoặc câu hỏi từ người dùng, nội dung sẽ được map bằng hàm này.
    """
    return await openai_embed(
        texts=texts,
        model="text-embedding-3-small", # Model tạo embedding hiệu suất cao của OpenAI
        api_key=os.getenv("OPENAI_API_KEY"),
    )


class XanhSMRAG:
    """
    Lớp đóng gói (Wrapper Class) bao bọc quy trình khởi tạo và truy vấn đến thư viện LightRAG.
    """

    def __init__(self, working_dir: str = DEFAULT_WORKING_DIR) -> None:
        """
        Hàm khởi tạo. Thiết lập môi trường và kết nối tới LightRAG.
        """
        self.working_dir = working_dir
        
        # Tạo sẵn tự động thư mục lưu trữ DB nếu chưa tồn tại trên ổ cứng
        os.makedirs(working_dir, exist_ok=True)
        self._initialized = False

        # Kiểm tra API Key, nếu không có sẽ sinh cảnh báo chứ chưa lỗi ngay
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            logger.warning("CẢNH BÁO: OPENAI_API_KEY chưa được set hợp lệ trong backend/.env")

        # Cấu hình cốt lõi của LightRAG: truyền vào hàm llm, hàm embedding, và tham số dung lượng token
        self.rag = LightRAG(
            working_dir=working_dir,
            llm_model_func=llm_model_func,
            embedding_func=EmbeddingFunc(
                func=embedding_func,
                embedding_dim=1536,    # OpenAI text-embedding-3-small trả về vector 1536 chiều
                max_token_size=8192,   # Giới hạn xử lý context 8192 token
            ),
        )
        logger.info(f"Đã khởi tạo xong LightRAG (lazy loading). Nơi chứa DB: {working_dir}")

    async def ensure_initialized(self) -> None:
        """
        Đảm bảo Storage Engine (vector DB) của LightRAG đã sẵn sàng.
        Phải được gọi một lần trước các thao tác insert hoặc query thực thụ.
        """
        if not self._initialized:
            await self.rag.initialize_storages()
            self._initialized = True

    async def ingest_text(self, text: str) -> None:
        """
        Chèn thêm toàn bộ một chuỗi văn bản (tài liệu) vào Kho dữ liệu đồ thị trí thức (RAG).
        """
        await self.ensure_initialized()  # Bật DB
        await self.rag.ainsert(text)     # Quá trình nhúng text diễn ra ở đây

    async def query(self, question: str, mode: str = "hybrid") -> str:
        """
        Thực hiện tra cứu trên kiến thức RAG.
        Mode support của LightRAG: 
          - 'naive': Tìm kiếm cơ bản (vector similarity)
          - 'local': Tập trung vào entity riêng lẻ trong knowledge graph
          - 'global': Tập trung vào mối liên hệ tổng quan (cấu trúc cộng đồng) trong graph
          - 'hybrid': Công thức lai giữa local và global (Khuyến nghị cho độ chính xác cao nhất)
        """
        await self.ensure_initialized()  # Bật DB
        # QueryParam thiết lập chế độ tìm kiếm để trả về kết quả
        return await self.rag.aquery(question, param=QueryParam(mode=mode))


# Biến private lưu trữ trạng thái Singleton
_rag_instance: Optional[XanhSMRAG] = None

def get_rag_instance() -> XanhSMRAG:
    """
    Factory Pattern / Singleton: Đảm bảo xuyên suốt cả một ứng dụng FastAPI 
    khi chạy sẽ chỉ có duy nhất (một) instance của XanhSMRAG được sinh ra 
    để không bị tốn RAM và rò rỉ kết nối vector DB.
    """
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = XanhSMRAG()
    return _rag_instance
