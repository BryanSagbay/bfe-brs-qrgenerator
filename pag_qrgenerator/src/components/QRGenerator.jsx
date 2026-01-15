import React, { useState, useEffect } from 'react';
import { useQRGenerator } from '../hooks/useQRGenerator';
import ConfigPanel from './ConfigPanel';
import PreviewPanel from './PreviewPanel';

export default function QRGenerator() {
  const [url, setUrl] = useState('');
  const [logo, setLogo] = useState(null);
  const [qrColor, setQrColor] = useState('#000000');
  const [bgColor, setBgColor] = useState('#ffffff');
  const [qrSize, setQrSize] = useState(300);
  const [errorLevel, setErrorLevel] = useState('H'); // Cambié a 'H' para mejor corrección con logo

  const { qrDataUrl, loading, error, generateQR, resetQR } = useQRGenerator();

  useEffect(() => {
    const debounce = setTimeout(() => {
      if (url) {
        const options = {
          fillColor: qrColor,
          backColor: bgColor,
          errorLevel: logo ? 'H' : errorLevel, // Usa nivel alto si hay logo
          boxSize: Math.floor(qrSize / 30),
          border: 4,
          // Opciones adicionales para el logo
          logoSize: logo ? 0.2 : 0, // 20% del tamaño del QR
          logoMargin: logo ? 10 : 0, // Margen alrededor del logo
          quietZone: logo ? 15 : 4 // Zona tranquila más grande con logo
        };
        generateQR(url, options, logo);
      } else {
        resetQR();
      }
    }, 500);

    return () => clearTimeout(debounce);
  }, [url, qrColor, bgColor, qrSize, errorLevel, logo, generateQR, resetQR]);

  const handleReset = () => {
    setUrl('');
    setLogo(null);
    setQrColor('#000000');
    setBgColor('#ffffff');
    setQrSize(300);
    setErrorLevel('M');
    resetQR();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Título */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-3">
            Generador de Códigos QR
          </h1>
          <p className="text-gray-600 text-base md:text-lg">
            Crea códigos QR personalizados con logo y colores
          </p>
        </div>

        {/* Grid Principal */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Configuración - Izquierda */}
          <div className="order-2 lg:order-1">
            <ConfigPanel
              url={url}
              setUrl={setUrl}
              logo={logo}
              setLogo={setLogo}
              qrColor={qrColor}
              setQrColor={setQrColor}
              bgColor={bgColor}
              setBgColor={setBgColor}
              qrSize={qrSize}
              setQrSize={setQrSize}
              errorLevel={errorLevel}
              setErrorLevel={setErrorLevel}
              onReset={handleReset}
            />
          </div>

          {/* Vista Previa - Derecha */}
          <div className="order-1 lg:order-2">
            <div className="lg:sticky lg:top-8">
              <PreviewPanel
                qrDataUrl={qrDataUrl}
                qrSize={qrSize}
                loading={loading}
                error={error}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}