import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ArticleList from './pages/ArticleList';
import ArticleDetail from './pages/ArticleDetail';
import ArticleCreate from './pages/ArticleCreate';
import Login from "./pages/Login";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/articles" element={<ArticleList />} />
          <Route path="/article/:slug" element={<ArticleDetail />} />
          <Route path="/create" element={<ArticleCreate />} />
          <Route path="/" element={<ArticleList />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;