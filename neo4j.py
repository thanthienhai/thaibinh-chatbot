import os
import requests
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Lấy session ID
def get_session_id():
    return get_script_run_ctx().session_id

# URL API
CHATBOT_URL = "https://thaibinh-chatbot.onrender.com/docs-rag-agent"

# Tùy chỉnh giao diện
st.set_page_config(page_title="Tỉnh Đoàn Thái Bình - Chatbot", page_icon="logo-doan.png", layout="centered")

# Thêm CSS để cố định chiều ngang hộp chat
st.markdown(
    """
    <style>
    /* Cố định chiều ngang của hộp chat */
    .st-chat-message {
        max-width: 800px;
        margin: 0 auto; /* Căn giữa */
    }
    /* Tùy chỉnh phần chat input */
    .stTextInput > div > div {
        max-width: 800px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.header("📌 Câu hỏi thường gặp")
    with st.expander("Chủ đề liên quan đến Đoàn"):
        st.markdown("- Đoàn Thanh niên được tổ chức theo mấy cấp?")
        st.markdown("- Đoàn viên có độ tuổi giới hạn là bao nhiêu?")
        st.markdown("- Quy trình kết nạp đoàn viên mới?")
    with st.expander("Quyền lợi & nghĩa vụ"):
        st.markdown("- Vai trò của Đoàn trong Hội Liên hiệp Thanh niên?")
        st.markdown("- Nguồn tài chính của Đoàn đến từ đâu?")
    st.info("📞 **Thông tin hỗ trợ:** [Liên hệ chúng tôi](#)")

# Tiêu đề chính
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image('huy-hieu-doan.png', width=150)

col1, col2, col3 = st.columns([0.5,5,1])
with col2:
    st.title("ChatGPT Nghiệp vụ Đoàn")
st.write("---")  # Đường phân cách
st.info(
    """Chào bạn! Tôi là ChatGPT hỗ trợ Nghiệp vụ công tác Đoàn. Bạn có thể đặt bất kỳ câu hỏi nào về tổ chức, hoạt động của tổ chức Đoàn."""
)

# Hộp chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị các tin nhắn
st.subheader("💬 Hộp Chat")
for message in st.session_state.messages:
    role_style = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role_style):
        st.markdown(message["output"])

# Nhập nội dung
if prompt := st.chat_input("Hãy đặt câu hỏi của bạn..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "output": prompt})

    # Gửi API
    data = {"text": prompt, "session": get_session_id()}
    with st.spinner("⏳ Đang tìm kiếm câu trả lời..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json().get("output", "Không có phản hồi hợp lệ từ API.")
            explanation = response.json().get("intermediate_steps", "Không có giải thích được cung cấp.")
        else:
            output_text = "❌ Lỗi: Không thể xử lý yêu cầu của bạn."
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.session_state.messages.append(
        {"role": "assistant", "output": output_text, "explanation": explanation}
    )
