# Prototype — XanhSM

## Mô tả
Chatbot thông minh hỗ trợ tài xế XanhSM tra cứu chính sách thưởng/phạt và quy trình vận hành. Sử dụng công nghệ **LightRAG** (Knowledge Graph-enhanced RAG) để đảm bảo câu trả lời chính xác, có ngữ cảnh và trích dẫn văn bản gốc trực quan.

## Level: Mock prototype
- UI build bằng gemini
- Dữ liệu thật từ các file chính sách public của xanhsm

## Links
 Prototype : https://github.com/dungvu242k3/xanhsm

 ## Tools
 UI : gemini
 AI : openai_key
 prompt : system-prompt 

## phân công
| Thành viên | Phần | Output |
|-----------|------|--------|
| Dũng | code |  UI +  ingest.py + streamlit.py|
| Thành | code | rag_manager.py + main.py |
| Phương | data | các bộ data file txt    |
| Trí | UX designer + prompt engineer | flow chatbot và viết system prompt |
|Lân| spec + demo | spec/spec-final.md + demo/demo-script.md |

