import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';
import { RefreshCw, Activity, AlertCircle, CheckCircle } from 'lucide-react';

const COLORS = ['#f59e0b', '#10b981']; // amber for pending, emerald for resolved

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [mId, setMId] = useState('');
  const [municipios, setMunicipios] = useState([]);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const qs = mId ? `?municipio_id=${mId}` : '';
      const [sRes, mRes] = await Promise.all([
        fetch(`http://localhost:8000/api/dashboard/stats${qs}`),
        fetch('http://localhost:8000/api/catalogos/municipio')
      ]);
      setStats(await sRes.json());
      if (municipios.length === 0) setMunicipios(await mRes.json());
    } catch (err) { }
    setLoading(false);
  };

  useEffect(() => { fetchStats(); }, [mId]);

  if (!stats) return <div className="text-white">Cargando...</div>;

  const pieData = [
    { name: 'Pendientes', value: stats.pendientes },
    { name: 'Resueltos', value: stats.resueltos }
  ];

  // Map array of dicts to object arrays for UI
  const barData = stats.por_municipio?.slice(0, 10).map((i:any) => ({ name: i.nombre, value: i['COUNT(*)'] })) || [];
  const asuntoData = stats.por_asunto?.map((i:any) => ({ name: i.descripcion, value: i['COUNT(*)'] })) || [];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Dashboard Analítico</h1>
          <p className="text-gray-400">Resumen en tiempo real de operaciones</p>
        </div>
        <div className="flex gap-4 mt-4 sm:mt-0">
          <select value={mId} onChange={e => setMId(e.target.value)} className="input-field bg-surface min-w-[200px]">
            <option value="">Filtro: Todo el Estado</option>
            {municipios.map((m:any) => <option key={m.id} value={m.id}>{m.nombre}</option>)}
          </select>
          <button onClick={fetchStats} className="btn-secondary px-3" title="Refrescar">
            <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-6 border-b-4 border-b-primary flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-medium tracking-wider mb-1">TOTAL TICKETS</p>
            <h2 className="text-4xl font-bold text-white">{stats.total}</h2>
          </div>
          <div className="w-12 h-12 rounded-xl bg-primary/20 text-primary flex items-center justify-center">
            <Activity className="w-6 h-6" />
          </div>
        </div>
        <div className="glass-panel p-6 border-b-4 border-b-amber-500 flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-medium tracking-wider mb-1">PENDIENTES</p>
            <h2 className="text-4xl font-bold text-white">{stats.pendientes}</h2>
          </div>
          <div className="w-12 h-12 rounded-xl bg-amber-500/20 text-amber-500 flex items-center justify-center">
            <AlertCircle className="w-6 h-6" />
          </div>
        </div>
        <div className="glass-panel p-6 border-b-4 border-b-emerald-500 flex items-center justify-between">
          <div>
            <p className="text-gray-400 text-sm font-medium tracking-wider mb-1">RESUELTOS</p>
            <h2 className="text-4xl font-bold text-white">{stats.resueltos}</h2>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/20 text-emerald-500 flex items-center justify-center">
            <CheckCircle className="w-6 h-6" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-panel p-6 h-96 flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">Estado Legal de Tramites</h3>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={80} outerRadius={120} paddingAngle={5} dataKey="value">
                  {pieData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', borderRadius: '8px' }} itemStyle={{ color: '#fff' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel p-6 h-96 flex flex-col">
          <h3 className="text-lg font-semibold text-white mb-6">{mId ? 'Distribución por Asunto' : 'Top Municipios (Actividad)'}</h3>
          <div className="flex-1">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart layout="vertical" data={mId ? asuntoData : barData} margin={{ top: 0, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" horizontal={false} />
                <XAxis type="number" stroke="#9CA3AF" />
                <YAxis dataKey="name" type="category" width={100} stroke="#9CA3AF" tick={{ fill: '#D1D5DB' }} />
                <Tooltip contentStyle={{ backgroundColor: '#1F2937', borderColor: '#374151', borderRadius: '8px' }} cursor={{fill: '#374151', opacity: 0.4}}/>
                <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={24} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
