import React from 'react';
import api from '../services/api';

const DownloadCertificateButton = ({ courseId }) => {
  const handleDownload = async () => {
    try {
      const res = await api.get(`/certificate/${courseId}/`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `/certificate_${courseId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Certificate download error:', err);
      alert('Sertifikatni olishda xatolik yuz berdi.');
    }
  };

  return <button onClick={handleDownload} className='btn btn-info'>Serfikat olish</button>;
};

export default DownloadCertificateButton;
