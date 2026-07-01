import os
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# client configuration
gemini_api_key = os.getenv("gemini_api_key")
client = genai.Client(api_key = gemini_api_key)

folder_path = "optisigns_articles"
uploaded_files = []

# upload .md files to gemini file API
print("uploading data to gemini file API")
for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)
        
        f = client.files.upload(
            file=file_path, 
            config={'display_name': filename, 'mime_type': 'text/plain'}
        )
        uploaded_files.append(f)
        
        print(f"  └─ uploaded: {filename}")
        time.sleep(2) 

print("\n=== UPLOAD RESULT ===")
print(f"Total: {len(uploaded_files)} files")
print("chunks: 1 (use Long-context window)\n")

# Initiate system prompt and question
system_instruction = """You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply."""

question = "How do I add a YouTube video?"

prompt = [question] + uploaded_files

# call model
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.1
    )
)

print("\n=== OPTIBOT ANSWER ===")
print(response.text)