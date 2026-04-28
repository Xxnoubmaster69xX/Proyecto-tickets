import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, Search, Database, LogOut, Ticket } from 'lucide-react';
import clsx from 'clsx';

export const Sidebar = ({ isLoggedIn, onLogout }: { isLoggedIn: boolean, onLogout: () => void }) => {
  const commonClasses = "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 hover:bg-white/10 text-gray-300 hover:text-white";
  const activeClasses = "bg-primary/20 text-primary border-l-4 border-primary shadow-[inset_0_0_20px_rgba(59,130,246,0.1)]";

  return (
    <div className="w-72 h-screen flex flex-col bg-surface/95 backdrop-blur-xl border-r border-gray-800 shadow-2xl z-50">
      <div className="p-8 flex items-center justify-center border-b border-gray-800/50 flex-col text-center">
        <img src="/logo.webp" alt="Logo UAdeC" className="w-24 h-auto object-contain mb-4 drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]" />
        <div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-100 to-gray-400">
            Ticket Turno
          </h1>
          <p className="text-xs text-gray-500 font-medium tracking-wider">UNIVERSIDAD AUTÓNOMA DE COAHUILA</p>
        </div>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        <div className="px-4 pb-2 text-xs font-semibold text-gray-500 tracking-widest">PÚBLICO</div>
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
            <div className="px-4 pt-6 pb-2 text-xs font-semibold text-gray-500 tracking-widest mt-4 border-t border-gray-800/50">ADMINISTRACIÓN</div>
            
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

      <div className="p-4 border-t border-gray-800/50">
        {isLoggedIn ? (
          <button 
            onClick={onLogout}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-red-500/10 text-red-400 hover:bg-red-500/20 hover:text-red-300 rounded-xl transition-all font-medium"
          >
            <LogOut className="w-5 h-5" />
            Cerrar Sesión
          </button>
        ) : (
          <NavLink 
            to="/login"
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-surfaceLight text-gray-300 hover:bg-white/10 hover:text-white rounded-xl transition-all font-medium border border-gray-700 hover:border-gray-600"
          >
            Acceso Administrador
          </NavLink>
        )}
      </div>
    </div>
  );
};
