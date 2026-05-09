import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import CardDetail from './pages/CardDetail';
import Home from './pages/Home';
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <nav className="navbar">
        <Link to="/" className="brand">Card Tracker</Link>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/cards/:id" element={<CardDetail />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
