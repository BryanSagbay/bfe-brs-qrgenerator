import { useState, useCallback } from 'react';
import { qrService } from '../services/qrService';

export const useQRGenerator = () => {
  const [qrDataUrl, setQrDataUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateQR = useCallback(async (url, options, logo) => {
    if (!url) {
      setQrDataUrl('');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await qrService.generateQR(url, options, logo);
      setQrDataUrl(result.qr_code);
    } catch (err) {
      setError(err.message);
      setQrDataUrl('');
    } finally {
      setLoading(false);
    }
  }, []);

  const resetQR = useCallback(() => {
    setQrDataUrl('');
    setError(null);
  }, []);

  return {
    qrDataUrl,
    loading,
    error,
    generateQR,
    resetQR
  };
};