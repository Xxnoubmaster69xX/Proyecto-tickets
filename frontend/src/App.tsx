import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import PublicRegistration from './pages/PublicRegistration';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AdminSearch from './pages/AdminSearch';
import Catalogos from './pages/Catalogos';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <BrowserRouter>
      <Layout isLoggedIn={isLoggedIn} onLogout={handleLogout}>
        <Routes>
          <Route path="/" element={<PublicRegistration />} />
          <Route path="/login" element={<Login onLogin={() => setIsLoggedIn(true)} />} />
          
          {/* Admin Routes shielded by mock guard for brevity */}
          <Route 
            path="/admin/dashboard" 
            element={isLoggedIn ? <Dashboard /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/admin/search" 
            element={isLoggedIn ? <AdminSearch /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/admin/catalogos" 
            element={isLoggedIn ? <Catalogos /> : <Navigate to="/login" />} 
          />
          
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
