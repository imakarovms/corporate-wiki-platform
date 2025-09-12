import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

interface Article {
  title: string;
  content: string;
  author: { email: string };
  category: { name: string };
  created_at: string;
}

const ArticleDetail = () => {
  const { slug } = useParams<{ slug: string }>();
  const [article, setArticle] = useState<Article | null>(null);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const response = await axios.get(`/wiki/${slug}/`);
        setArticle(response.data);
      } catch (error) {
        console.error('Failed to fetch article:', error);
      }
    };
    fetchArticle();
  }, [slug]);

  if (!article) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>{article.title}</h1>
      <p><small>Category: {article.category.name} | Author: {article.author.email} | Published: {new Date(article.created_at).toLocaleDateString()}</small></p>
      <div dangerouslySetInnerHTML={{ __html: article.content }} />
      <hr />
      <Link to="/articles">← Back to Articles</Link>
    </div>
  );
};

export default ArticleDetail;