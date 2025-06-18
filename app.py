#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client, handle_file
import os
import tempfile
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Flutter'dan çağırabilmek için

# Gradio client'ı başlat
try:
    client = Client("AAAAA12344321/GardenGuard")
    print("✅ Gradio client başlatıldı!")
except Exception as e:
    print(f"❌ Gradio client hatası: {e}")
    client = None

@app.route('/health', methods=['GET'])
def health_check():
    """Sunucu sağlık kontrolü"""
    return jsonify({
        "status": "healthy",
        "gradio_client": "connected" if client else "disconnected"
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Plant disease prediction endpoint"""
    try:
        if not client:
            return jsonify({
                "success": False,
                "error": "Gradio client not available"
            }), 500

        # JSON request'ten image URL/path al
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'image' field in request"
            }), 400

        image_input = data['image']
        
        # Görüntüdeki doğru API formatını kullan
        result = client.predict(
            image=handle_file(image_input),
            api_name="/predict"
        )
        
        # Sonucu formatla
        return jsonify({
            "success": True,
            "data": result,
            "model": "AAAAA12344321/GardenGuard"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/predict-file', methods=['POST'])
def predict_file():
    """Dosya upload ile prediction"""
    try:
        if not client:
            return jsonify({
                "success": False,
                "error": "Gradio client not available"
            }), 500

        # Dosya upload kontrolü
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "error": "No file uploaded"
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400

        # Güvenli dosya adı
        filename = secure_filename(file.filename)
        
        # Temp dosyaya kaydet
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        try:
            # Doğru API formatı ile prediction yap
            result = client.predict(
                image=handle_file(temp_path),
                api_name="/predict"
            )
            
            return jsonify({
                "success": True,
                "data": result,
                "model": "AAAAA12344321/GardenGuard"
            })
        finally:
            # Temp dosyayı sil
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """API info"""
    return jsonify({
        "name": "GardenGuard Plant Disease Detection API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "GET - Health check",
            "/predict": "POST - Predict with image URL/path",
            "/predict-file": "POST - Predict with file upload"
        },
        "model": "AAAAA12344321/GardenGuard",
        "status": "running"
    })

# Vercel için uyumluluk - serverless function olarak çalışacak
if __name__ == '__main__':
    # Local development için
    print("🌱 GardenGuard API Server")
    print("🚀 Starting server on http://localhost:5001")
    print("📖 API docs: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True) 
