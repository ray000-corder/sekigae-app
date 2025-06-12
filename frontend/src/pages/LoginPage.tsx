import { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

function LoginPage() {
  // ... (handleLoginなどの関数は変更なし) ...
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: username,
        password: password,
      });
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      navigate('/');
    } catch (error) {
      console.error('ログインエラー:', error);
      alert('ログインに失敗しました。ユーザー名かパスワードを確認してください。');
    }
  };


  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold text-center mb-6">ログイン</h2>
        <form onSubmit={handleLogin}>
          {/* ... (フォームの中身は変更なし) ... */}
          <div className="mb-4">
            <label className="block text-gray-700 mb-2" htmlFor="username">ユーザー名</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-indigo-200"
              required
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 mb-2" htmlFor="password">パスワード</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-indigo-200"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition duration-200"
          >
            ログイン
          </button>
        </form>
        <div className="text-center mt-4">
          <p className="text-sm">
            アカウントをお持ちでないですか？ <Link to="/register" className="text-indigo-500 hover:underline">新規登録</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
