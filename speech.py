
from google import genai

# Configure API key
client = genai.Client (api_key = "your-api-key")
response = client.models.generate_content(
    model = "gemini-2.0-flash",
    contents = "Why is sky blue?"
)
print (response.text)

