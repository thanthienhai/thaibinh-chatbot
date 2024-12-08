import requests

CHATBOT_URL="http://chatbo-albae-sonwpq1g7qtg-1247164783.us-east-1.elb.amazonaws.com/market-rag-agent"


data = {
"text": "Xin chào rất vui được gặp bạn"
}

response = requests.post(CHATBOT_URL,json=data)
print("✅✅   "   +    str(response.json()['output']))
print("✅✅   "   +    str(response.json()['intermediate_steps']))


# if response.status_code == 200:
#     output_text = response.json()["output"]
#     explanation = response.json()["intermediate_steps"]