
# from groq import Groq
# import os

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def get_ai_response(prompt):
#     response = client.chat.completions.create(
#         model="llama3-70b-8192",
#         messages=[
#             {"role": "system", "content": "You are Loop AI, a hospital assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message.content
