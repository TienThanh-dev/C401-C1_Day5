"""
Máy chủ FastAPI — Cung cấp API phục vụ Hệ thống AI Trợ lý Chính sách XanhSM.

File này chứa toàn bộ các khai báo API, quy tắc CORS (cho phép Font-end giao tiếp),
và chứa hệ thống logic cốt túy xử lý câu lệnh yêu cầu (Prompt Engineering) đối với RAG.
"""

import logging
import os
import glob
import re
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import hàm Factory Singleton để lấy instance kiến thức RAG
from rag_manager import get_rag_instance
from ingest import ingest_policies

# Cấu hình logging mặc định cho server FastAPI
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# =========================================================================
# CONSTANT CAUTIONS (SYSTEM PROMPTS)
# =========================================================================

# Khối lệnh nhắc (Prompt) được thiết kế đặc biệt nhằm ràng buộc thái độ 
# và khả năng tư duy step-by-step của LLM đối với dữ liệu nội bộ XanhSM.
SYSTEM_INSTRUCTION_PROMPT = """
QUAN TRỌNG:
1. TRẢ LỜI CHI TIẾT: Yêu cầu trả lời thật chi tiết, đầy đủ nhất có thể. Giải thích cặn kẽ mọi yếu tố liên quan. Tuyệt đối KHÔNG trả lời vắn tắt hay tóm lược.
2. TÍNH TOÁN BƯỚC MỘT (Step-by-Step): NẾU câu hỏi có yếu tố đánh giá, TÍNH TOÁN (tính lương, thưởng, phạt tiêu chuẩn...), bạn PHẢI thực hiện phân tích 'từng bước một'. Trích xuất trọn vẹn con số từ tài liệu, viết rõ ràng minh bạch các phép tính trước khi đưa ra kết quả cuối cùng để đảm bảo độ tin cậy tuyệt đối.
3. TRÍCH DẪN NGUỒN CỤ THỂ (Quotes): Ở cuối câu trả lời của bạn, PHẢI liệt kê chính xác các đoạn trích dẫn (nguyên văn) mà bạn đã dùng từ tài liệu. Đặt mỗi trích dẫn đó trong một thẻ mở/đóng <quote>...</quote>. Ví dụ: <quote>đoạn 1</quote>.
4. CHỈ ĐỊNH TÊN TÀI LIỆU GỐC: Cuối cùng, hãy liệt kê TÊN ĐẦY ĐỦ của (các) tệp tài liệu gốc mà bạn đã sử dụng. Đặt tên tệp trong thẻ mở/đóng <file>...</file>. Xin viết chính xác tên viết hoa hay các dấu gạch dưới nếu có. Ví dụ: <file>Chính sách lương_cơ_bản.txt</file>.
"""


