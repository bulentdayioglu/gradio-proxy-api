from flask import Flask, request, jsonify
from gradio_client import Client, handle_file

app = Flask(__name__)

client = Client("AAAAA12344321/GardenGuard")  # Gradio Space ID doğru yaz!

@app.route('/')
def index():
    return '✅ API is working!'

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    result = client.predict(
        image=handle_file(file),
        api_name="/predict"
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
