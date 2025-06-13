import { useState } from "react";
import apiClient from "../api/axiosConfig";
import { useNavigate, Link } from "react-router-dom";

function RegisterPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState(""); // 確認用パスワード
  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // パスワードが一致しない場合はエラー
    if (password !== password2) {
      alert("パスワードが一致しません。");
      return;
    }

    try {
      // ↓ axios.post を apiClient.post に変更し、URLを相対パスにする
      await apiClient.post("/register/", {
        username: username,
        password: password,
      });

      alert("登録に成功しました！ログインしてください。");
      // 登録成功後、ログインページに移動
      navigate("/login");
    } catch (error: any) {
      console.error("登録エラー:", error);
      // バックエンドから返却されたエラーメッセージを表示
      const errorMsg =
        error.response?.data?.username?.[0] || "登録に失敗しました。";
      alert(errorMsg);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded-lg shadow-md w-96">
        <h2 className="text-2xl font-bold text-center mb-6">新規登録</h2>
        <form onSubmit={handleRegister}>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2" htmlFor="username">
              ユーザー名
            </label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 mb-2" htmlFor="password">
              パスワード
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg"
              required
            />
          </div>
          <div className="mb-6">
            <label className="block text-gray-700 mb-2" htmlFor="password2">
              パスワード（確認用）
            </label>
            <input
              type="password"
              id="password2"
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600"
          >
            登録
          </button>
        </form>
        <div className="text-center mt-4">
          <p className="text-sm">
            アカウントをお持ちですか？{" "}
            <Link to="/login" className="text-indigo-500 hover:underline">
              ログイン
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
