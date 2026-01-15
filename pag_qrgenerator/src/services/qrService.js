import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;


export const qrService = {
  generateQR: async (url, options, logo = null) => {
    try {
      const response = await axios.post(`${API_URL}/generate`, {
        url,
        options,
        logo
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error generando QR');
    }
  },

  checkHealth: async () => {
    try {
      const response = await axios.get(`${API_URL}/health`);
      return response.data;
    } catch (error) {
      throw new Error(error || 'Backend no disponible');
    }
  }
};