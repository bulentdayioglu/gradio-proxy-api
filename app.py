import os
import base64
from flask import Flask, request, jsonify
from gradio_client import Client

app = Flask(__name__)

client = Client("AAAAA12344321/GardenGuard") # Gradio Space ID'nizi doğru yazdığınızdan emin olun

@app.route('/')
def index():
    return '✅ API is working!'

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']

    try:
        # 1. Yüklenen dosyanın içeriğini byte olarak oku (diske kaydetme).
        image_bytes = file.read()
        
        # 2. Byte'ları Base64 formatına kodla.
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # 3. Gradio API'sinin beklediği standart "data URI" formatını oluştur.
        # file.mimetype (örn: 'image/png') dosyanın türünü belirtir.
        data_uri = f"data:{file.mimetype};base64,{base64_image}"

        # 4. client.predict fonksiyonuna bu data URI'ını ver.
        # Gradio bu formatı doğrudan anlar.
        result = client.predict(
            image=data_uri,
            api_name="/predict"
        )
        
        return jsonify(result)

    except Exception as e:
        # Olası bir hata durumunda detaylı loglama yap.
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
