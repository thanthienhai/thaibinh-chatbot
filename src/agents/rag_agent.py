import os
from typing import Any
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from typing import List, Dict, Any
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_community.chat_message_histories import Neo4jChatMessageHistory

from chains.semantic_search_chunk_chain import get_chunk

from tools.tools import get_customer_service_infor
from llm.get_llm import get_embedding_function, get_model_function
from llm.get_graph import get_graph_function
from langchain_core.runnables.history import RunnableWithMessageHistory



print("✅✅call agent step")

graph = get_graph_function()
@tool 
def explore_document(question: str) -> str:

    """
    Useful for answering questions about relevant information in the document. Use the entire prompt
    as input to the tool. When the question is general and hard to find keywords from the question.
    For example, if the prompt is "Tôi cần tìm thông tin về điều kiện gia nhập đoàn".

    For when you need to find information about movies based on a plot"
    """
    
    result =  get_chunk(question)
    return result


# @tool
# def get_from_database(text: str) -> List[Dict[str, Any]]:
#     """
#     Useful query information from databse for answering questions about customers, products, brands, orders,
#     customer reviews, sales statistics, and product availability. Use the entire prompt
#     as input to the tool. Or give the overview about the product.
#     Here is few example:
#     1. What are the specifications and features of [product_name]
#     2. How does [product_name] compare to other products in terms of sales?
#     3. How many products does [brand_name] have listed in our marketplace?
#     4. What are the most common complaints from customers about [brand_name]?
#     5. Which products are trending in the [category]?
#     """
#     return cypher_summary()


@tool
def get_customer_service() -> str:
    """
    Retrieve contact information for customer service.
    
    Example:
    "How can I contact customer service?"
    """
    return get_customer_service_infor()


agent_tools = [

    explore_document,
    get_customer_service,
    # get_from_database,
 
]
def get_memory(session_id):
    return Neo4jChatMessageHistory(session_id=session_id, graph=graph)

agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Bạn là một chatbot hỗ trợ người dùng trả lời các câu hỏi liên quan đến Đoàn Thanh niên Cộng sản Hồ Chí Minh và Đảng Cộng sản Việt Nam. Dựa trên tài liệu và thông tin đã cung cấp, hãy thực hiện các nhiệm vụ sau:
                1.	Trả lời câu hỏi: Giải đáp các thắc mắc của người dùng về tổ chức, nhiệm vụ, quyền hạn, quy trình hoạt động, và các nội dung liên quan đến Điều lệ Đoàn Thanh niên Cộng sản Hồ Chí Minh hoặc Đảng Cộng sản Việt Nam.
                2.	Giữ ngôn ngữ chính xác và dễ hiểu:
                •	Sử dụng giọng văn trang trọng, khách quan.
                •	Đảm bảo thông tin chính xác, ngắn gọn, và phù hợp với nội dung tài liệu đã cung cấp.
                3.	Hạn chế vượt ra ngoài nội dung tài liệu:
                •	Chỉ trả lời các câu hỏi dựa trên những thông tin đã được cung cấp.
                •	Nếu thông tin không có trong tài liệu, hãy trả lời rằng bạn không có thông tin hoặc khuyến nghị người dùng tham khảo nguồn khác.
                6.	Trung thành với thông tin trong tài liệu:
                •	Không phỏng đoán hoặc thêm thông tin ngoài tài liệu.
                •	Luôn nhắc đến cơ sở quy định trong tài liệu nếu người dùng yêu cầu làm rõ.
                7.	Phong cách trả lời:
                •	Luôn giữ sự lịch sự, sẵn sàng giúp đỡ.
                •	Cung cấp câu trả lời với định dạng dễ theo dõi khi mô tả quy trình hoặc danh sách.
                8. Lưu ý:
                    Câu trả lời không nên quá ngắn. Nếu câu trả lời quá ngắn bạn có thể giải thích thêm. Bạn nên thêm phần tương tác với người dùng ở cuối câu trả lời và khuyến khích họ hỏi thêmc các chủ đề liên quan. 
                9. Khi không tìm được tài liệu trong hệ thông cung cấp hãy nói người dùng sử dụng cách diễn đạt khác. Nếu 2 lần vẫn không thể hỗ trợ. Hãy cung cấp cho  người dùng thông tin chăm sóc khách hàng để người dùng tự liên hệ.
                10. Để đảm bảo chất lượng và uy tín của câu trả lời. Bạn luôn phải đưa ra những thông tin tham khảo vào cuối câu trả lời theo format từ metadata: Tên file tài liệu - Số trang - [**Link thao khảo từ metadata**]
            Ví dụ:
            Câu hỏi: Quy trình kết nạp đoàn viên Đoàn Thanh niên Cộng sản Hồ Chí Minh như thế nào?
            Câu trả lời:
            Quy trình kết nạp đoàn viên mới bao gồm các bước:
                1.	Thanh niên tự nguyện viết đơn xin gia nhập Đoàn, báo cáo lý lịch.
                2.	Nhận sự giới thiệu và bảo đảm từ một đoàn viên, chi hội hoặc tập thể liên quan.
                3.	Hội nghị chi đoàn tổ chức họp để xét kết nạp với biểu quyết tán thành của trên 1/2 đoàn viên có mặt.
                4.	Đoàn cấp trên trực tiếp ra quyết định kết nạp.
            Previous conversation history:
            """
        ),
        

        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent_llm_with_tools = get_model_function().bind_tools(agent_tools)

rag_agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
        
    }
    | agent_prompt
    | agent_llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

rag_agent_executor = AgentExecutor(
    agent=rag_agent,
    tools=agent_tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True,
)

chat_agent = RunnableWithMessageHistory(
    rag_agent_executor,
    get_memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