# =========================================================================
# LIFESPAN (VÒNG ĐỜI SERVER)
# =========================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Hàm Vòng đời (Lifespan). Được FastAPI tự động kích hoạt khi server vừa được chạy lên.
    Mục đích: Gọi `get_rag_instance()` một lần để "Hâm nóng" mô hình RAG (Load graph DB) trước khi có Request ập tới.
    """
    logger.info("Đang khởi động Server Trợ Lý Chính Sách XanhSM API...")
    get_rag_instance()  # Warm up database
    yield
    logger.info("Đang tắt Server (Shutdown).")


# =========================================================================
# CẤU HÌNH ỨNG DỤNG (APP SETUP)
# =========================================================================

app = FastAPI(
    title="XanhSM Policy Assistant API",
    description="Backend AI trả lời chính sách bằng mô hình RAG dành cho tài xế XanhSM.",
    version="1.0.0",
    lifespan=lifespan,
)

# Cấu hình CORS (Cross-Origin Resource Sharing) 
# Cho phép Streamlit (hoặc React/Next) chạy ở các port khác có thể POST tới API này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dành cho Development. Nếu deploy production hãy thay bằng URL thật
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================================
# DATA SCHEMAS (KHUNG DỮ LIỆU ĐẦU VÀO / ĐẦU RA BẰNG PYDANTIC)
# =========================================================================

class QueryRequest(BaseModel):
    """Mô hình dữ liệu nhận vào (Input) từ request gửi đi của Bot."""
    query: str = Field(..., min_length=1, max_length=1000, description="Câu hỏi chi tiết từ bác tài")
    mode: str = Field(
        default="hybrid",
        pattern="^(naive|local|global|hybrid)$",
        description="Chế độ phân tích RAG (Khuyến cáo ưu tiên dùng hybrid)",
    )


class QueryResponse(BaseModel):
    """Mô hình dữ liệu trả về (Output JSON) cho phía Font-end ứng dụng."""
    answer: str                 # Phần trả lời trọng tâm (đã bóc tách thẻ html cặn bùn)
    sources: List[str]          # [Hiện không xài tới]
    quotes: List[str]           # Danh sách các câu trích dẫn chuẩn xác (dùng để highlight text)
    source_text: str            # Đoạn chép chứa toàn bộ bộ luật của tài liệu mà LLM dùng để truy xuất


# =========================================================================
# ĐỊNH NGHĨA API ENDPOINTS (ROUTE)
# =========================================================================

@app.get("/", summary="Kiểm tra trạng thái máy chủ (Health check)")
async def health_check():
    """Endpoint root cơ bản để ping thử xem server chạy chưa."""
    return {"status": "ok", "service": "XanhSM Policy Assistant API"}


@app.post("/ingest", summary="Buộc máy chủ chạy lại hàm cập nhật tài liệu chính sách")
async def ingest_endpoint():
    """
    Endpoint kích hoạt hàm ingest.py để nạp dữ liệu vào DB mà không cần gõ lệnh.
    Cực kì hữu dụng nếu tích hợp chung vào giao diện Front-end (Nút 'Cập nhật lại dữ liệu').
    """
    try:
        await ingest_policies()
        return {"status": "success", "message": "Dữ liệu Knowledge Graph đã được làm mới!"}
    except Exception as e:
        logger.exception("Ingest dữ liệu qua mạng bị lỗi")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse, summary="Xử lý câu hỏi về chính sách")
async def query_policy(request: QueryRequest):
    """
    Endpoint Cốt Lõi. Nhận câu hỏi ngôn ngữ tự nhiên -> Nhúng (Embed) -> 
    Truy vấn LightRAG -> Phân giải XML/HTML -> Bóc tách về trả kết quả sạch.
    """
    try:
        # Lấy Instance Singleton
        rag = get_rag_instance()
        
        # 1. Gắn thêm Instruction (Luật lệ suy luận) vào mệnh lệnh người dùng
        modified_query = f"{request.query}\n\n{SYSTEM_INSTRUCTION_PROMPT}"
        
        # 2. Bắt đầu đẩy lên Cloud để AI tính toán và truy tìm trong Knowledge Graph
        # Output raw của `result` thực tế là nguyên một chuỗi string văn bản.
        raw_result_str = await rag.query(modified_query, mode=request.mode)
        
        # 3. Sử dụng RegEx (Regular Expressions) để bóc tách thông tin XML tag
        # Lấy các String nằm ở giữa `<quote>` và `</quote>`
        quotes: List[str] = re.findall(r"<quote>(.*?)</quote>", raw_result_str, flags=re.DOTALL)
        # Làm sạch chuỗi dư thừa
        quotes = [q.strip() for q in quotes if q.strip()]

        # Lấy các String nằm ở giữa `<file>` và `</file>`
        files: List[str] = re.findall(r"<file>(.*?)</file>", raw_result_str, flags=re.DOTALL)
        files = [f.strip() for f in files if f.strip()]
        
        # 4. Filter dọn dẹp văn bản hiển thị cho người xem (Lược bỏ bớt rác tag <quote> và <file>)
        clean_answer = re.sub(r"<quote>.*?</quote>", "", raw_result_str, flags=re.DOTALL)
        clean_answer = re.sub(r"<file>.*?</file>", "", clean_answer, flags=re.DOTALL).strip()
        
        # 5. Duyệt trong ổ cứng để tìm chính xác văn bản Full-text tương ứng với list tên `files` 
        # (Để trả về cho Frontend làm tư liệu View Document/Highlight)
        # 5. Duyệt trong ổ cứng để tìm chính xác văn bản Full-text tương ứng với list tên `files` 
        # (Để trả về cho Frontend làm tư liệu View Document/Highlight)
        combined_source_text = ""
        
        # Dùng pathlib để trỏ chính xác tuyệt đối ra thư mục gốc chứa file .txt
        import pathlib
        policy_dir = pathlib.Path(__file__).resolve().parent.parent
        txt_files = list(policy_dir.glob("*.txt"))
        
        debug_info = f"LLM FILES: {files}\n"
        for fpath in txt_files:
            fname = fpath.name
            fname_norm = fname.lower().replace(".txt", "").replace("_", " ")
            
            # Logic Đối chiếu: Nếu File do LLM đề xuất có tồn tại tên (tương đối),
            # Hoặc list `files` LLM không xuất gì (trọng số lỏng) thì sẽ đính kèm bản txt text cho source view.
            is_file_used = True
            if files:
                # Cắt đuôi .txt và thay dấu _ khoảng trắng khỏi tf nếu có để so sánh thoải mái
                # Tới nước này là thà bắt nhầm còn hơn bỏ sót
                is_file_used = any(
                    (tf.lower().replace(".txt", "").replace("_", " ").strip() in fname_norm) or 
                    (fname_norm in tf.lower().replace(".txt", "").replace("_", " ").strip()) 
                    for tf in files
                )
                
            debug_info += f"FNAME: {fname} | NORM: {fname_norm} | MATCH: {is_file_used}\n"
            if not is_file_used:
                continue  # Bỏ qua tài liệu này vì LLM không ưu tiên nó
                
            with open(fpath, "r", encoding="utf-8") as f:
                # Ghép nguyên gốc text vào combined result, đóng dập Header để Streamlit Parser
                combined_source_text += f"=== NGUỒN: {fname} ===\n\n{f.read()}\n\n"
        
        # ---------------- FALLBACK TỐI THƯỢNG ----------------
        # Nếu vì lý do nào đó (LLM bịa tên, regex hỏng) mà ta không tìm được file nào:
        # => Buộc phải đính kèm tất cả file để tránh lỗi "(Không có dữ liệu gốc)" trên Front-end
        if not combined_source_text.strip() and txt_files:
            for fpath in txt_files:
                with open(fpath, "r", encoding="utf-8") as f:
                    combined_source_text += f"=== NGUỒN: {fpath.name} ===\n\n{f.read()}\n\n"

        with open("debug_main.txt", "w", encoding="utf-8") as dfile:
            dfile.write(debug_info)

        # Trả về kết quả JSON tiêu chuẩn theo Pydantic Schema
        return QueryResponse(
            answer=clean_answer, 
            sources=[],
            quotes=quotes,
            source_text=combined_source_text
        )

    except Exception as e:
        logger.exception(f"Lỗi truy vấn đối với câu hỏi: {request.query}")
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================================
# LỆNH KHỞI ĐỘNG XUYÊN HỆ THỐNG DEVELOPMENT (ENTRY POINT)
# =========================================================================
if __name__ == "__main__":
    import uvicorn
    # Chỉ chạy khi gõ bằng lệnh python main.py
    uvicorn.run(
        "main:app",
        host="0.0.0.0",           # Bind mọi địa chỉ IP mạng nội vùng
        port=8000,                # Mở cổng API 8000
        reload=True,              # Tự reload server khi Dev có sửa đổi File Python mới (hot reload)
    )
