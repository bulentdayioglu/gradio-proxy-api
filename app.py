import os
from flask import Flask, request, jsonify
from gradio_client import Client

app = Flask(__name__)

# NOT: Artık handle_file'a ihtiyacımız yok çünkü gradio_client dosya yolunu doğrudan işleyebilir.
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
        # 1. Yüklenen dosyayı Vercel'in geçici /tmp klasörüne kaydet.
        # Bu, dosyaya sunucu içinde bir "dosya yolu" verir.
        filepath = os.path.join("/tmp", file.filename)
        file.save(filepath)

        # 2. client.predict fonksiyonuna artık obje değil, dosyanın yolunu ver.
        result = client.predict(
            image=filepath,
            api_name="/predict"
        )
        
        return jsonify(result)

    except Exception as e:
        # Olası bir hata durumunda daha detaylı loglama yapalım.
        return jsonify({'error': str(e)}), 500
    
    finally:
        # 3. (İsteğe bağlı ama iyi bir pratik) İşlem bittikten sonra geçici dosyayı sil.
        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
