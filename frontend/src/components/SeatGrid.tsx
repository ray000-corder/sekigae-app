// TypeScriptのための型定義
interface Seat {
  id: number;
  row: number;
  col: number;
  student_name: string | null;
  is_active: boolean;
}

interface SeatLayout {
  id: number;
  name: string;
  rows: number;
  cols: number;
  seats: Seat[];
}

// このコンポーネントが受け取るデータ(props)の型定義
interface SeatGridProps {
  layout: SeatLayout | null;
  onSeatClick: (seatId: number, currentStatus: boolean) => void;
}

const SeatGrid = ({ layout, onSeatClick }: SeatGridProps) => {
  // データがまだ読み込まれていない場合は、ローディング表示
  if (!layout) {
    return <p>座席表を読み込み中...</p>;
  }

  // APIから取得した1次元配列の座席データを、画面表示用の2次元配列（グリッド）に変換
  const seatGrid: (Seat | null)[][] = Array(layout.rows).fill(null).map(() => Array(layout.cols).fill(null));
  layout.seats.forEach(seat => {
    if (seat.row < layout.rows && seat.col < layout.cols) {
      seatGrid[seat.row][seat.col] = seat;
    }
  });

  return (
    <div className="p-4 bg-gray-200 rounded-lg inline-block">
      <div 
        className="grid gap-4"
        // 列の数に応じて、CSS Gridの列数を動的に設定
        style={{ gridTemplateColumns: `repeat(${layout.cols}, minmax(0, 1fr))` }}
      >
        {/* 2次元配列をmapで展開して、各座席を描画 */}
        {seatGrid.map((row, rowIndex) => (
          row.map((seat, colIndex) => (
            <div 
              key={`${rowIndex}-${colIndex}`}
               onClick={() => seat && onSeatClick(seat.id, seat.is_active)}
              className={`
                w-28 h-20 rounded-md flex items-center justify-center text-center
                ${seat && seat.is_active ? 'bg-white shadow' : 'bg-gray-200'}
              `}
            >
              {seat && seat.is_active && (
                <span className="text-sm text-gray-800 p-1">
                  {seat.student_name || '（空席）'}
                </span>
              )}
            </div>
          ))
        ))}
      </div>
    </div>
  );
};

export default SeatGrid;