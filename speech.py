# import google.generativeai as genai

# genai.configure(api_key="AIzaSyB5mYJJa7vfgwLkmpe2Cw2r9Ldc8O9B0hg")

# generation_config = {
#     "temperature": 0.9,
#     "top_p": 1,
#     "top_k":1,
#     "max_output_tokens": 2048,
# }

# model = genai.GenerativeModel(
#     model_name="gemini-1.0-pro",generation_config= generation_config
# )
# convo = model.start_chat(history=[])

# convo.send_message ("Hii, Give me 3 names")
# print(convo.last.text)

from google import genai

# Configure API key
client = genai.Client (api_key = "AIzaSyA7UAuOPaYMV06AH-XG8KnDJ3ERCKcJDow")
response = client.models.generate_content(
    model = "gemini-2.0-flash",
    contents = "Why is sky blue?"
)
print (response.text)
