# MEMORIA — Consultorio Dental

> Archivo vivo. LEER al iniciar sesión. ACTUALIZAR al cerrar. Commit para persistir.

## Estado
- ✅ Fase 1: base + ventana 3 pestañas (Agenda/Pacientes/Historia)
- ✅ Fase 2: módulo pacientes (CRUD + búsqueda sin tildes + filas 30px)
- ✅ Fase 3: agenda + calendario tkcalendar (slots 08:00-18:30 cada 30min, valida hora ocupada, ventana maximizada, columnas anchas)
- ✅ Fase 4A: HISTORIA ODONTOLOGICA + componente ODONTOGRAMA (cuadrícula FDI reutilizable, 32 dientes)
- ⬜ 4B: Historia Urgencia · 4C: Hoja Evolución · 4D: Certificación Carta Dental (reusa odontograma) · 4E: Endodoncia · 4F: Dra Fawiza (5 registros admin)
- ⬜ Fase 5: exportar PDF (SOLO cuando las 6 plantillas estén replicadas)
- ⬜ Fase 6: pulido + estados de cita

## Decisiones tomadas
- Offline, local, sin servidor, sin nube, sin seguridad/login, 1 usuario, sin updates.
- Python 3.14 + Tkinter + SQLite + tkcalendar + reportlab.
- Una fase por turno; probar antes de avanzar.
- Odontograma = componente reutilizable (cuadrícula FDI, opción A). Instanciado en 4A (Odontológica) y 4D (Certificación). Las 2 imágenes de los PDFs son el MISMO odontograma.
- Export a PDF solo tras replicar las 6 plantillas (regla del usuario).
- Defaults asumidos sin confirmar explícita: paciente puede tener VARIAS historias (una por visita).

## Inventario plantillas (6 PDFs en Plantillas/)
A. HISTORIA ODONTOLOGICA (2 pág, imagen=odontograma 693×348)
B. HISTORIA URGENCIA (1 pág)
C. HOJA DE EVOLUCION (2 pág, tabla por visita)
D. CERTIFICACION CARTA DENTAL (1 pág, imagen=odontograma 417×156)
E. HISTORIA ENDODONCIA (3 pág, checkboxes + tabla conductos)
F. DRA. FAWIZA TAYLOR (7 pág = 5 registros admin: temp ambiente, insumos, esterilización, glutaraldehído, temp nevera)

## Prioridad acordada
4A Odontológica → 4B Urgencia → 4C Evolución → 4D Certificación → 4E Endodoncia → 4F Administrativos.

## Estructura (adicionales Fase 4A)
| Archivo | Función |
|---------|---------|
| `odontograma.py` | Componente reutilizable: 32 dientes FDI, combos de estado, `get_estados()`/`set_estados()`. Usado en 4A y 4D |
| `historia_odontologica.py` | Formulario completo (identificación, anamnesis, hábitos, odontograma, examen oral 16 ítems N/AN, diagnóstico). `cargar()`/`datos()`/`limpiar()` |
| `historia.py` | Pestaña Historia: selector paciente + documento, lista de historias, form con scroll. Tabla `DOCUMENTOS` registra cada plantilla (extensible a 4B-4F) |
| Tabla `historia_odontologica` | exámen oral y odontograma guardados como JSON en columnas TEXT |

## Reglas de sesión / convenciones
- Tkinter, UI en español, sin comentarios en código salvo pedido.
- `db.py` concentra TODO el SQL; pestañas no escriben SQL directo.
- Tabla nueva → registrar en `init_db()`. Ventanas: `Toplevel`+`grab_set()`+`transient()`.
- `fuente` en tkcalendar debe ser tupla `("Segoe UI", N)`, no string.
- Maximizar ventana: `attributes("-zoomed", True)` en Linux (NO `state("zoomed")`).
- Rowheight de treeview se setea con `ttk.Style(...).configure("Treeview", rowheight=N)`.
- Correr: `./run.sh` (activa .venv). Test rápido: `source .venv/bin/activate && python -c ...`.