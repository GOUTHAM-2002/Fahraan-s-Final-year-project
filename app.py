from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
import PyPDF2

app = Flask(__name__)

# Define the PDF file path
pdf_file = "meow.pdf"


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

# Configure the Generative AI API
genai.configure(api_key="meow")

# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=(
        f"{knowledge}You are integrated as a chatbot of RNSIT college that has below knowledge of the college. You answer all queries of teachers and students solely using this knowledge only."
    )
)

# Initialize a chat session
chat_session = model.start_chat(history=[])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user's input from the request
        user_input = request.json.get('user_input')

        if not user_input:
            return jsonify({"error": "No user input provided!"}), 400

        # Generate a response
        response = chat_session.send_message(user_input)
        model_response = response.text

        # Update the chat history
        chat_session.history.append({"role": "user", "parts": [user_input]})
        chat_session.history.append({"role": "model", "parts": [model_response]})

        # Return the response as JSON
        return jsonify({"response": model_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)