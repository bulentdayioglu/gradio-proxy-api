from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '✅ API is working!'

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    # Dosya bilgilerini geri döndür (sadece test)
    file = request.files['image']
    return jsonify({'filename': file.filename, 'content_type': file.content_type})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
