import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ArticleCreate = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('authToken');
      await axios.post('/wiki/create/', {
        title,
        content,
        category: 1, // Пока фиксированная категория
      }, {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });
      navigate('/articles');
    } catch (error) {
      console.error('Failed to create article:', error);
      alert('Не удалось создать статью. Попробуйте позже.');
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '50px auto', padding: '20px' }}>
      <h2>Создать статью</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>Заголовок:</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
            required
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label>Содержание:</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            style={{ width: '100%', height: '200px', padding: '8px' }}
            required
          />
        </div>
        <button type="submit" style={{ padding: '10px 20px' }}>
          Создать
        </button>
      </form>
    </div>
  );
};

export default ArticleCreate;