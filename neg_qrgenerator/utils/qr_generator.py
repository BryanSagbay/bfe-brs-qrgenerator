import qrcode
from PIL import Image, ImageDraw
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
    
    def add_logo_to_qr(self, qr_image, logo_image, logo_size_percent=0.25):
        """
        Añade un logo al centro del código QR con área limpia automática
        que se adapta a la forma del logo
        """
        # Convertir QR a RGB
        qr_image = qr_image.convert('RGB')
        qr_width, qr_height = qr_image.size
        
        # Obtener color de fondo del QR
        bg_color = qr_image.getpixel((0, 0))
        
        # Preparar logo
        logo_image = logo_image.convert('RGBA')
        
        # Calcular tamaño máximo para el logo
        max_logo_size = int(min(qr_width, qr_height) * logo_size_percent * 0.7)
        
        # Redimensionar logo manteniendo su proporción original
        logo_image.thumbnail((max_logo_size, max_logo_size), Image.Resampling.LANCZOS)
        logo_width, logo_height = logo_image.size
        
        # Calcular centro del QR
        center_x = qr_width // 2
        center_y = qr_height // 2
        
        # Detectar proporción del logo
        aspect_ratio = logo_width / logo_height
        
        # PADDING ADAPTATIVO según la forma del logo
        if 0.85 <= aspect_ratio <= 1.15:
            # Logo casi cuadrado -> usar forma circular/cuadrada
            # Usar el lado mayor como referencia
            max_side = max(logo_width, logo_height)
            padding = int(max_side * 0.5)  # 50% de padding uniforme
            
            # Área cuadrada
            total_size = max_side + (padding * 2)
            
            clean_area_bbox = [
                center_x - (total_size // 2),
                center_y - (total_size // 2),
                center_x + (total_size // 2),
                center_y + (total_size // 2)
            ]
            
            # Radio más grande para forma más circular
            corner_radius = int(total_size * 0.4)
            
        else:
            # Logo rectangular -> área rectangular que sigue la proporción
            # Padding proporcional a cada dimensión
            padding_x = int(logo_width * 0.45)
            padding_y = int(logo_height * 0.45)
            
            total_width = logo_width + (padding_x * 2)
            total_height = logo_height + (padding_y * 2)
            
            clean_area_bbox = [
                center_x - (total_width // 2),
                center_y - (total_height // 2),
                center_x + (total_width // 2),
                center_y + (total_height // 2)
            ]
            
            # Radio más pequeño para rectangulares
            corner_radius = int(min(total_width, total_height) * 0.2)
        
        # Crear capa de dibujo
        draw = ImageDraw.Draw(qr_image)
        
        # Dibujar el área limpia con esquinas redondeadas
        draw.rounded_rectangle(
            clean_area_bbox, 
            radius=corner_radius, 
            fill=bg_color,
            outline=bg_color,
            width=2
        )
        
        # Calcular posición del logo (siempre centrado)
        logo_x = center_x - (logo_width // 2)
        logo_y = center_y - (logo_height // 2)
        
        # Pegar el logo
        if logo_image.mode == 'RGBA':
            # Crear fondo del color del QR
            logo_bg = Image.new('RGB', logo_image.size, bg_color)
            # Pegar logo con transparencia
            logo_bg.paste(logo_image, (0, 0), logo_image.split()[3])
            qr_image.paste(logo_bg, (logo_x, logo_y))
        else:
            qr_image.paste(logo_image.convert('RGB'), (logo_x, logo_y))
        
        return qr_image
    
    def image_to_base64(self, img):
        """
        Convierte una imagen PIL a base64
        """
        buffered = io.BytesIO()
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    
    def base64_to_image(self, base64_string):
        """
        Convierte base64 a imagen PIL
        """
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        img_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(img_data))