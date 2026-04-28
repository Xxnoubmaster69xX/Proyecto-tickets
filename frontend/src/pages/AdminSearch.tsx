import React, { useState, useEffect } from 'react';
import { Search, Eye, RefreshCw, Edit3, Trash2, ShieldAlert } from 'lucide-react';
import clsx from 'clsx';

export default function AdminSearch() {
  const [query, setQuery] = useState('');
  const [type, setType] = useState('curp');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const performSearch = async () => {
    setLoading(true);
    try {
      const q = query ? `?${type}=${encodeURIComponent(query)}` : '';
      const res = await fetch(`http://localhost:8000/api/solicitudes/buscar${q}`);
      setResults(await res.json());
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => { performSearch(); }, []);

  const handleStatusChange = async (id: number, currentStatus: string) => {
    if (!confirm('¿Cambiar estatus?')) return;
    const ns = currentStatus === 'Pendiente' ? 'Resuelto' : 'Pendiente';
    await fetch(`http://localhost:8000/api/solicitudes/${id}/estatus?estatus=${ns}`, { method: 'PUT' });
    performSearch();
  };

  const handleDelete = async (id: number) => {
    if (!confirm('¿Eliminar definitivamente? Esta acción no se puede deshacer.')) return;
    await fetch(`http://localhost:8000/api/solicitudes/${id}`, { method: 'DELETE' });
    performSearch();
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Búsqueda y Gestión</h1>
          <p className="text-gray-400">Modifica o elimina tickets del sistema</p>
        </div>
      </div>

      <div className="glass-panel p-6 flex flex-col md:flex-row gap-4 items-end">
        <div className="w-full md:w-1/4">
          <label className="block text-sm font-medium text-gray-400 mb-1">Buscar por</label>
          <select value={type} onChange={e => setType(e.target.value)} className="input-field">
            <option value="curp">CURP</option>
            <option value="nombre">Nombre / Apellidos</option>
          </select>
        </div>
        <div className="w-full md:w-1/2">
          <label className="block text-sm font-medium text-gray-400 mb-1">Término de búsqueda</label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input 
              value={query} 
              onChange={e => setQuery(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && performSearch()}
              placeholder="Ingrese datos..." 
              className="input-field pl-10"
            />
          </div>
        </div>
        <button onClick={performSearch} disabled={loading} className="btn-primary w-full md:w-auto h-[42px] flex items-center justify-center gap-2">
          {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Search className="w-5 h-5" />}
          Buscar
        </button>
      </div>

      <div className="glass-panel overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="text-xs uppercase bg-surfaceLight/50 text-gray-400 border-b border-gray-800">
              <tr>
                <th className="px-6 py-4">Turno</th>
                <th className="px-6 py-4">Estudiante</th>
                <th className="px-6 py-4">CURP</th>
                <th className="px-6 py-4">Asunto</th>
                <th className="px-6 py-4">Estatus</th>
                <th className="px-6 py-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {results.length === 0 ? (
                <tr><td colSpan={6} className="text-center py-8 text-gray-500">No se encontraron resultados</td></tr>
              ) : (
                results.map((r:any) => (
                  <tr key={r.id} className="border-b border-gray-800/50 hover:bg-white/5 transition-all">
                    <td className="px-6 py-4 font-bold text-white">#{r.numero_turno}</td>
                    <td className="px-6 py-4 font-medium">{r.nombre_alumno}</td>
                    <td className="px-6 py-4 font-mono text-xs">{r.curp_alumno}</td>
                    <td className="px-6 py-4">{r.asunto_descripcion}</td>
                    <td className="px-6 py-4">
                      <button 
                        onClick={() => handleStatusChange(r.id, r.estatus)}
                        className={clsx("px-3 py-1 rounded-full text-xs font-bold border transition-colors", 
                          r.estatus === 'Resuelto' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/20' : 
                          'bg-amber-500/10 text-amber-400 border-amber-500/20 hover:bg-amber-500/20'
                        )}
                      >
                        {r.estatus}
                      </button>
                    </td>
                    <td className="px-6 py-4 flex gap-2 justify-end">
                      <button onClick={() => window.open(`http://localhost:8000/api/solicitudes/${r.id}/pdf`, '_blank')} className="p-2 bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 rounded-lg transition-all" title="Ver PDF">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button onClick={() => handleDelete(r.id)} className="p-2 bg-red-500/10 text-red-400 hover:bg-red-500/20 rounded-lg transition-all" title="Eliminar">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
