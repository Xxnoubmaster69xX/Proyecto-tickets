import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { KeyRound, User, Lock, AlertCircle, ArrowRight } from 'lucide-react';

export default function Login({ onLogin }: { onLogin: () => void }) {
  const navigate = useNavigate();
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: user, password: pass })
      });
      const data = await res.json();
      
      if (data.success) {
        onLogin();
        navigate("/admin/dashboard");
      } else {
        setError(data.mensaje || "Credenciales incorrectas");
      }
    } catch (err) {
      setError("Error de conexión al servidor");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[80vh]">
      <div className="glass-panel p-8 w-full max-w-md relative overflow-hidden">
        {/* Glow effect */}
        <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-primary via-accent to-primary opacity-70"></div>
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-primary/20 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-accent/20 rounded-full blur-3xl"></div>

        <div className="relative z-10 flex flex-col items-center mb-8 text-center">
          <img src="/logo.webp" alt="Logo UAdeC" className="w-32 h-auto object-contain mb-4 drop-shadow-2xl" />
          <h2 className="text-2xl font-bold text-white mb-1">Acceso Administrador</h2>
          <p className="text-gray-400 text-sm">Panel de control de Tickets</p>
        </div>

        {error && (
          <div className="relative z-10 mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-3 text-red-400">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        <form onSubmit={handleLogin} className="relative z-10 space-y-5">
          <div className="space-y-1">
            <label className="text-sm font-medium text-gray-300 ml-1">Usuario</label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input 
                value={user} 
                onChange={e => setUser(e.target.value)} 
                placeholder="Nombre de usuario" 
                className="input-field pl-10 bg-black/20 focus:bg-black/40"
              />
            </div>
          </div>
          
          <div className="space-y-1">
            <label className="text-sm font-medium text-gray-300 ml-1">Contraseña</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input 
                type="password" 
                value={pass} 
                onChange={e => setPass(e.target.value)} 
                placeholder="••••••••" 
                className="input-field pl-10 bg-black/20 focus:bg-black/40"
              />
            </div>
          </div>
          
          <button 
            type="submit" 
            disabled={loading}
            className="w-full btn-primary py-3 flex items-center justify-center gap-2 mt-4 text-base"
          >
            {loading ? "Autenticando..." : "Ingresar al Sistema"}
            {!loading && <ArrowRight className="w-4 h-4" />}
          </button>
        </form>
      </div>
    </div>
  );
}
