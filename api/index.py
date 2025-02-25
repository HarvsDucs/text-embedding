from flask import Flask, request, jsonify 

from openai import OpenAI

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()  # Get JSON data from the request body

        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text data in request body'}), 400

        text = data['text']

        client = OpenAI()

        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )

        return response.data[0].embedding

    except Exception as e:
        print(f"Error embedding text: {text}. Error: {e}")

        return jsonify({'error': str(e)}), 500  # Return a 500 error with the exception message

if __name__ == '__main__':
    app.run(debug=True)

