import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://sekigae-backend.onrender.com',
});

apiClient.interceptors.request.use(async (config) => {
  const accessToken = localStorage.getItem('access_token');
  
  // ↓ 監視カメラ1
  console.log('インターセプターがトークンをチェック中:', accessToken); 
  
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
    // ↓ 監視カメラ2
    console.log('ヘッダーにトークンをセットしました！'); 
  }
  
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default apiClient;