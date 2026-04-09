import streamlit as st
import requests
import html

# ------------------------------------------------------------------
# CONFIG & CSS
# ------------------------------------------------------------------
st.set_page_config(page_title="XanhSM Assistant", page_icon="🤖", layout="wide")

st.markdown("""
<style>
/* XanhSM Theme overrides */
:root {
  --clr-primary: #00b5b5;
}
.stApp {
    background-color: #0a0a0a;
}
.highlight-mark {
  background-color: rgba(255, 215, 0, 0.4);
  color: #fff;
  padding: 0.1em 0.3em;
  border-radius: 4px;
  font-weight: 500;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.2);
}
.source-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: #00b5b5;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
}
.excerpt-box {
  background: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #00b5b5;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
  line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# HELPER: HIGHLIGHT EXTRACTOR
# ------------------------------------------------------------------
def get_highlighted_html(source_text: str, quotes: list) -> str:
    if not source_text:
        return "<i>(Không có dữ liệu văn bản gốc)</i>"

    # Hiển thị toàn bộ văn bản gốc và escape mã HTML để an toàn
    html_out = html.escape(source_text).replace('\n', '<br/>')

    if quotes:
        for q in quotes:
            q = q.strip()
            if not q: continue
            
            escaped_q = html.escape(q).replace('\n', '<br/>')
            # Thay thế tất cả các match trong toàn văn bản
            html_out = html_out.replace(escaped_q, f'<mark class="highlight-mark">{escaped_q}</mark>')
            
    # Bọc trong một hộp
    return f'<div class="excerpt-box">{html_out}</div>'

# ------------------------------------------------------------------
# MAIN APP
# ------------------------------------------------------------------
st.title("🤖 XanhSM Assistant")
st.caption("Trợ lý Chính sách Tài xế")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Xin chào Bác Tài Xanh! Tôi là Trợ lý Chính sách XanhSM. Tôi có thể giúp gì cho anh về quy định thưởng/phạt hay quy trình vận hành hôm nay?"}
    ]

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Details expander for sources
        if msg["role"] == "assistant" and "quotes" in msg:
            with st.expander("📜 Trích dẫn văn bản gốc"):
                st.markdown('<div class="source-label">NGUỒN: CHÍNH SÁCH VẬN HÀNH XANHSM 2026</div>', unsafe_allow_html=True)
                html_snippet = get_highlighted_html(msg.get("source_text", ""), msg.get("quotes", []))
                st.markdown(html_snippet, unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("Hỏi về thưởng tuần, lương cơ bản, quy tắc ứng xử…"):
    # Append User msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Fetch AI msg
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                res = requests.post(
                    "http://localhost:8000/query", 
                    json={"query": prompt},
                    timeout=90
                )
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "")
                    source_text = data.get("source_text", "")
                    quotes = data.get("quotes", [])
                    
                    st.markdown(answer)
                    with st.expander("📜 Trích dẫn văn bản gốc"):
                        st.markdown('<div class="source-label">NGUỒN: CHÍNH SÁCH VẬN HÀNH XANHSM 2026</div>', unsafe_allow_html=True)
                        html_snippet = get_highlighted_html(source_text, quotes)
                        st.markdown(html_snippet, unsafe_allow_html=True)
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "source_text": source_text,
                        "quotes": quotes
                    })
                else:
                    err_msg = f"⚠ Lỗi {res.status_code}: Không thể lấy phản hồi từ server."
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
            except Exception as e:
                err_msg = f"⚠ Lỗi kết nối: Mở terminal phía backend chạy `python main.py` nhé. Chi tiết: {str(e)}"
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})
