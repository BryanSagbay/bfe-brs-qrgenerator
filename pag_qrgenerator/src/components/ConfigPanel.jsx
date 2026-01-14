import React, { useRef } from 'react';
import { Upload, RotateCcw } from 'lucide-react';
import ColorPicker from './ColorPicker';

export default function ConfigPanel({
  url,
  setUrl,
  logo,
  setLogo,
  qrColor,
  setQrColor,
  bgColor,
  setBgColor,
  qrSize,
  setQrSize,
  errorLevel,
  setErrorLevel,
  onReset
}) {
  const logoInputRef = useRef(null);

  const handleLogoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setLogo(event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6">
      <h2 className="text-2xl font-semibold mb-6 text-gray-800">
        Configuración
      </h2>

      {/* URL Input */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          URL o Texto *
        </label>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://ejemplo.com"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
        />
      </div>

      {/* Logo Upload */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Logo (Opcional)
        </label>
        <div className="flex items-center gap-3">
          <input
            ref={logoInputRef}
            type="file"
            accept="image/*"
            onChange={handleLogoUpload}
            className="hidden"
            id="logo-upload"
          />
          <label
            htmlFor="logo-upload"
            className="flex-1 px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-purple-500 transition-colors flex items-center justify-center gap-2"
          >
            <Upload size={20} />
            <span className="text-sm">
              {logo ? 'Cambiar logo' : 'Cargar logo'}
            </span>
          </label>
          {logo && (
            <button
              onClick={() => {
                setLogo(null);
                if (logoInputRef.current) logoInputRef.current.value = '';
              }}
              className="px-4 py-3 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors"
            >
              Quitar
            </button>
          )}
        </div>
        {logo && (
          <div className="mt-3 flex justify-center">
            <img
              src={logo}
              alt="Logo preview"
              className="w-20 h-20 object-contain border rounded-lg"
            />
          </div>
        )}
      </div>

      {/* Colores */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <ColorPicker
          label="Color QR"
          value={qrColor}
          onChange={setQrColor}
        />
        <ColorPicker
          label="Color Fondo"
          value={bgColor}
          onChange={setBgColor}
        />
      </div>

      {/* Tamaño */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Tamaño: {qrSize}px
        </label>
        <input
          type="range"
          min="200"
          max="600"
          step="50"
          value={qrSize}
          onChange={(e) => setQrSize(Number(e.target.value))}
          className="w-full accent-purple-600"
        />
      </div>

      {/* Nivel de Corrección */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Nivel de Corrección de Errores
        </label>
        <select
          value={errorLevel}
          onChange={(e) => setErrorLevel(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
        >
          <option value="L">Bajo (7%)</option>
          <option value="M">Medio (15%)</option>
          <option value="Q">Alto (25%)</option>
          <option value="H">Muy Alto (30%)</option>
        </select>
      </div>

      {/* Botón Reset */}
      <button
        onClick={onReset}
        className="w-full px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors flex items-center justify-center gap-2 font-medium"
      >
        <RotateCcw size={20} />
        Resetear Todo
      </button>
    </div>
  );
}