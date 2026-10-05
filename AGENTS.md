# AGENTS.md — Consultorio Dental

## Qué es
App de escritorio local (Python + Tkinter) para consultorio odontológico: gestión de pacientes, agenda de citas e historias clínicas. **Offline, sin servidor, sin nube, sin seguridad/login, un solo usuario, sin actualizaciones.**

## Stack
- Python 3.14 + Tkinter + SQLite (todo local, 1 archivo `datos.db`)
- `tkcalendar` → solo `Calendar` (la pestaña Agenda lo usa; el resto usa canvas propios)
- `reportlab` → exportar a PDF (Fase 5, usada)
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
| `historia_endodoncia.py` | Formulario Historia de Endodoncia (Fase 4E): datos + motivo + **56 checkboxes en canvas** (`CanvasChecks`: 23 antecedentes + 11 clínico + 11 radiográfico + 11 dolor) + vitales + tabla de conductos (4 filas × 5 col) + diagnóstico/pronóstico/plan + firmas. `cargar()`/`datos()`/`limpiar()`/`validar()`/`tiene_contenido()`/`prefill_nombre()` |
| `registros.py` | **`RegistroTab`** (Fase 4F): registros administrativos ledger (temp ambiente/nevera, insumos, esterilización, glutaraldehído). Tabla + dialogo Agregar/Editar/Eliminar + **Exportar PDF**. Fechas con `CampoFecha` → ISO. CRUD genérico en `db.py` (`REGISTROS`/`REGISTROS_CRUD`). No son de paciente |
| `exportar_pdf.py` | **Exportar PDF (Fase 5)** con reportlab. `exportar_por_tipo(tipo, paciente, datos)` genera el PDF de cada formulario; `_tabla_odontograma` pinta el odontograma (sectores no-Sano por celda); `exportar_registro` para ledgers admin. Salida en `historias_pdf/` (gitignored). Botón "Exportar PDF" en cada pestaña |
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
- ✅ Fase 4E: HISTORIA DE ENDODONCIA (56 checkboxes en canvas, tabla de conductos)
- ✅ Fase 4F: REGISTROS ADMINISTRATIVOS DRA. FAWIZA (5 ledgers: temp ambiente/nevera, insumos, esterilización, glutaraldehído)
- ✅ Fase 5: EXPORTAR A PDF (reportlab; todas las plantillas + registros admin)
- ✅ Fase 6: PULIDO — estados de cita (pendiente/realizada/cancelada; columna estado + color calendario)

**Detalles de fases y decisiones en `MEMORIA.md` — consultar ahí antes de trabajar.**

## Convenciones
- Una fase por turno; probar (sintaxis + ejecución) antes de avanzar.
- UI en español. Sin comentarios en código salvo que se pida.
- `db.py` concentra todo SQL; las pestañas no escriben SQL directo.
- Nombres de funciones/archivos en español.
- Tablas SQLite nuevas → registrar también en `init_db()`.
- Ventana nueva dentro de la app: `Toplevel` + `grab_set()` + `transient()`.
- **Empaquetado (PyInstaller):** `db.py` y `exportar_pdf.py` usan `sys.frozen` → `BASE_DIR = Path(sys.executable).parent` para que `datos.db`/`historias_pdf/` queden **junto al ejecutable** (en onefile `__file__` apunta a `_MEIPASS`, que se borra). Maximizar: `state("zoomed")` (Windows) con fallback `attributes("-zoomed", True)` (Linux). Tabs no scrollables (Pacientes/Agenda) deben caber en 900×600 (treeview con `height` fijo).
- **Odontograma:** los rótulos de zonas comparten el tag del rectángulo (para clic); al repintar con `itemconfig`, cambiar `fill` SOLO a items de tipo `rectangle` (no a `text`).
- **Canvas interactivo:** los textos sobre zonas clicables deben compartir tag y NO usar `state="disabled"` (deja el texto invisible).