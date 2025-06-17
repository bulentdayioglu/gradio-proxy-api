import os
import base64
import requests
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Flutter uygulamasından gelen isteklere izin ver

GRADIO_API_URL = "https://AAAAA12344321-gardenguard.hf.space/run/predict"  # KENDİ URL'NİZİ KONTROL EDİN

@app.route('/')
def index():
    return '✅ API is working!'

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    # Dosya türü kontrolü
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400

    try:
        # Dosya içeriğini al
        image_bytes = file.read()
        
        # Geçici dosya oluştur
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name

        # Multipart form data ile Hugging Face API'ye gönder
        with open(temp_file_path, 'rb') as f:
            files = {'file': (file.filename, f, file.mimetype)}
            response = requests.post(GRADIO_API_URL, files=files, timeout=30)
        
        # Geçici dosyayı sil
        os.unlink(temp_file_path)
        
        response.raise_for_status()
        
        print(f"✅ Hugging Face API yanıtı: {response.status_code}")
        return jsonify(response.json())

    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP Error: {http_err}")
        return jsonify({
            'error': f'Hugging Face API Error: {http_err}', 
            'details': response.text if 'response' in locals() else 'No response details'
        }), response.status_code if 'response' in locals() else 500
    except requests.exceptions.Timeout:
        print("❌ Timeout Error")
        return jsonify({'error': 'Request timeout. Please try again.'}), 408
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error")
        return jsonify({'error': 'Connection error. Please check your internet connection.'}), 503
    except Exception as e:
        print(f"❌ General Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Proxy server is running'})

if __name__ == "__main__":
    print("🚀 Proxy server başlatılıyor...")
    print(f"📡 Hugging Face API URL: {GRADIO_API_URL}")
    print("🌐 Server: http://localhost:3000")
    app.run(host="0.0.0.0", port=3000, debug=True)
