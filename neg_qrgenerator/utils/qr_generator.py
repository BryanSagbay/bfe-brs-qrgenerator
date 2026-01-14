import qrcode
from PIL import Image
import io
import base64

class QRGenerator:
    def __init__(self):
        self.error_correction_levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H
        }
    
    def generate_qr(self, url, options=None):
        """
        Genera un código QR básico
        """
        if options is None:
            options = {}
        
        error_level = self.error_correction_levels.get(
            options.get('errorLevel', 'M'),
            qrcode.constants.ERROR_CORRECT_M
        )
        
        qr = qrcode.QRCode(
            version=options.get('version', 1),
            error_correction=error_level,
            box_size=options.get('boxSize', 10),
            border=options.get('border', 4)
        )
        
        qr.add_data(url)
        qr.make(fit=True)
        
        # Crear imagen con colores personalizados
        fill_color = options.get('fillColor', 'black')
        back_color = options.get('backColor', 'white')
        
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        return img
    
    def add_logo_to_qr(self, qr_image, logo_image, logo_size_percent=0.3):
        """
        Añade un logo al centro del código QR
        """
        # Convertir a RGBA si es necesario
        qr_image = qr_image.convert('RGBA')
        logo_image = logo_image.convert('RGBA')
        
        # Calcular tamaño del logo
        qr_width, qr_height = qr_image.size
        logo_max_size = int(min(qr_width, qr_height) * logo_size_percent)
        
        # Redimensionar logo manteniendo proporción
        logo_image.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
        
        # Calcular posición central
        logo_width, logo_height = logo_image.size
        logo_position = (
            (qr_width - logo_width) // 2,
            (qr_height - logo_height) // 2
        )
        
        # Crear un fondo blanco para el logo
        background = Image.new('RGBA', (logo_width + 20, logo_height + 20), 'white')
        background.paste(logo_image, (10, 10), logo_image)
        
        # Pegar el logo con fondo en el QR
        bg_position = (
            (qr_width - background.width) // 2,
            (qr_height - background.height) // 2
        )
        qr_image.paste(background, bg_position, background)
        
        return qr_image
    
    def image_to_base64(self, img):
        """
        Convierte una imagen PIL a base64
        """
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def base64_to_image(self, base64_string):
        """
        Convierte base64 a imagen PIL
        """
        # Remover el prefijo data:image si existe
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        img_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(img_data))