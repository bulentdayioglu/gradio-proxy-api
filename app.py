import os
import base64
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GRADIO_API_URL = "https://AAAAA12344321-gardenguard.hf.space/run/predict" # KENDİ URL'NİZİ KONTROL EDİN

@app.route('/')
def index():
    return '✅ API is working!'

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']

    try:
        # Dosya içeriğini ve boyutunu al
        image_bytes = file.read()
        file_size = len(image_bytes)
        
        # Base64 data URI'ını oluştur
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        data_uri = f"data:{file.mimetype};base64,{base64_image}"

        # !!!! YENİ KISIM: DOĞRUDAN BİR SÖZLÜK (DICTIONARY) OLUŞTURUYORUZ !!!!
        # Bu, Gradio'nun dahili olarak bir dosyayı temsil etme şekline çok benzer.
        image_payload_dict = {
            "name": file.filename,
            "data": data_uri,
            "size": file_size,
            "is_file": True,
        }

        # Hugging Face API'sinin beklediği nihai JSON payload'ını bu sözlük ile oluştur
        payload = {
            "data": [
                image_payload_dict # Metin yerine sözlük gönderiyoruz
            ]
        }
        
        # Requests kütüphanesi ile doğrudan API'ye POST isteği at
        response = requests.post(GRADIO_API_URL, json=payload)
        response.raise_for_status()
        
        return jsonify(response.json())

    except requests.exceptions.HTTPError as http_err:
        return jsonify({
            'error': f'Hugging Face API Error: {http_err}', 
            'details': response.text
        }), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
