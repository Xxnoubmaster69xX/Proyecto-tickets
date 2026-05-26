import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';
import { RefreshCw, Activity, AlertCircle, CheckCircle, X, Filter } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const COLORS = ['#f59e0b', '#10b981']; // amber for pending, emerald for resolved

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  
  // Interactive filters
  const [mId, setMId] = useState<number | ''>('');
  const [aId, setAId] = useState<number | ''>('');
  const [nId, setNId] = useState<number | ''>('');
  
  // Catalogs for names mapping
  const [catalogos, setCatalogos] = useState<{municipios: any[], asuntos: any[], niveles: any[]}>({ municipios: [], asuntos: [], niveles: [] });

  const fetchStats = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (mId) params.append('municipio_id', mId.toString());
      if (aId) params.append('asunto_id', aId.toString());
      if (nId) params.append('nivel_id', nId.toString());

      const [sRes, mRes, aRes, nRes] = await Promise.all([
        fetch(`http://localhost:8000/api/dashboard/stats?${params.toString()}`),
        fetch('http://localhost:8000/api/catalogos/municipio'),
        fetch('http://localhost:8000/api/catalogos/asunto'),
        fetch('http://localhost:8000/api/catalogos/nivel')
      ]);
      setStats(await sRes.json());
      
      if (catalogos.municipios.length === 0) {
        setCatalogos({
          municipios: await mRes.json(),
          asuntos: await aRes.json(),
          niveles: await nRes.json()
        });
      }
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  useEffect(() => { fetchStats(); }, [mId, aId, nId]);

  if (!stats) return <div className="text-white text-center py-20 animate-pulse">Cargando Sistema Analítico...</div>;

  const pieData = [
    { name: 'Pendientes', value: stats.pendientes },
    { name: 'Resueltos', value: stats.resueltos }
  ];

  // Map array of dicts to object arrays for UI
  const barData = stats.por_municipio?.map((i:any) => ({ name: i.nombre, id: i.id, value: i['COUNT(*)'] })) || [];
  const asuntoData = stats.por_asunto?.map((i:any) => ({ name: i.descripcion, id: i.id, value: i['COUNT(*)'] })) || [];
  const nivelData = stats.por_nivel?.map((i:any) => ({ name: i.nombre, id: i.id, value: i['COUNT(*)'] })) || [];

  const handleItemClick = (data: any, type: 'municipio' | 'asunto' | 'nivel') => {
    if (!data) return;
    const item = data.activePayload ? data.activePayload[0]?.payload : data.payload || data;
    if (!item || !item.id) return;
    
    if (type === 'municipio') setMId(item.id);
    if (type === 'asunto') setAId(item.id);
    if (type === 'nivel') setNId(item.id);
  };

  const activeFilters = [
    { type: 'Municipio', val: mId, name: catalogos.municipios.find((m:any) => m.id === mId)?.nombre, clear: () => setMId('') },
    { type: 'Asunto', val: aId, name: catalogos.asuntos.find((a:any) => a.id === aId)?.descripcion, clear: () => setAId('') },
    { type: 'Nivel', val: nId, name: catalogos.niveles.find((n:any) => n.id === nId)?.nombre, clear: () => setNId('') },
  ].filter(f => f.val !== '');

  return (
    <div className="space-y-6 relative z-10">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard Analítico</h1>
          <p className="text-gray-400">Resumen interactivo en tiempo real. Haz clic en las gráficas para filtrar.</p>
        </div>
        <button onClick={fetchStats} className="btn-secondary px-3 mt-4 md:mt-0 flex items-center gap-2" title="Refrescar">
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          <span>Sincronizar</span>
        </button>
      </div>

      {/* Active Filters Banner */}
      <AnimatePresence>
        {activeFilters.length > 0 && (
          <motion.div 
            initial={{ opacity: 0, y: -10 }} 
            animate={{ opacity: 1, y: 0 }} 
            exit={{ opacity: 0, scale: 0.95 }}
            className="flex flex-wrap items-center gap-3 p-4 liquid-glass-panel"
          >
            <div className="flex items-center gap-2 text-sm text-gray-400 mr-2">
              <Filter className="w-4 h-4" /> Filtros Activos:
            </div>
            {activeFilters.map(f => (
              <span key={f.type} className="inline-flex items-center gap-2 px-3 py-1 bg-primary/20 border border-primary/40 rounded-full text-white text-sm">
                <span className="font-semibold">{f.type}:</span> {f.name}
                <button onClick={f.clear} className="hover:text-red-400 hover:bg-white/10 rounded-full p-0.5 transition-colors">
                  <X className="w-3 h-3" />
                </button>
              </span>
            ))}
            <button 
              onClick={() => { setMId(''); setAId(''); setNId(''); }}
              className="ml-auto text-sm text-red-400 hover:text-red-300 font-medium transition-colors underline underline-offset-2"
            >
              Limpiar Todos
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <motion.div key={stats.total} initial={{ scale: 0.95, opacity: 0.5 }} animate={{ scale: 1, opacity: 1 }} className="liquid-glass-panel p-6 border-b-4 border-b-primary flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-medium tracking-wider mb-1">TOTAL TICKETS</p>
            <h2 className="text-4xl font-bold text-white">{stats.total}</h2>
          </div>
          <div className="w-12 h-12 rounded-xl bg-primary/20 text-primary flex items-center justify-center">
            <Activity className="w-6 h-6" />
          </div>
        </motion.div>
        <motion.div key={stats.pendientes} initial={{ scale: 0.95, opacity: 0.5 }} animate={{ scale: 1, opacity: 1 }} className="liquid-glass-panel p-6 border-b-4 border-b-amber-500 flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-medium tracking-wider mb-1">PENDIENTES</p>
            <h2 className="text-4xl font-bold text-white">{stats.pendientes}</h2>
          </div>
          <div className="w-12 h-12 rounded-xl bg-amber-500/20 text-amber-500 flex items-center justify-center">
            <AlertCircle className="w-6 h-6" />
          </div>
        </motion.div>
        <motion.div key={stats.resueltos} initial={{ scale: 0.95, opacity: 0.5 }} animate={{ scale: 1, opacity: 1 }} className="liquid-glass-panel p-6 border-b-4 border-b-emerald-500 flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-medium tracking-wider mb-1">RESUELTOS</p>
            <h2 className="text-4xl font-bold text-white">{stats.resueltos}</h2>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/20 text-emerald-500 flex items-center justify-center">
            <CheckCircle className="w-6 h-6" />
          </div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="liquid-glass-panel p-6 h-[400px] flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">Estado Legal de Tramites</h3>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie 
                  data={pieData} cx="50%" cy="50%" innerRadius={80} outerRadius={120} paddingAngle={5} dataKey="value"
                  isAnimationActive={true} animationDuration={800}
                >
                  {pieData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: 'rgba(30, 41, 59, 0.8)', backdropFilter: 'blur(10px)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px' }} itemStyle={{ color: '#fff' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="liquid-glass-panel p-6 h-[400px] flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">Top Municipios (Actividad)</h3>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart layout="vertical" data={barData.slice(0, 8)} margin={{ top: 0, right: 30, left: 0, bottom: 0 }} onClick={(e) => handleItemClick(e, 'municipio')}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" horizontal={false} />
                <XAxis type="number" stroke="#9CA3AF" />
                <YAxis dataKey="name" type="category" width={110} stroke="#9CA3AF" tick={{ fill: '#D1D5DB' }} />
                <Tooltip cursor={{fill: 'rgba(255,255,255,0.1)'}} contentStyle={{ backgroundColor: 'rgba(30, 41, 59, 0.8)', backdropFilter: 'blur(10px)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px' }}/>
                <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={20} className="cursor-pointer hover:opacity-80 transition-opacity cursor-pointer" isAnimationActive={true} animationDuration={800} onClick={(data) => handleItemClick(data, 'municipio')} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="liquid-glass-panel p-6 h-[400px] flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">Asuntos de Trámite</h3>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={asuntoData} margin={{ top: 20, right: 0, left: 0, bottom: 20 }} onClick={(e) => handleItemClick(e, 'asunto')}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                <XAxis dataKey="name" stroke="#9CA3AF" tick={{ fill: '#D1D5DB' }} angle={-25} textAnchor="end" height={60} />
                <YAxis type="number" stroke="#9CA3AF" />
                <Tooltip cursor={{fill: 'rgba(255,255,255,0.1)'}} contentStyle={{ backgroundColor: 'rgba(30, 41, 59, 0.8)', backdropFilter: 'blur(10px)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px' }}/>
                <Bar dataKey="value" fill="#8b5cf6" radius={[4, 4, 0, 0]} barSize={35} className="cursor-pointer hover:opacity-80 transition-opacity cursor-pointer" isAnimationActive={true} animationDuration={800} onClick={(data) => handleItemClick(data, 'asunto')} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="liquid-glass-panel p-6 h-[400px] flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">Niveles Educativos</h3>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart layout="vertical" data={nivelData} margin={{ top: 0, right: 30, left: 0, bottom: 0 }} onClick={(e) => handleItemClick(e, 'nivel')}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" horizontal={false} />
                <XAxis type="number" stroke="#9CA3AF" />
                <YAxis dataKey="name" type="category" width={110} stroke="#9CA3AF" tick={{ fill: '#D1D5DB' }} />
                <Tooltip cursor={{fill: 'rgba(255,255,255,0.1)'}} contentStyle={{ backgroundColor: 'rgba(30, 41, 59, 0.8)', backdropFilter: 'blur(10px)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px' }}/>
                <Bar dataKey="value" fill="#ec4899" radius={[0, 4, 4, 0]} barSize={24} className="cursor-pointer hover:opacity-80 transition-opacity cursor-pointer" isAnimationActive={true} animationDuration={800} onClick={(data) => handleItemClick(data, 'nivel')} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
