from flask import Flask, request, jsonify 
import ollama

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/test')
def test():
    return 'test'

@app.route('/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()  # Get JSON data from the request body

        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text data in request body'}), 400

        text = data['text']

        chunk_embeddings_data = []

        vector_embedding = ollama.embeddings(model='nomic-embed-text', prompt=text)

        chunk_embeddings_data.append({
            "text": text,
            "vector_embedding": vector_embedding['embedding']
        })

        return chunk_embeddings_data

    except Exception as e:
        print(f"Error embedding text: {text}. Error: {e}")
        # Handle the error appropriately, e.g., skip the chunk or log the error
        chunk_embeddings_data.append({ # Store even if embedding fails, but mark it
            "text": text,
            "vector_embedding": None, # Or some error marker
            "error": str(e)
        })

        return jsonify({'error': str(e)}), 500  # Return a 500 error with the exception message

if __name__ == '__main__':
    app.run(debug=True)

