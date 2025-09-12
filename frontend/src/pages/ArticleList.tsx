import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

interface Article {
  id: number;
  title: string;
  slug: string;
  content: string;
  author: { email: string };
  category: { name: string };
  created_at: string;
}

const ArticleList = () => {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/wiki/api/');
        
        // Проверка: если это объект с results — используем его
        if (Array.isArray(response.data)) {
          setArticles(response.data);
        } else if (response.data.results) {
          setArticles(response.data.results);
        } else {
          setArticles([]); // Если ничего не получили
        }
      } catch (error) {
        console.error('Failed to fetch articles:', error);
        setArticles([]);
      } finally {
        setLoading(false);
      }
    };

    fetchArticles();
  }, []);

  if (loading) {
    return <div style={{ padding: '20px' }}>Загрузка...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Articles</h1>
      {articles.length > 0 ? (
        articles.map((article) => (
          <div key={article.id} style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ccc' }}>
            <h2><Link to={`/article/${article.slug}`}>{article.title}</Link></h2>
            <p><small>Category: {article.category.name} | Author: {article.author.email}</small></p>
            <p>{article.content.substring(0, 100)}...</p>
          </div>
        ))
      ) : (
        <p>Нет опубликованных статей.</p>
      )}
    </div>
  );
};

export default ArticleList;