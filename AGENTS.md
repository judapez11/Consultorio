# AGENTS.md — Consultorio Dental

## Qué es
App de escritorio local (Python + Tkinter) para consultorio odontológico: gestión de pacientes, agenda de citas e historias clínicas. **Offline, sin servidor, sin nube, sin seguridad/login, un solo usuario, sin actualizaciones.**

## Stack
- Python 3.14 + Tkinter + SQLite (todo local, 1 archivo `datos.db`)
- `tkcalendar` → calendario visual
- `reportlab` → exportar a PDF (Fase 5, aún no usada)
- Entorno: `.venv/` (activar con `source .venv/bin/activate`)

## Cómo correr
```bash
cd ~/Documentos/Consultorio && ./run.sh
```
(`run.sh` activa el venv y lanza `main.py`)

## Estructura
| Archivo | Función |
|---------|---------|
| `main.py` | Lanzador: init_db + App |
| `app.py` | Ventana principal (maximizada), pestañas: Agenda / Pacientes / Historia |
| `db.py` | Conexión SQLite + DAO (pacientes, citas) |
| `pacientes.py` | Pestaña Pacientes: CRUD + búsqueda sin tildes, filas rowheight=30 |
| `agenda.py` | Pestaña Agenda: calendario tkcalendar, slots 30min 08:00-18:30, valida hora ocupada |
| `run.sh` | Lanzador |
| `Plantillas/` | **6 PDFs plantilla** de historias clínicas por replicar |
| `MEMORIA.md` | **LEER PRIMERO**: estado actual, decisiones, fases. Actualizar al cierre de cada sesión |
| `.venv/`, `datos.db`, `__pycache__/` | Ignorados en git |

## Estado del plan
- ✅ Fase 1: base + ventana 3 pestañas
- ✅ Fase 2: módulo pacientes
- ✅ Fase 3: agenda + calendario
- 🔨 Fase 4A: HISTORIA ODONTOLOGICA (+ componente ODONTOGRAMA)
- ⬜ 4B: Historia Urgencia · 4C: Hoja Evolución · 4D: Certificación Carta Dental (reusa odontograma) · 4E: Endodoncia · 4F: Dra Fawiza (5 registros admin)
- ⬜ Fase 5: exportar PDF (solo cuando las 6 plantillas estén replicadas)
- ⬜ Fase 6: pulido + estados de cita

**Detalles de fases y decisiones en `MEMORIA.md` — consultar ahí antes de trabajar.**

## Convenciones
- Una fase por turno; probar (sintaxis + ejecución) antes de avanzar.
- UI en español. Sin comentarios en código salvo que se pida.
- `db.py` concentra todo SQL; las pestañas no escriben SQL directo.
- Nombres de funciones/archivos en español.
- Tablas SQLite nuevas → registrar también en `init_db()`.
- Ventana nueva dentro de la app: `Toplevel` + `grab_set()` + `transient()`.