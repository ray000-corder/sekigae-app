import { useState, useEffect, useCallback } from 'react';
import apiClient from '../api/axiosConfig';
import SeatGrid from '../components/SeatGrid';

// 型定義
interface Seat { id: number; row: number; col: number; student_name: string | null; is_active: boolean; }
interface SeatLayout { id: number; name: string; rows: number; cols: number; seats: Seat[]; }

function SeatChartPage() {
  const [seatLayout, setSeatLayout] = useState<SeatLayout | null>(null);
  const [editRows, setEditRows] = useState(0);
  const [editCols, setEditCols] = useState(0);

  const fetchSeatLayout = useCallback(async () => {
    try {
      const response = await apiClient.get('/seat-layouts/');
      if (response.data && response.data.length > 0) {
        const layoutData = response.data[0];
        setSeatLayout(layoutData);
        setEditRows(layoutData.rows);
        setEditCols(layoutData.cols);
      }
    } catch (error) { console.error('座席表データの取得に失敗しました:', error); }
  }, []);

  
  useEffect(() => {
    fetchSeatLayout();
  }, [fetchSeatLayout]);

  const handleShuffle = async () => {
    if (!seatLayout) return;
    if (!window.confirm('席替えを実行しますか？')) return;
    try {
      const response = await apiClient.post(`/seat-layouts/${seatLayout.id}/shuffle/`);
      setSeatLayout(response.data);
      alert('席替えが完了しました！');
    } catch (error) {
      console.error('席替えの実行に失敗しました:', error);
      alert('席替えに失敗しました。');
    }
  };

  const handleSeatClick = async (seatId: number, currentStatus: boolean) => {
    try {
      await apiClient.patch(`/seats/${seatId}/`, { is_active: !currentStatus });
      fetchSeatLayout();
    } catch (error) {
      console.error('座席の状態更新に失敗しました:', error);
      alert('座席の状態更新に失敗しました。');
    }
  };

  const handleLayoutUpdate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!seatLayout) return;
    try {
      await apiClient.patch(`/seat-layouts/${seatLayout.id}/`, { rows: editRows, cols: editCols });
      fetchSeatLayout();
      alert('レイアウトを更新しました！');
    } catch (error) {
      console.error('レイアウトの更新に失敗しました:', error);
      alert('レイアウトの更新に失敗しました。');
    }
  };

  return (
    <div className="space-y-8">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">座席表</h2>
          {/* ↓ デバッグ用の「更新」ボタンは不要になったので削除しました */}
          <button onClick={handleShuffle} className="px-6 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600">席替え実行！</button>
        </div>
        <SeatGrid layout={seatLayout} onSeatClick={handleSeatClick} />
      </div>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-4">レイアウト設定</h2>
        <form onSubmit={handleLayoutUpdate} className="flex items-end gap-4">
          <div>
            <label htmlFor="rows" className="block text-sm font-medium text-gray-700">行数</label>
            <input type="number" id="rows" value={editRows} onChange={(e) => setEditRows(Number(e.target.value))} className="mt-1 w-24 px-3 py-2 border rounded-lg" min="1" max="20" />
          </div>
          <div>
            <label htmlFor="cols" className="block text-sm font-medium text-gray-700">列数</label>
            <input type="number" id="cols" value={editCols} onChange={(e) => setEditCols(Number(e.target.value))} className="mt-1 w-24 px-3 py-2 border rounded-lg" min="1" max="20" />
          </div>
          <button type="submit" className="px-6 py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600">更新</button>
        </form>
      </div>
    </div>
  );
}

export default SeatChartPage;