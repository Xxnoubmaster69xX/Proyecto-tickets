import React from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, FileText, Search, Database, LogOut } from 'lucide-react';
import clsx from 'clsx';

export const Sidebar = ({ isLoggedIn, onLogout }: { isLoggedIn: boolean, onLogout: () => void }) => {
  const navigate = useNavigate();

  const commonClasses = "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 hover:bg-surfaceLight text-textSecondary hover:text-textPrimary";
  const activeClasses = "bg-primary/20 text-primary border-l-4 border-primary shadow-[inset_0_0_20px_rgba(59,130,246,0.1)]";

  return (
    <div className="w-72 h-screen flex flex-col bg-surface backdrop-blur-xl border-r border-borderTheme shadow-2xl z-50">
      <div className="p-8 flex items-center justify-center border-b border-borderTheme flex-col text-center">
        <img src="/logo.webp" alt="Logo UAdeC" className="w-24 h-auto object-contain mb-4 drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]" />
        <div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-textPrimary to-textSecondary">
            Ticket Turno
          </h1>
          <p className="text-xs text-textSecondary font-medium tracking-wider">UNIVERSIDAD AUTÓNOMA DE COAHUILA</p>
        </div>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <div className="px-4 pb-2 text-xs font-semibold text-textSecondary tracking-widest">PÚBLICO</div>
        <NavLink 
          to="/" 
          className={({ isActive }) => clsx(commonClasses, isActive && activeClasses)}
          end
        >
          <FileText className="w-5 h-5" />
          <span>Registrar Trámite</span>
        </NavLink>

        {isLoggedIn && (
          <>
            <div className="px-4 pt-6 pb-2 text-xs font-semibold text-textSecondary tracking-widest mt-4 border-t border-borderTheme">ADMINISTRACIÓN</div>
            
            <NavLink 
              to="/admin/dashboard" 
              className={({ isActive }) => clsx(commonClasses, isActive && activeClasses)}
            >
              <LayoutDashboard className="w-5 h-5" />
              <span>Dashboard</span>
            </NavLink>
            
            <NavLink 
              to="/admin/search" 
              className={({ isActive }) => clsx(commonClasses, isActive && activeClasses)}
            >
              <Search className="w-5 h-5" />
              <span>Búsqueda y Gestión</span>
            </NavLink>
            
            <NavLink 
              to="/admin/catalogos" 
              className={({ isActive }) => clsx(commonClasses, isActive && activeClasses)}
            >
              <Database className="w-5 h-5" />
              <span>Catálogos</span>
            </NavLink>
          </>
        )}
      </nav>

      <div className="p-4 border-t border-borderTheme">
        {isLoggedIn ? (
          <button
            onClick={onLogout}
            className="flex items-center space-x-3 text-textSecondary hover:text-textPrimary transition-colors w-full px-4 py-3 rounded-lg hover:bg-surfaceLight"
          >
            <LogOut size={20} />
            <span className="font-medium">Cerrar Sesión</span>
          </button>
        ) : (
          <button
            onClick={() => navigate('/login')}
            className="flex items-center justify-center space-x-2 text-textSecondary hover:text-textPrimary transition-colors w-full px-4 py-3 rounded-lg bg-surfaceLight hover:bg-opacity-80"
          >
            <span className="font-medium">Acceso Administrador</span>
          </button>
        )}
      </div>
    </div>
  );
};
