import os
import google.generativeai as genai

import os
import PyPDF2

# Define the PDF file path
pdf_file = "rnsit_content.pdf"

# Function to extract text from PDF
def extract_pdf_text(file_path):
  try:
    with open(file_path, 'rb') as pdf_file_obj:
      pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
      text = ""
      for page in pdf_reader.pages:
        text += page.extract_text()
      return text
  except FileNotFoundError:
    print("Error: PDF file not found!")
    return ""

# Load the knowledge base from the PDF
knowledge = extract_pdf_text(pdf_file)


genai.configure(api_key="AIzaSyDAG9BXn9U17DRPQoH0VSQ1NWelfgklBwc")

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction=(f"{knowledge}You are integrated as a chatbot of RNSIT college that has below knowledge of college. you answer all the qeuries of teacheers and students soley using this knowledge only ." )
)



chat_session = model.start_chat(
    history=[]
)

print("Mohammed AI: Hello, how can I help you?")
print()
while True:

    user_input = input("You: ")
    print()

    response = chat_session.send_message(user_input)

    model_response = response.text

    print(f'Bot: {model_response}')
    print()

    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})