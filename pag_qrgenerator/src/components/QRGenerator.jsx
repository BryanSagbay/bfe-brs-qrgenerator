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
  const [errorLevel, setErrorLevel] = useState('M');

  const { qrDataUrl, loading, error, generateQR, resetQR } = useQRGenerator();

  useEffect(() => {
    const debounce = setTimeout(() => {
      if (url) {
        const options = {
          fillColor: qrColor,
          backColor: bgColor,
          errorLevel: errorLevel,
          boxSize: Math.floor(qrSize / 30),
          border: 4
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
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Generador de Códigos QR
          </h1>
          <p className="text-gray-600">
            Crea códigos QR personalizados con logo y colores
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
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

          <PreviewPanel
            qrDataUrl={qrDataUrl}
            qrSize={qrSize}
            loading={loading}
            error={error}
          />
        </div>
      </div>
    </div>
  );
}