import React, { useState, useEffect } from 'react';
import { Search, Eye, RefreshCw, Edit3, Trash2, X, Save } from 'lucide-react';
import clsx from 'clsx';

export default function AdminSearch() {
  const [query, setQuery] = useState('');
  const [type, setType] = useState('curp');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Edit Modal State
  const [editingTicket, setEditingTicket] = useState<any>(null);
  const [catalogos, setCatalogos] = useState({ asuntos: [], municipios: [] });

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

  useEffect(() => { 
    performSearch(); 
    // Fetch catalogs for the edit modal
    Promise.all([
      fetch('http://localhost:8000/api/catalogos/asunto').then(r => r.json()),
      fetch('http://localhost:8000/api/catalogos/municipio').then(r => r.json())
    ]).then(([asuntos, municipios]) => setCatalogos({ asuntos, municipios }));
  }, []);

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

  const handleEditSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTicket) return;
    
    try {
      await fetch(`http://localhost:8000/api/solicitudes/${editingTicket.curp_alumno}/${editingTicket.numero_turno}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          quien_tramita: editingTicket.quien_tramita,
          telefono_principal: editingTicket.telefono_principal,
          telefono_secundario: editingTicket.telefono_secundario,
          correo: editingTicket.correo,
          observaciones: editingTicket.observaciones,
          asunto_id: parseInt(editingTicket.asunto_id),
          estatus: editingTicket.estatus
        })
      });
      setEditingTicket(null);
      performSearch();
    } catch (err) {
      alert("Error al guardar");
    }
  };

  return (
    <div className="space-y-6 relative">
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
                  <tr key={r.id} onDoubleClick={() => setEditingTicket({...r})} className="border-b border-gray-800/50 hover:bg-white/5 transition-all cursor-pointer">
                    <td className="px-6 py-4 font-bold text-white">#{r.numero_turno}</td>
                    <td className="px-6 py-4 font-medium">{r.nombre_alumno}</td>
                    <td className="px-6 py-4 font-mono text-xs">{r.curp_alumno}</td>
                    <td className="px-6 py-4">{r.asunto_descripcion}</td>
                    <td className="px-6 py-4">
                      <button 
                        onClick={(e) => { e.stopPropagation(); handleStatusChange(r.id, r.estatus); }}
                        className={clsx("px-3 py-1 rounded-full text-xs font-bold border transition-colors", 
                          r.estatus === 'Resuelto' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20 hover:bg-emerald-500/20' : 
                          'bg-amber-500/10 text-amber-400 border-amber-500/20 hover:bg-amber-500/20'
                        )}
                      >
                        {r.estatus}
                      </button>
                    </td>
                    <td className="px-6 py-4 flex gap-2 justify-end">
                      <button onClick={(e) => { e.stopPropagation(); window.open(`http://localhost:8000/api/solicitudes/${r.id}/pdf`, '_blank'); }} className="p-2 bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 rounded-lg transition-all" title="Ver PDF">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button onClick={(e) => { e.stopPropagation(); setEditingTicket({...r}); }} className="p-2 bg-gray-600/30 text-gray-300 hover:bg-gray-600/50 rounded-lg transition-all" title="Editar">
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button onClick={(e) => { e.stopPropagation(); handleDelete(r.id); }} className="p-2 bg-red-500/10 text-red-400 hover:bg-red-500/20 rounded-lg transition-all" title="Eliminar">
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

      {/* Edit Modal */}
      {editingTicket && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-[fadeIn_0.2s_ease-out]">
          <div className="glass-panel w-full max-w-2xl max-h-[90vh] overflow-y-auto flex flex-col">
            <div className="p-6 border-b border-gray-800 flex justify-between items-center bg-surfaceLight/50 sticky top-0 z-10">
              <div>
                <h3 className="text-xl font-bold text-white">Modificar Ticket #{editingTicket.numero_turno}</h3>
                <p className="text-sm text-gray-400 font-mono">{editingTicket.curp_alumno} - {editingTicket.nombre_alumno}</p>
              </div>
              <button onClick={() => setEditingTicket(null)} className="p-2 hover:bg-white/10 rounded-lg transition-colors">
                <X className="w-5 h-5 text-gray-400" />
              </button>
            </div>
            
            <form onSubmit={handleEditSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Estatus del Trámite</label>
                  <select 
                    value={editingTicket.estatus} 
                    onChange={e => setEditingTicket({...editingTicket, estatus: e.target.value})} 
                    className={clsx("input-field font-bold border-2", editingTicket.estatus === 'Resuelto' ? 'border-emerald-500 text-emerald-400' : 'border-amber-500 text-amber-400')}
                  >
                    <option value="Pendiente">Pendiente</option>
                    <option value="Resuelto">Resuelto</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Asunto</label>
                  <select 
                    value={editingTicket.asunto_id} 
                    onChange={e => setEditingTicket({...editingTicket, asunto_id: e.target.value})} 
                    className="input-field"
                  >
                    {catalogos.asuntos.map((a:any) => <option key={a.id} value={a.id}>{a.descripcion}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Contacto Principal (Tutor)</label>
                  <input value={editingTicket.quien_tramita} onChange={e => setEditingTicket({...editingTicket, quien_tramita: e.target.value})} className="input-field" required />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Correo Electrónico</label>
                  <input type="email" value={editingTicket.correo} onChange={e => setEditingTicket({...editingTicket, correo: e.target.value})} className="input-field" required />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Teléfono Principal</label>
                  <input value={editingTicket.telefono_principal} onChange={e => setEditingTicket({...editingTicket, telefono_principal: e.target.value})} className="input-field" required />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-1">Teléfono Secundario</label>
                  <input value={editingTicket.telefono_secundario || ''} onChange={e => setEditingTicket({...editingTicket, telefono_secundario: e.target.value})} className="input-field" />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-300 mb-1">Observaciones</label>
                  <textarea rows={3} value={editingTicket.observaciones || ''} onChange={e => setEditingTicket({...editingTicket, observaciones: e.target.value})} className="input-field resize-none"></textarea>
                </div>
              </div>
              
              <div className="pt-4 flex justify-end gap-3 border-t border-gray-800 mt-6">
                <button type="button" onClick={() => setEditingTicket(null)} className="btn-secondary">Cancelar</button>
                <button type="submit" className="btn-primary flex items-center gap-2"><Save className="w-4 h-4"/> Guardar Cambios</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
