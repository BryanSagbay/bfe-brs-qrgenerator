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
    
    def detect_logo_shape(self, logo_image):
        """
        Detecta si el logo es más circular/cuadrado o rectangular
        Retorna 'circle' para logos cuadrados/circulares o 'rectangle' para rectangulares
        """
        width, height = logo_image.size
        aspect_ratio = width / height
        
        # Rango más estricto para detectar cuadrados
        if 0.90 <= aspect_ratio <= 1.10:
            return 'circle'
        else:
            return 'rectangle'
    
    def add_logo_to_qr(self, qr_image, logo_image, logo_size_percent=0.25):
        """
        Añade un logo al centro del código QR creando un área blanca limpia
        El área blanca se dibuja PRIMERO para crear el "hueco" y luego se coloca el logo
        """
        # Convertir QR a RGB y obtener color de fondo
        qr_image = qr_image.convert('RGB')
        qr_width, qr_height = qr_image.size
        
        # Obtener color de fondo del QR (esquina superior izquierda)
        bg_color = qr_image.getpixel((0, 0))
        
        # Preparar logo
        logo_image = logo_image.convert('RGBA')
        
        # Detectar forma del logo
        logo_shape = self.detect_logo_shape(logo_image)
        
        # Calcular tamaño del área contenedora (más grande para el espacio blanco)
        container_size = int(min(qr_width, qr_height) * logo_size_percent)
        
        # Redimensionar logo (será más pequeño que el contenedor)
        logo_max_size = int(container_size * 0.65)  # Logo ocupa 65% del área
        logo_image.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
        logo_width, logo_height = logo_image.size
        
        # Crear el "hueco" blanco según la forma
        if logo_shape == 'circle':
            # CÍRCULO BLANCO para logos cuadrados
            circle_size = int(container_size * 1.3)  # Más grande para el margen
            
            # Crear máscara circular
            mask = Image.new('L', (circle_size, circle_size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, circle_size - 1, circle_size - 1), fill=255)
            
            # Crear círculo blanco sólido
            white_circle = Image.new('RGB', (circle_size, circle_size), bg_color)
            
            # Calcular posición central del círculo
            circle_x = (qr_width - circle_size) // 2
            circle_y = (qr_height - circle_size) // 2
            
            # PASO 1: Pegar el círculo blanco (crear el hueco)
            qr_image.paste(white_circle, (circle_x, circle_y), mask)
            
            # PASO 2: Pegar el logo centrado sobre el círculo blanco
            logo_x = (qr_width - logo_width) // 2
            logo_y = (qr_height - logo_height) // 2
            
        else:
            # RECTÁNGULO REDONDEADO para logos rectangulares
            # Calcular dimensiones del rectángulo con padding
            padding = int(logo_max_size * 0.25)  # 25% de padding
            rect_width = logo_width + (padding * 2)
            rect_height = logo_height + (padding * 2)
            
            # Crear máscara rectangular con bordes redondeados
            radius = int(min(rect_width, rect_height) * 0.2)  # Radio 20%
            mask = Image.new('L', (rect_width, rect_height), 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle(
                [(0, 0), (rect_width - 1, rect_height - 1)],
                radius=radius,
                fill=255
            )
            
            # Crear rectángulo blanco sólido
            white_rect = Image.new('RGB', (rect_width, rect_height), bg_color)
            
            # Calcular posición central del rectángulo
            rect_x = (qr_width - rect_width) // 2
            rect_y = (qr_height - rect_height) // 2
            
            # PASO 1: Pegar el rectángulo blanco (crear el hueco)
            qr_image.paste(white_rect, (rect_x, rect_y), mask)
            
            # PASO 2: Pegar el logo centrado sobre el rectángulo blanco
            logo_x = rect_x + padding
            logo_y = rect_y + padding
        
        # Pegar el logo sobre el área blanca
        if logo_image.mode == 'RGBA':
            # Si tiene transparencia, crear versión RGB
            logo_rgb = Image.new('RGB', logo_image.size, bg_color)
            logo_rgb.paste(logo_image, mask=logo_image.split()[3])
            qr_image.paste(logo_rgb, (logo_x, logo_y))
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