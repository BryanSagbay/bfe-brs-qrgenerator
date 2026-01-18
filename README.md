# 🎯 BFE-BRS QR Generator

Generador de códigos QR personalizados con soporte para logos y múltiples opciones de diseño.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![React](https://img.shields.io/badge/React-18+-61dafb.svg)
![Vite](https://img.shields.io/badge/Vite-5+-646cff.svg)

## ✨ Características

- 🎨 **Personalización completa**: Colores, tamaño y nivel de corrección de errores
- 🖼️ **Logos integrados**: Agrega tu marca con detección automática de forma (cuadrado/rectangular)
- 📱 **Responsive**: Interfaz adaptable a cualquier dispositivo
- ⚡ **Rápido**: Generación instantánea de códigos QR
- 💾 **Descarga directa**: Exporta en formato PNG de alta calidad

## 🛠️ Tecnologías

### Backend
- Python 3.8+
- Flask 3.0+
- Pillow (PIL)
- python-qrcode
- Flask-CORS

### Frontend
- React 18+
- Vite 5+
- Tailwind CSS
- Axios

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior
- Node.js 18 o superior
- npm o yarn

### 1. Clonar el repositorio
```bash
git clone https://github.com/BryanSagbay/bfe-brs-qrgenerator.git
cd bfe-brs-qrgenerator
```

### 2. Configurar Backend (Flask)

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env (ver sección de configuración)
cp .env.example .env

# Ejecutar servidor
python app.py
```

El backend estará disponible en `http://localhost:5000`

### 3. Configurar Frontend (React)

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

## 📝 Configuración

### Variables de Entorno

Crear archivo **`backend/.env`**:
```env
SECRET_KEY=tu-clave-secreta-super-segura-aqui
FLASK_ENV=development
FLASK_APP=app.py
PORT=5000
```

Crear archivo **`frontend/.env`** (opcional):
```env
VITE_API_URL=http://localhost:5000
```

## 📖 Uso

### API Endpoints

#### Generar QR Code
```http
POST /api/qr/generate
Content-Type: application/json

{
  "url": "https://ejemplo.com",
  "options": {
    "errorLevel": "H",
    "boxSize": 10,
    "border": 4,
    "fillColor": "black",
    "backColor": "white"
  },
  "logo": "data:image/png;base64,..." // Opcional
}
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "qr_code": "data:image/png;base64,..."
}
```

#### Health Check
```http
GET /api/qr/health
```

### Niveles de Corrección de Errores

| Nivel | Descripción | Uso recomendado |
|-------|-------------|------------------|
| `L` | ~7% recuperación | QR simples sin logo |
| `M` | ~15% recuperación | Uso general |
| `Q` | ~25% recuperación | QR con diseños |
| `H` | ~30% recuperación | **Requerido para logos** |

## 🎨 Características del Logo

- **Formato soportado**: PNG, JPG, JPEG (se recomienda PNG con transparencia)
- **Tamaño recomendado**: 200x200px a 500x500px
- **Detección automática**: 
  - Logos cuadrados → área circular
  - Logos rectangulares → área rectangular con esquinas redondeadas
- **Margen adaptativo**: Se ajusta automáticamente según las dimensiones del logo

## 📦 Estructura del Proyecto

```
bfe-brs-qrgenerator/
├── backend/
│   ├── app.py                 # Aplicación principal Flask
│   ├── requirements.txt       # Dependencias Python
│   ├── .env                   # Variables de entorno
│   ├── routes/
│   │   └── qr_routes.py      # Rutas de la API
│   └── utils/
│       └── qr_generator.py   # Lógica de generación QR
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Componente principal
│   │   ├── components/       # Componentes React
│   │   └── api/              # Servicios API
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run test
```

## 🚢 Despliegue

### Backend (Flask)
```bash
# Producción con Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend (React)
```bash
npm run build
# Los archivos se generan en dist/
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Bryan Sagbay** - *Trabajo Inicial* - [BryanSagbay](https://github.com/BryanSagbay)

## 🙏 Agradecimientos

- [python-qrcode](https://github.com/lincolnloop/python-qrcode) - Librería de generación QR
- [Pillow](https://python-pillow.org/) - Procesamiento de imágenes
- [React](https://react.dev/) - Framework frontend
- [Vite](https://vitejs.dev/) - Build tool

## 📞 Soporte

Si tienes problemas o preguntas:
- 📧 Email: bryansagbay01@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/BryanSagbay/bfe-brs-qrgenerator/issues)

---
