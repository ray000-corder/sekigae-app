import { useState, useEffect, useCallback } from 'react';
import apiClient from '../api/axiosConfig';

interface Student { id: number; name: string; }

function StudentManagerPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [newStudentName, setNewStudentName] = useState('');

  const fetchStudents = useCallback(async () => {
    try {
      const response = await apiClient.get('/students/');
      setStudents(response.data);
    } catch (error) { console.error('生徒データの取得に失敗しました:', error); }
  }, []);

  useEffect(() => {
    fetchStudents();
  }, [fetchStudents]);

  const handleAddStudent = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!newStudentName.trim()) return;
    try {
      await apiClient.post('/students/', { name: newStudentName });
      setNewStudentName('');
      fetchStudents();
    } catch (error) { console.error('生徒の追加に失敗しました:', error); }
  };

  const handleDeleteStudent = async (studentId: number) => {
    if (window.confirm('本当にこの生徒を削除しますか？')) {
      try {
        await apiClient.delete(`/students/${studentId}/`);
        fetchStudents();
      } catch (error) { console.error('生徒の削除に失敗しました:', error); }
    }
  };

  return (
    <div className="space-y-8">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-4">新しい生徒を追加</h2>
        <form onSubmit={handleAddStudent} className="flex gap-4">
          <input type="text" value={newStudentName} onChange={(e) => setNewStudentName(e.target.value)} placeholder="生徒の名前" className="flex-grow px-3 py-2 border rounded-lg" />
          <button type="submit" className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">追加</button>
        </form>
      </div>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-4">生徒一覧</h2>
        <ul className="max-h-96 overflow-y-auto">
          {students.map(student => (
            <li key={student.id} className="flex justify-between items-center border-b py-2">
              <span>{student.name}</span>
              <button onClick={() => handleDeleteStudent(student.id)} className="px-3 py-1 bg-gray-200 text-sm rounded hover:bg-gray-300">削除</button>
            </li>
          ))}
          {students.length === 0 && <p>まだ生徒が登録されていません。</p>}
        </ul>
      </div>
    </div>
  );
}

export default StudentManagerPage;