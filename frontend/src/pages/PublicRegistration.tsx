import React, { useState, useEffect } from 'react';
import { Send, Download, CheckCircle, Ticket, User, Search, Edit3 } from 'lucide-react';
import clsx from 'clsx';

const CURP_REGEX = /^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$/;

export default function PublicRegistration() {
  const [catalogs, setCatalogs] = useState({ municipios: [], niveles: [], asuntos: [] });
  const [mode, setMode] = useState<'nuevo' | 'modificar' | 'consultar'>('nuevo');
  const [turnoMod, setTurnoMod] = useState('');
  
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
  const [foundTicketId, setFoundTicketId] = useState<number | null>(null);

  const curpValid = form.curp_alumno.length === 18 && CURP_REGEX.test(form.curp_alumno);
  const isFormValid = curpValid && form.nombre && form.paterno && form.materno && form.nivel_id && form.municipio_id && form.asunto_id && form.quien_tramita && form.telefono_principal && form.correo;

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

  const handleSearchToModify = async () => {
    if (!curpValid) {
      setStatus({ loading: false, msg: 'Ingrese una CURP válida para buscar', type: 'error' });
      return;
    }
    if (mode === 'modificar' && !turnoMod) {
      setStatus({ loading: false, msg: 'Para modificar necesita ingresar su Número de Turno', type: 'error' });
      return;
    }
    
    setStatus({ loading: true, msg: 'Buscando...', type: 'info' });
    try {
      const res = await fetch(`http://localhost:8000/api/solicitudes/buscar?curp=${form.curp_alumno}`);
      const data = await res.json();
      
      let found;
      if (mode === 'consultar') {
        // En consulta, si hay varios, agarramos el más reciente (o primero).
        // En una app real podríamos mostrar una lista de tickets.
        found = data.length > 0 ? data[data.length - 1] : null;
      } else {
        found = data.find((d:any) => d.numero_turno.toString() === turnoMod);
      }
      
      if (found) {
        setForm({
          curp_alumno: found.curp_alumno,
          nombre: found.nombre_alumno.split(' ')[0] || '', // Aproximación
          paterno: found.nombre_alumno.split(' ')[1] || '',
          materno: found.nombre_alumno.split(' ')[2] || '',
          nivel_id: found.nivel_id || '',
          municipio_id: found.municipio_id || '',
          asunto_id: found.asunto_id || '',
          quien_tramita: found.quien_tramita || '',
          telefono_principal: found.telefono_principal || '',
          telefono_secundario: found.telefono_secundario || '',
          correo: found.correo || '',
          observaciones: found.observaciones || ''
        });
        setFoundTicketId(found.id);
        if (mode === 'consultar') {
          setStatus({ loading: false, msg: 'Solicitud encontrada. Estatus: ' + found.estatus, type: 'success' });
        } else {
          setStatus({ loading: false, msg: 'Solicitud encontrada. Puede modificar datos de contacto y asunto.', type: 'success' });
        }
      } else {
        setStatus({ loading: false, msg: 'No se encontró una solicitud con esos datos', type: 'error' });
        setFoundTicketId(null);
      }
    } catch (err) {
      setStatus({ loading: false, msg: 'Error de conexión', type: 'error' });
      setFoundTicketId(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isFormValid) return;
    
    setStatus({ loading: true, msg: 'Procesando...', type: 'info' });
    
    try {
      const payload = {
        ...form, 
        nivel_id: parseInt(form.nivel_id), 
        municipio_id: parseInt(form.municipio_id), 
        asunto_id: parseInt(form.asunto_id)
      };

      let url = 'http://localhost:8000/api/solicitudes';
      let method = 'POST';

      if (mode === 'modificar') {
        url = `http://localhost:8000/api/solicitudes/${form.curp_alumno}/${turnoMod}`;
        method = 'PUT';
      }

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      
      if (data.success) {
        if (mode === 'nuevo') {
          setStatus({ loading: false, msg: '¡Trámite registrado con éxito!', type: 'success' });
          setSuccessData(data.solicitud);
        } else {
          setStatus({ loading: false, msg: '¡Trámite actualizado con éxito!', type: 'success' });
        }
        if (mode === 'nuevo') {
          setForm({ curp_alumno: '', nombre: '', paterno: '', materno: '', nivel_id: '', municipio_id: '', asunto_id: '', quien_tramita: '', telefono_principal: '', telefono_secundario: '', correo: '', observaciones: '' });
        }
      } else {
        setStatus({ loading: false, msg: data.detail || 'Error al procesar', type: 'error' });
      }
    } catch (err) {
      setStatus({ loading: false, msg: 'Error de conexión', type: 'error' });
    }
  };

  const handleDownload = () => {
    if (successData) window.open(`http://localhost:8000/api/solicitudes/${successData.id}/pdf`, '_blank');
  };

  const handleReprint = () => {
    if (foundTicketId) window.open(`http://localhost:8000/api/solicitudes/${foundTicketId}/pdf`, '_blank');
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
          <h1 className="text-3xl font-bold text-white tracking-tight">Ventanilla de Trámites</h1>
          <p className="text-gray-400 mt-2">Complete el formulario para obtener su número de turno en la UAdeC.</p>
        </div>
      </div>

      <div className="flex space-x-1 bg-surfaceLight p-1 rounded-xl mb-6 max-w-2xl">
        <button
          onClick={() => { setMode('nuevo'); setStatus({ loading: false, msg: '', type: ''}); setFoundTicketId(null); }}
          className={clsx("w-full py-2.5 text-sm font-medium rounded-lg transition-all flex items-center justify-center gap-2", mode === 'nuevo' ? 'bg-primary text-white shadow-lg' : 'text-gray-400 hover:text-white hover:bg-white/5')}
        >
          <Ticket className="w-4 h-4" /> Nuevo Registro
        </button>
        <button
          onClick={() => { setMode('consultar'); setStatus({ loading: false, msg: '', type: ''}); setFoundTicketId(null); }}
          className={clsx("w-full py-2.5 text-sm font-medium rounded-lg transition-all flex items-center justify-center gap-2", mode === 'consultar' ? 'bg-primary text-white shadow-lg' : 'text-gray-400 hover:text-white hover:bg-white/5')}
        >
          <Search className="w-4 h-4" /> Consultar Turno
        </button>
        <button
          onClick={() => { setMode('modificar'); setStatus({ loading: false, msg: '', type: ''}); setFoundTicketId(null); }}
          className={clsx("w-full py-2.5 text-sm font-medium rounded-lg transition-all flex items-center justify-center gap-2", mode === 'modificar' ? 'bg-primary text-white shadow-lg' : 'text-gray-400 hover:text-white hover:bg-white/5')}
        >
          <Edit3 className="w-4 h-4" /> Modificar Datos
        </button>
      </div>

      <div className="glass-panel p-1 sm:p-8 relative">
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl pointer-events-none"></div>
        
        {status.msg && (
          <div className={clsx("p-4 mb-6 rounded-lg text-sm font-medium border", 
            status.type === 'error' ? 'bg-red-500/10 text-red-400 border-red-500/20' : 
            status.type === 'info' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 
            'bg-green-500/10 text-green-400 border-green-500/20'
          )}>
            {status.msg}
          </div>
        )}

        {(mode === 'modificar' || mode === 'consultar') && (
          <div className="mb-6 p-4 bg-surfaceLight rounded-xl border border-gray-700 flex gap-4 items-end">
             <div className="flex-1">
              <label className="block text-sm font-medium text-gray-300 mb-1">CURP Registrada</label>
              <input value={form.curp_alumno} onChange={e => setForm({...form, curp_alumno: e.target.value.toUpperCase()})} className={clsx("input-field font-mono", form.curp_alumno && (curpValid ? 'border-green-500 focus:ring-green-500' : 'border-red-500 focus:ring-red-500'))} placeholder="18 caracteres" maxLength={18} />
            </div>
            {mode === 'modificar' && (
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-300 mb-1">Número de Turno</label>
                <input value={turnoMod} onChange={e => setTurnoMod(e.target.value)} type="number" className="input-field" placeholder="Requerido para modificar" />
              </div>
            )}
            <button onClick={handleSearchToModify} disabled={!curpValid || (mode === 'modificar' && !turnoMod) || status.loading} className="btn-secondary h-[42px] flex items-center justify-center gap-2 px-6">
              <Search className="w-4 h-4" /> Buscar
            </button>
          </div>
        )}

        {mode === 'consultar' && foundTicketId && (
          <div className="flex flex-col items-center justify-center p-8 bg-surface rounded-xl border border-gray-700 mt-4 text-center">
            <CheckCircle className="w-16 h-16 text-green-500 mb-4" />
            <h3 className="text-2xl font-bold text-white mb-2">Ticket Encontrado</h3>
            <p className="text-gray-400 mb-6">Puede descargar una copia en PDF del comprobante original de su turno.</p>
            <button onClick={handleReprint} className="btn-primary flex items-center gap-2 px-8 py-3 text-lg">
              <Download className="w-5 h-5" /> Descargar Comprobante PDF
            </button>
          </div>
        )}

        {mode !== 'consultar' && (
        <form onSubmit={handleSubmit} className={clsx("relative z-10 grid grid-cols-1 md:grid-cols-2 gap-6 p-4", mode === 'modificar' && !form.quien_tramita && 'opacity-50 pointer-events-none')}>
          
          <div className="space-y-4 md:col-span-2">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-gray-800 pb-2">
              <User className="w-5 h-5 text-primary" /> Datos del Alumno
            </h3>
          </div>

          {mode === 'nuevo' && (
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-300 mb-1">CURP *</label>
              <input required value={form.curp_alumno} onChange={e => setForm({...form, curp_alumno: e.target.value.toUpperCase()})} className={clsx("input-field font-mono uppercase", form.curp_alumno && (curpValid ? 'border-green-500 focus:ring-green-500 shadow-[0_0_10px_rgba(34,197,94,0.2)]' : 'border-red-500 focus:ring-red-500'))} placeholder="Ingrese los 18 caracteres de la CURP" maxLength={18} />
              {form.curp_alumno && !curpValid && <p className="text-red-400 text-xs mt-1">Formato de CURP inválido o incompleto</p>}
              {curpValid && <p className="text-green-400 text-xs mt-1">CURP Válida ✓</p>}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Nombre(s) *</label>
            <input required disabled={mode==='modificar'} value={form.nombre} onChange={e => setForm({...form, nombre: e.target.value})} className="input-field disabled:opacity-50" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Apellido Paterno *</label>
            <input required disabled={mode==='modificar'} value={form.paterno} onChange={e => setForm({...form, paterno: e.target.value})} className="input-field disabled:opacity-50" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Apellido Materno *</label>
            <input required disabled={mode==='modificar'} value={form.materno} onChange={e => setForm({...form, materno: e.target.value})} className="input-field disabled:opacity-50" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Nivel Educativo *</label>
            <select required disabled={mode==='modificar'} value={form.nivel_id} onChange={e => setForm({...form, nivel_id: e.target.value})} className="input-field disabled:opacity-50">
              <option value="">Seleccione...</option>
              {catalogs.niveles.map((n:any) => <option key={n.id} value={n.id}>{n.nombre}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Municipio de Estudio *</label>
            <select required disabled={mode==='modificar'} value={form.municipio_id} onChange={e => setForm({...form, municipio_id: e.target.value})} className="input-field disabled:opacity-50">
              <option value="">Seleccione un municipio</option>
              {catalogs.municipios.map((m:any) => <option key={m.id} value={m.id}>{m.nombre}</option>)}
            </select>
          </div>

          <div className="space-y-4 md:col-span-2 mt-4">
            <h3 className="text-lg font-semibold text-white flex items-center gap-2 border-b border-gray-800 pb-2">
              <Ticket className="w-5 h-5 text-primary" /> Datos del Trámite y Contacto
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

          <div className="md:col-span-2 pt-6 flex flex-col md:flex-row justify-end gap-4">
            {mode === 'modificar' && foundTicketId && (
              <button type="button" onClick={handleReprint} className="px-8 py-3 flex items-center justify-center gap-2 font-bold rounded-lg border border-primary text-primary hover:bg-primary/10 transition-all">
                <Download className="w-5 h-5" />
                Reimprimir Ticket (PDF)
              </button>
            )}
            <button type="submit" disabled={status.loading || !isFormValid} className={clsx("px-8 py-3 flex items-center justify-center gap-2 font-bold rounded-lg shadow-lg transition-all", isFormValid ? 'bg-primary hover:bg-primaryHover text-white shadow-primary/20' : 'bg-gray-700 text-gray-400 cursor-not-allowed')}>
              {mode === 'nuevo' ? <Send className="w-5 h-5" /> : <Save className="w-5 h-5" />}
              {status.loading ? 'Procesando...' : (mode === 'nuevo' ? 'Generar Ticket de Turno' : 'Guardar Cambios')}
            </button>
          </div>
        </form>
        )}
      </div>
    </div>
  );
}
// Import Save locally to fix missing dependency
import { Save } from 'lucide-react';
