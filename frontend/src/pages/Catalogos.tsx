import { useState, useEffect, useMemo } from 'react';
import { Plus, Trash2, Edit3, ArrowUp, ArrowDown, ArrowUpDown, SlidersHorizontal, FilterX } from 'lucide-react';
import clsx from 'clsx';
import { useExcelTable } from '../hooks/useExcelTable';

export default function Catalogos() {
  const [activeTab, setActiveTab] = useState('municipio');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newItem, setNewItem] = useState('');

  const columns = useMemo(() => [
    { key: 'id', type: 'number' as const, label: 'ID' },
    { 
      key: 'display_name', 
      type: 'string' as const, 
      label: 'Nombre / Descripción',
      getValue: (item: any) => item.nombre || item.descripcion || ''
    },
  ], []);

  const [showExcelFilters, setShowExcelFilters] = useState(true);

  const {
    filteredAndSortedData,
    filters,
    validationErrors,
    sortField,
    sortDirection,
    handleFilterChange,
    handleSort,
    clearFilters,
  } = useExcelTable(data, columns);

  const fetchData = async () => {
    setLoading(true);
    const res = await fetch(`http://localhost:8000/api/catalogos/${activeTab}`);
    setData(await res.json());
    setLoading(false);
  };

  useEffect(() => { 
    fetchData(); 
    clearFilters();
  }, [activeTab]);

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
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Catálogos</h1>
          <p className="text-gray-400">Administra las listas desplegables del sistema</p>
        </div>
        <div className="flex gap-2 mt-4 sm:mt-0">
          <button 
            onClick={() => setShowExcelFilters(!showExcelFilters)} 
            className={clsx("btn-secondary flex items-center gap-2 text-sm px-4 py-2 border-gray-800", showExcelFilters && "bg-white/10 text-white border-white/20")}
            title="Mostrar/Ocultar Filtros de Excel"
          >
            <SlidersHorizontal className="w-4 h-4" />
            {showExcelFilters ? "Ocultar Filtros" : "Mostrar Filtros"}
          </button>
          {(Object.values(filters).some(Boolean) || sortField) && (
            <button 
              onClick={clearFilters} 
              className="btn-secondary flex items-center gap-2 text-sm px-4 py-2 border-red-500/30 hover:border-red-500/50 hover:bg-red-500/10 text-red-400"
              title="Restablecer todos los filtros y orden"
            >
              <FilterX className="w-4 h-4" />
              Limpiar Filtros
            </button>
          )}
        </div>
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

      <div className="liquid-glass-panel p-6">
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
                  <th className="px-6 py-3 w-32 cursor-pointer hover:bg-white/5 hover:text-white select-none transition-colors" onClick={() => handleSort('id')}>
                    <div className="flex items-center gap-1.5">
                      <span>ID</span>
                      {sortField === 'id' ? (
                        sortDirection === 'asc' ? <ArrowUp className="w-3.5 h-3.5 text-primary" /> : <ArrowDown className="w-3.5 h-3.5 text-primary" />
                      ) : (
                        <ArrowUpDown className="w-3.5 h-3.5 opacity-40 hover:opacity-100" />
                      )}
                    </div>
                  </th>
                  <th className="px-6 py-3 cursor-pointer hover:bg-white/5 hover:text-white select-none transition-colors" onClick={() => handleSort('display_name')}>
                    <div className="flex items-center gap-1.5">
                      <span>Nombre / Descripción</span>
                      {sortField === 'display_name' ? (
                        sortDirection === 'asc' ? <ArrowUp className="w-3.5 h-3.5 text-primary" /> : <ArrowDown className="w-3.5 h-3.5 text-primary" />
                      ) : (
                        <ArrowUpDown className="w-3.5 h-3.5 opacity-40 hover:opacity-100" />
                      )}
                    </div>
                  </th>
                  <th className="px-6 py-3 w-32 text-right select-none">Acciones</th>
                </tr>
                {showExcelFilters && (
                  <tr className="bg-surfaceLight/30 border-b border-gray-800">
                    {/* ID */}
                    <th className="px-4 py-2 font-normal">
                      <div className="relative">
                        <input
                          value={filters['id'] || ''}
                          onChange={e => handleFilterChange('id', e.target.value)}
                          placeholder="Filtrar ID (ej: >10)"
                          className={clsx(
                            "w-full text-xs bg-black/40 border rounded px-2.5 py-1.5 text-white placeholder-gray-500 focus:outline-none focus:border-primary",
                            validationErrors['id'] ? 'border-red-500 focus:border-red-500' : 'border-gray-800/80'
                          )}
                        />
                        {validationErrors['id'] && (
                          <div className="absolute left-0 top-full mt-1 bg-red-950/95 text-red-400 border border-red-800/50 text-[10px] p-1.5 rounded shadow-xl z-20 whitespace-nowrap">
                            {validationErrors['id']}
                          </div>
                        )}
                      </div>
                    </th>
                    {/* Nombre / Descripción */}
                    <th className="px-4 py-2 font-normal">
                      <input
                        value={filters['display_name'] || ''}
                        onChange={e => handleFilterChange('display_name', e.target.value)}
                        placeholder="Filtrar por descripción..."
                        className="w-full text-xs bg-black/40 border border-gray-800/80 rounded px-2.5 py-1.5 text-white placeholder-gray-500 focus:outline-none focus:border-primary"
                      />
                    </th>
                    {/* Acciones */}
                    <th className="px-4 py-2 text-right">
                      {(Object.values(filters).some(Boolean) || sortField) && (
                        <button 
                          onClick={clearFilters} 
                          className="p-1.5 bg-red-500/10 text-red-400 hover:bg-red-500/20 rounded-md transition-all inline-flex items-center justify-center" 
                          title="Limpiar filtros"
                        >
                          <FilterX className="w-4 h-4" />
                        </button>
                      )}
                    </th>
                  </tr>
                )}
              </thead>
              <tbody className="divide-y divide-gray-800">
                {filteredAndSortedData.length === 0 ? (
                  <tr><td colSpan={3} className="text-center py-6 text-gray-500">No se encontraron resultados</td></tr>
                ) : (
                  filteredAndSortedData.map((item:any) => (
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
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
