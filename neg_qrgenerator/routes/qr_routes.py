from flask import Blueprint, request, jsonify
from utils.qr_generator import QRGenerator
from PIL import Image
import io

qr_bp = Blueprint('qr', __name__)
qr_gen = QRGenerator()

@qr_bp.route('/generate', methods=['POST'])
def generate_qr():
    """
    Endpoint para generar código QR
    Body: {
        "url": "https://example.com",
        "options": {
            "fillColor": "#000000",
            "backColor": "#ffffff",
            "errorLevel": "M",
            "boxSize": 10,
            "border": 4
        },
        "logo": "base64_image_string" (opcional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL es requerida'}), 400
        
        url = data['url']
        options = data.get('options', {})
        logo_base64 = data.get('logo')
        
        # Generar QR básico
        qr_image = qr_gen.generate_qr(url, options)
        
        # Añadir logo si existe
        if logo_base64:
            try:
                logo_image = qr_gen.base64_to_image(logo_base64)
                qr_image = qr_gen.add_logo_to_qr(qr_image, logo_image)
            except Exception as e:
                return jsonify({'error': f'Error procesando logo: {str(e)}'}), 400
        
        # Convertir a base64
        qr_base64 = qr_gen.image_to_base64(qr_image)
        
        return jsonify({
            'success': True,
            'qr_code': qr_base64
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@qr_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de salud"""
    return jsonify({'status': 'ok'}), 200