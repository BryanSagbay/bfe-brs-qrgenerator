import React from 'react';
import { Download, Palette, Loader2 } from 'lucide-react';

export default function PreviewPanel({ qrDataUrl, qrSize, loading, error }) {
  const downloadQR = () => {
    if (qrDataUrl) {
      const link = document.createElement('a');
      link.download = 'qrcode.png';
      link.href = qrDataUrl;
      link.click();
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
      <h2 className="text-2xl font-semibold mb-6 text-gray-800">
        Vista Previa
      </h2>

      <div className="flex flex-col items-center justify-center min-h-[400px]">
        {loading ? (
          <div className="text-center">
            <Loader2 size={64} className="mx-auto mb-4 animate-spin text-purple-600" />
            <p className="text-lg text-gray-600">Generando QR...</p>
          </div>
        ) : error ? (
          <div className="text-center text-red-500">
            <p className="text-lg font-medium">Error</p>
            <p className="text-sm mt-2">{error}</p>
          </div>
        ) : qrDataUrl ? (
          <div className="space-y-6 w-full">
            <div className="bg-gray-50 p-8 rounded-xl flex justify-center">
              <img
                src={qrDataUrl}
                alt="QR Code"
                className="max-w-full h-auto rounded-lg shadow-lg"
                style={{ width: qrSize, height: qrSize }}
              />
            </div>
            <button
              onClick={downloadQR}
              className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
              <Download size={20} />
              Descargar QR
            </button>
          </div>
        ) : (
          <div className="text-center text-gray-400">
            <Palette size={64} className="mx-auto mb-4 opacity-50" />
            <p className="text-lg">Ingresa una URL para generar el QR</p>
          </div>
        )}
      </div>
    </div>
  );
}