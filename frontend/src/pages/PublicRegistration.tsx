import React, { useState, useEffect } from 'react';
import { Send, Download, CheckCircle, Ticket } from 'lucide-react';

export default function PublicRegistration() {
  const [catalogs, setCatalogs] = useState({ municipios: [], niveles: [], asuntos: [] });
  const [form, setForm] = useState({
    curp_alumno: '',
    nombre: '',
    paterno: '',
    materno: '',
    nivel_id: '',
    municipio_id: '',
    asunto_id: '',
    quien_tramita: '',
    telefono_principal: '',
    telefono_secundario: '',
    correo: '',
    observaciones: ''
  });
  const [status, setStatus] = useState({ loading: false, msg: '', type: '' });
  const [successData, setSuccessData] = useState<any>(null);

  useEffect(() => {
    const fetchCatalogs = async () => {
      try {
        const [mRes, nRes, aRes] = await Promise.all([
          fetch('http://localhost:8000/api/catalogos/municipio'),
          fetch('http://localhost:8000/api/catalogos/nivel'),
          fetch('http://localhost:8000/api/catalogos/asunto')
        ]);
        setCatalogs({
          municipios: await mRes.json(),
          niveles: await nRes.json(),
          asuntos: await aRes.json()
        });
      } catch (err) {
        console.error("Error cargando catálogos", err);
      }
    };
    fetchCatalogs();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus({ loading: true, msg: 'Procesando...', type: 'info' });
    
    try {
      const res = await fetch('http://localhost:8000/api/solicitudes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({...form, nivel_id: parseInt(form.nivel_id), municipio_id: parseInt(form.municipio_id), asunto_id: parseInt(form.asunto_id)})
      });
      const data = await res.json();
      
      if (data.success) {
        setStatus({ loading: false, msg: '¡Trámite registrado con éxito!', type: 'success' });
        setSuccessData(data.solicitud);
        setForm({ curp_alumno: '', nombre: '', paterno: '', materno: '', nivel_id: '', municipio_id: '', asunto_id: '', quien_tramita: '', telefono_principal: '', telefono_secundario: '', correo: '', observaciones: '' });
      } else {
        setStatus({ loading: false, msg: data.detail || 'Error al procesar', type: 'error' });
      }
    } catch (err) {
      setStatus({ loading: false, msg: 'Error de conexión', type: 'error' });
    }
  };

  const handleDownload = () => {
    window.open(`http://localhost:8000/api/solicitudes/${successData.id}/pdf`, '_blank');
  };

  if (successData) {
    return (
      <div className="max-w-2xl mx-auto py-12 animate-[fadeIn_0.5s_ease-out]">
        <div className="glass-panel p-10 text-center relative overflow-hidden">
          <div className="absolute top-0 inset-x-0 h-2 bg-gradient-to-r from-green-500 to-emerald-400"></div>
          
          <div className="w-20 h-20 bg-green-500/20 text-green-400 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="w-10 h-10" />
          </div>
          
          <h2 className="text-3xl font-bold text-white mb-2">¡Trámite Registrado!</h2>
          <p className="text-gray-300 mb-8 max-w-md mx-auto">
            Hemos recibido su solicitud. Por favor guarde su número de turno para darle seguimiento.
          </p>
          
          <div className="bg-surface p-6 rounded-2xl border border-gray-700/50 inline-block mb-8 shadow-inner shadow-black/50">
            <p className="text-sm text-gray-400 uppercase tracking-widest font-semibold mb-1">SU NÚMERO DE TURNO ES</p>
            <p className="text-6xl font-black text-primary drop-shadow-[0_0_15px_rgba(59,130,246,0.5)]">
              {successData.numero_turno.toString().padStart(4, '0')}
            </p>
          </div>
          
          <div className="flex gap-4 justify-center">
            <button onClick={() => setSuccessData(null)} className="btn-secondary">
              Registrar otro trámite
            </button>
            <button onClick={handleDownload} className="btn-primary flex items-center gap-2">
              <Download className="w-5 h-5" />
              Descargar Comprobante PDF
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto pb-12">
      <div className="mb-8 flex items-center gap-6">
        <img src="/logo.webp" alt="Logo UAdeC" className="w-24 h-auto object-contain drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]" />
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Registro de Trámite Nuevo</h1>
          <p className="text-gray-400 mt-2">Complete el formulario para obtener su número de turno en la UAdeC.</p>
        </div>
      </div>

      <div className="glass-panel p-1 sm:p-8 relative">
        {/* Glow corner */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl pointer-events-none"></div>
        
        {status.msg && (
          <div className={`p-4 mb-6 rounded-lg text-sm font-medium ${
            status.type === 'error' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 
            status.type === 'info' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' : 
            'bg-green-500/10 text-green-400 border border-green-500/20'
          }`}>
            {status.msg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="relative z-10 grid grid-cols-1 md:grid-cols-2 gap-6 p-4">
          
          <div className="space-y-4 md:col-span-2">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-gray-800 pb-2">
              <User className="w-5 h-5 text-primary" /> Datos del Alumno
            </h3>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">CURP *</label>
            <input required value={form.curp_alumno} onChange={e => setForm({...form, curp_alumno: e.target.value.toUpperCase()})} className="input-field" placeholder="18 caracteres" maxLength={18} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Nombre(s) *</label>
            <input required value={form.nombre} onChange={e => setForm({...form, nombre: e.target.value})} className="input-field" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Apellido Paterno *</label>
            <input required value={form.paterno} onChange={e => setForm({...form, paterno: e.target.value})} className="input-field" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Apellido Materno *</label>
            <input required value={form.materno} onChange={e => setForm({...form, materno: e.target.value})} className="input-field" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Nivel Educativo *</label>
            <select required value={form.nivel_id} onChange={e => setForm({...form, nivel_id: e.target.value})} className="input-field">
              <option value="">Seleccione...</option>
              {catalogs.niveles.map((n:any) => <option key={n.id} value={n.id}>{n.nombre}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Municipio de Estudio *</label>
            <select required value={form.municipio_id} onChange={e => setForm({...form, municipio_id: e.target.value})} className="input-field">
              <option value="">Seleccione un municipio</option>
              {catalogs.municipios.map((m:any) => <option key={m.id} value={m.id}>{m.nombre}</option>)}
            </select>
          </div>

          <div className="space-y-4 md:col-span-2 mt-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-gray-800 pb-2">
              <Ticket className="w-5 h-5 text-primary" /> Datos del Trámite
            </h3>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Asunto a tratar *</label>
            <select required value={form.asunto_id} onChange={e => setForm({...form, asunto_id: e.target.value})} className="input-field">
              <option value="">Seleccione asunto</option>
              {catalogs.asuntos.map((a:any) => <option key={a.id} value={a.id}>{a.descripcion}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Quien tramita (Padre/Tutor) *</label>
            <input required value={form.quien_tramita} onChange={e => setForm({...form, quien_tramita: e.target.value})} className="input-field" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Teléfono Principal *</label>
            <input required value={form.telefono_principal} onChange={e => setForm({...form, telefono_principal: e.target.value})} type="tel" className="input-field" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Teléfono Secundario</label>
            <input value={form.telefono_secundario} onChange={e => setForm({...form, telefono_secundario: e.target.value})} type="tel" className="input-field bg-black/20" />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-300 mb-1">Correo Electrónico *</label>
            <input required type="email" value={form.correo} onChange={e => setForm({...form, correo: e.target.value})} className="input-field" />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-300 mb-1">Observaciones</label>
            <textarea rows={3} value={form.observaciones} onChange={e => setForm({...form, observaciones: e.target.value})} className="input-field resize-none bg-black/20" placeholder="Información adicional..."></textarea>
          </div>

          <div className="md:col-span-2 pt-6">
            <button type="submit" disabled={status.loading} className="w-full md:w-auto px-8 btn-primary float-right flex items-center justify-center gap-2">
              <Send className="w-4 h-4" />
              {status.loading ? 'Procesando...' : 'Generar Ticket de Turno'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
// Temporary import resolution for lucide missing User since we didn't import it at the top
import { User } from 'lucide-react';
