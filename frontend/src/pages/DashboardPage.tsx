import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';

function DashboardPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  // 現在のパスに応じて、ナビゲーションリンクのスタイルを変更するための関数
  const getLinkClass = (path: string) => {
    // location.pathnameが '/students' で、引数のpathが '/students' の場合は一致
    // location.pathnameが '/' で、引数のpathが '/' の場合も一致
    return location.pathname === path
      ? 'px-3 py-2 rounded-md text-sm font-medium text-white bg-gray-900'
      : 'px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white';
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-gray-800">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <span className="text-white font-bold">席替えアプリ</span>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4">
                  <Link to="/" className={getLinkClass('/')}>座席表</Link>
                  <Link to="/students" className={getLinkClass('/students')}>生徒管理</Link>
                </div>
              </div>
            </div>
            <div className="hidden md:block">
              <button onClick={handleLogout} className="px-3 py-2 bg-red-500 text-sm text-white rounded-md hover:bg-red-600">
                ログアウト
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main>
        <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
          {/* ↓ ここに、URLに応じた子ページが描画される */}
          <Outlet /> 
        </div>
      </main>
    </div>
  );
}

export default DashboardPage;