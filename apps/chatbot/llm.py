from google import genai
from google.genai.types import Content

# Configure the client
client = genai.Client(api_key="YOUR_GOOGLE_API_KEY")

# Call Gemini
response = client.models.generate_content(
    model="gemini-2.0-pro-exp",  # you can also use gemini-1.5-pro
    contents=[Content(role="user", parts=["What is my biggest expense this month?"])],
)

print(response.text)
