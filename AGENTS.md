# AGENTS.md — Consultorio Dental

## Qué es
App de escritorio local (Python + Tkinter) para consultorio odontológico: gestión de pacientes, agenda de citas e historias clínicas. **Offline, sin servidor, sin nube, sin seguridad/login, un solo usuario, sin actualizaciones.**

## Stack
- Python 3.14 + Tkinter + SQLite (todo local, 1 archivo `datos.db`)
- `tkcalendar` → solo `Calendar` (la pestaña Agenda lo usa; el resto usa canvas propios)
- `reportlab` → exportar a PDF (Fase 5, aún no usada)
- Entorno: `.venv/` (activar con `source .venv/bin/activate`)

## Cómo correr
```bash
cd ~/Documentos/Consultorio && ./run.sh
```
(`run.sh` activa el venv y lanza `main.py`)

## ⚠️ Rendimiento (X server lento)
- El `grid`/`pack` de Tk con ~50 widgets tarda ~3-5s en este sistema; los `Canvas` son gratis (400 items = 0.00s).
- **Regla: dibujar en Canvas, no crear widgets.** Evitar `tk.Button`/`ttk.Button`/Combobox en masa.
- Odontograma, examen oral y campos de fecha interactivos se dibujan en canvas.

## Estructura
| Archivo | Función |
|---------|---------|
| `main.py` | Lanzador: init_db + App |
| `app.py` | Ventana principal (maximizada). **Barra global de paciente arriba** (`tk.Button` + `tk.Menu` con postcommand) + Notebook: Agenda, Pacientes, 1 pestaña por documento (`DOCUMENTOS`). Guarda `paciente_id`; al cambiar notifica a todas las tabs. Paciente global compartido (fuera del área de formularios → inmune al bug de bloqueo) |
| `db.py` | Conexión SQLite + DAO (pacientes, citas, historias odontológicas, urgencia, evolución) |
| `pacientes.py` | Pestaña Pacientes: CRUD + búsqueda sin tildes, filas rowheight=30 |
| `agenda.py` | Pestaña Agenda: calendario tkcalendar, slots 30min 08:00-18:30, valida hora ocupada |
| `historia.py` | **`DocumentoTab`**: pestaña por tipo de documento. Selector de paciente = **`tk.Listbox` visible + scrollbar** (sin popup → robusto; escala a cientos de pacientes). Guarda: `tiene_contenido()` → confirmar antes de cambiar. Botón **Cancelar** descarta. `DOCUMENTOS` registra cada plantilla (4D-4F = entrada nueva → pestaña sola) |
| `historia_odontologica.py` | Formulario Historia Odontológica (Fase 4A): identificación + checkbox menor/acudiente, anamnesis, hábitos, odontograma, examen oral, diagnóstico. `cargar()`/`datos()`/`limpiar()`/`validar()` |
| `historia_urgencia.py` | Formulario Historia de Urgencia (Fase 4B): datos paciente, motivo, antecedentes (checkbuttons), exámenes, impresión, plan, firmas. `cargar()`/`datos()`/`limpiar()`/`validar()` + `prefill_nombre()` |
| `historia_evolucion.py` | Formulario Hoja de Evolución (Fase 4C): fecha, detalle, firmas. `cargar()`/`datos()`/`limpiar()`/`validar()` |
| `historia_carta.py` | Formulario Certificación Carta Dental (Fase 4D): datos + tipo doc (radios CC/TI/RC) + motivo + **odontograma reutilizado** + resumen SI/NO + examen 8 ítems en canvas + plan + firma. `cargar()`/`datos()`/`limpiar()`/`validar()`/`tiene_contenido()`/`prefill_nombre()` |
| `odontograma.py` | Canvas: grid 2×2 por cuadrante, cada cuadrante 4×2, 5 sectores/diente, paleta de estados, clic derecho = ausente. API `get_estados()`/`set_estados()` |
| `campo_fecha.py` | Campo de fecha editable con máscara dd/mm/yyyy (sin calendario; evita el bug de bloqueo del combo). `get_date()`/`set_date()`/`limpiar()` |
| `mi_calendario.py` | Calendario propio en canvas (rápido). Actualmente sin uso directo (agenda usa tkcalendar; fechas usan campo_fecha) |
| `run.sh` | Lanzador |
| `Plantillas/` | **6 PDFs plantilla** de historias clínicas por replicar |
| `MEMORIA.md` | **LEER PRIMERO**: estado actual, decisiones, fases. Actualizar al cierre de cada sesión |
| `.venv/`, `datos.db`, `__pycache__/` | Ignorados en git |

## Estado del plan
- ✅ Fase 1: base + ventana 3 pestañas
- ✅ Fase 2: módulo pacientes
- ✅ Fase 3: agenda + calendario
- ✅ Fase 4A: HISTORIA ODONTOLOGICA (+ componente ODONTOGRAMA por sectores)
- ✅ Fase 4B: HISTORIA DE URGENCIA
- ✅ Fase 4C: HOJA DE EVOLUCION
- ✅ Fase 4D: CERTIFICACION CARTA DENTAL (reusa odontograma)
- ⬜ 4E: Endodoncia · 4F: Dra Fawiza (5 registros admin)
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
- **Odontograma:** los rótulos de zonas comparten el tag del rectángulo (para clic); al repintar con `itemconfig`, cambiar `fill` SOLO a items de tipo `rectangle` (no a `text`).
- **Canvas interactivo:** los textos sobre zonas clicables deben compartir tag y NO usar `state="disabled"` (deja el texto invisible).