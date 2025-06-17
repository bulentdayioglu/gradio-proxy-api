import os
import base64
import requests # Yeni import
from flask import Flask, request, jsonify

app = Flask(__name__)

# !!! ÇOK ÖNEMLİ: BU URL'Yİ KENDİ HUGGING FACE SPACE'İNİZDEN ALMALISINIZ !!!
# Nasıl bulunur: Hugging Face'de Space sayfanıza gidin -> Sağ üstteki üç noktaya (...) tıklayın
# -> "Embed this Space" seçeneğini seçin -> "Direct API URL" kısmındaki URL'yi kopyalayın.
# URL genellikle /run/predict ile biter.
GRADIO_API_URL = "https://AAAAA12344321-gardenguard.hf.space/run/predict" # KENDİ URL'NİZİ YAPIŞTIRIN

@app.route('/')
def index():
    return '✅ API is working!'

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']

    try:
        # Resmi Base64 data URI formatına çevir
        image_bytes = file.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        data_uri = f"data:{file.mimetype};base64,{base64_image}"

        # Hugging Face API'sinin beklediği nihai JSON payload'ını oluştur
        payload = {
            "data": [
                data_uri
            ]
        }
        
        # Requests kütüphanesi ile doğrudan API'ye POST isteği at
        response = requests.post(GRADIO_API_URL, json=payload)
        
        # Hugging Face'den gelen yanıtı kontrol et
        response.raise_for_status()  # Eğer 2xx dışında bir yanıt varsa (4xx, 5xx), hata fırlat
        
        # Başarılı yanıtı olduğu gibi istemciye (Dart) geri döndür
        return jsonify(response.json())

    except requests.exceptions.HTTPError as http_err:
        # Hugging Face'den gelen bir hata varsa (örn: 422 Unprocessable Entity)
        return jsonify({
            'error': f'Hugging Face API Error: {http_err}', 
            'details': response.text
        }), response.status_code
    except Exception as e:
        # Diğer beklenmedik hatalar için
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
