import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Save, X } from 'lucide-react';

export default function Catalogos() {
  const [activeTab, setActiveTab] = useState('municipio');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newItem, setNewItem] = useState('');

  const fetchData = async () => {
    setLoading(true);
    const res = await fetch(`http://localhost:8000/api/catalogos/${activeTab}`);
    setData(await res.json());
    setLoading(false);
  };

  useEffect(() => { fetchData(); }, [activeTab]);

  const handleAdd = async () => {
    if (!newItem.trim()) return;
    await fetch(`http://localhost:8000/api/catalogos/${activeTab}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre: newItem, descripcion: newItem })
    });
    setNewItem('');
    fetchData();
  };

  const handleEdit = async (id: number, currentVal: string) => {
    const newVal = window.prompt(`Editar ${activeTab}:`, currentVal);
    if (!newVal || !newVal.trim() || newVal === currentVal) return;
    
    await fetch(`http://localhost:8000/api/catalogos/${activeTab}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre: newVal.trim(), descripcion: newVal.trim() })
    });
    fetchData();
  };

  const handleDelete = async (id: number) => {
    if (!confirm('¿Seguro?')) return;
    const res = await fetch(`http://localhost:8000/api/catalogos/${activeTab}/${id}`, { method: 'DELETE' });
    if (!res.ok) alert("No se puede eliminar porque está en uso por alguna solicitud.");
    else fetchData();
  };

  const tabs = [
    { id: 'municipio', label: 'Municipios' },
    { id: 'nivel', label: 'Niveles Educativos' },
    { id: 'asunto', label: 'Asuntos de Trámite' }
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold text-white">Catálogos</h1>
        <p className="text-gray-400">Administra las listas desplegables del sistema</p>
      </div>

      <div className="flex space-x-1 bg-surfaceLight p-1 rounded-xl">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`w-full py-2.5 text-sm font-medium rounded-lg transition-all ${
              activeTab === tab.id
                ? 'bg-primary text-white shadow-lg'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="glass-panel p-6">
        <div className="flex gap-4 mb-6">
          <input 
            value={newItem} 
            onChange={e => setNewItem(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleAdd()}
            placeholder={`Agregar nuevo ${activeTab}...`} 
            className="input-field" 
          />
          <button onClick={handleAdd} className="btn-primary flex items-center gap-2 whitespace-nowrap">
            <Plus className="w-5 h-5" /> Agregar
          </button>
        </div>

        {loading ? (
          <div className="text-center py-8 text-gray-500">Cargando...</div>
        ) : (
          <div className="border border-gray-800 rounded-xl overflow-hidden">
            <table className="w-full text-left text-sm text-gray-300">
              <thead className="bg-surfaceLight/50 text-gray-400">
                <tr>
                  <th className="px-6 py-3 w-16">ID</th>
                  <th className="px-6 py-3">Nombre / Descripción</th>
                  <th className="px-6 py-3 w-32 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {data.map((item:any) => (
                  <tr key={item.id} className="hover:bg-white/5 transition-colors">
                    <td className="px-6 py-3 font-mono text-gray-500">{item.id}</td>
                    <td className="px-6 py-3 font-medium text-white">{item.nombre || item.descripcion}</td>
                    <td className="px-6 py-3 text-right flex gap-2 justify-end">
                      <button onClick={() => handleEdit(item.id, item.nombre || item.descripcion)} className="p-1.5 bg-gray-600/30 text-gray-300 hover:bg-gray-600/50 rounded-md transition-all">
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button onClick={() => handleDelete(item.id)} className="p-1.5 bg-red-500/10 text-red-400 hover:bg-red-500/20 rounded-md transition-all">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
// Local import fixing
import { Edit3 } from 'lucide-react';
