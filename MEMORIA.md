# MEMORIA — Consultorio Dental

> Archivo vivo. LEER al iniciar sesión. ACTUALIZAR al cerrar. Commit para persistir.

## Estado
- ✅ Fase 1: base + ventana 3 pestañas (Agenda/Pacientes/Historia)
- ✅ Fase 2: módulo pacientes (CRUD + búsqueda sin tildes + filas 30px)
- ✅ Fase 3: agenda + calendario tkcalendar (slots 08:00-18:30 cada 30min, valida hora ocupada, ventana maximizada, columnas anchas)
- ✅ Fase 4A: HISTORIA ODONTOLOGICA + componente ODONTOGRAMA (cuadrícula FDI reutilizable, 32 dientes)
- ✅ Fase 4B: HISTORIA DE URGENCIA (formulario + tabla historia_urgencia)
- ✅ Fase 4C: HOJA DE EVOLUCION (tabla evolucion, entrada por visita; columna del tree configurable "Detalle")
- ✅ Fase 4D: CERTIFICACION CARTA DENTAL (tabla carta_dental, reusa OdontogramaFrame; examen 8 ítems SI/NO en canvas; tipo doc = radios CC/TI/RC)
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
| `odontograma.py` | **Canvas, grid 2×2 por cuadrante, cada cuadrante 4×2**. Ocupa 100% del ancho (`fill=x` + `<Configure>`→`_dibujar`, sin tope). 5 sectores/diente (Vest/Mes/Ocl/Dis/Ling) con mapeo clínico por cuadrante (mesial a línea media, vestibular hacia fuera). Paleta 7 estados con colores (Sano/Caries/Obturado/Ausente/Endodoncia/Protesis/Otro). Clic en sector pinta, re-clic = Sano, **clic derecho = diente ausente** (✕). ⚠️ Los rótulos comparten el tag del rectángulo (para clic) y `_pintar` cambia fill SOLO a items `rectangle` (no text, o desaparecen). API `get_estados()`→`{diente:{sector:estado}}`, `set_estados()` acepta dict y **legacy plano**. |
| `historia_odontologica.py` | Formulario completo (identificación, anamnesis, hábitos, odontograma, examen oral 16 ítems N/AN, diagnóstico). **Checkbox "¿Es menor de edad?"** → muestra/oculta frame Acudiente (`_toggle_acudiente`, pack before=anamnesis). `validar()`: si menor → obliga apellido/nombre/parentesco/dirección/teléfono del acudiente; adulto → sin requisitos. `cargar()` deduce menor si hay datos de acudiente. Entries con `sticky="we"` + weight → 100% |
| `historia.py` | **`DocumentoTab`**: pestaña por tipo de documento. Selector de paciente = **`tk.Listbox` visible + scrollbar** (widget plano, sin popup → robusto; soporta 100+ pacientes). Clic → `_list_seleccion` → `_intentar_cambiar`; rueda del listbox hace `break` (no mueve el form). ⚠️ `ScrollableFrame._rueda` ignora `tk.Listbox`. Guarda: `tiene_contenido()` → askyesno antes de cambiar (No revierte selección). Botón **Cancelar** descarta. Lista (id/fecha/motivo), form con scroll, `_guardar` llama `form.validar()` |
| `campo_fecha.py` | **Campo de fecha editable con máscara** (`CampoFecha`): Entry dd/mm/yyyy, solo dígitos + barras automáticas (`_formatear_fecha`), default hoy. `get_date()` → date o None, `set_date()`, `limpiar()`. ⚠️ SIN calendario ni Toplevel ni grab (elimina el bug de bloqueo del combo). Los 3 formularios validan `get_date() is None` → bloquean con "Fecha invalida"; `datos()` guarda ISO solo si válida, si no `""` (nunca formatos mezclados) |
| `historia_urgencia.py` | Formulario Historia de Urgencia (Fase 4B): datos del paciente (fecha CampoFecha + nombre con prefill), motivo, 6 antecedentes personales (checkbuttons), antecedentes familiares, examen físico/radiológico, impresión diagnóstica, plan, firmas + CC. `cargar()`/`datos()`/`limpiar()`/`validar()` (obliga motivo). `prefill_nombre()` lo llama `historia.py` al crear form |
| `historia_evolucion.py` | Formulario Hoja de Evolución (Fase 4C): fecha + detalle (Text) + firmas (paciente/profesional). `validar()` obliga detalle. `listar_evolucion` devuelve `detalle AS motivo_consulta` para el tree |
| Columna tree configurable | `DOCUMENTOS[...]["columna"]` (ej. "Detalle"); `_nueva()` llama `_refrescar_historias()` para actualizar encabezado y lista al cambiar de documento |
| Tabla `historia_odontologica` | exámen oral y odontograma guardados como JSON en columnas TEXT |
| Tabla `historia_urgencia` | antecedentes personales como 6 columnas INTEGER (0/1) |

## Reglas de sesión / convenciones
- Tkinter, UI en español, sin comentarios en código salvo pedido.
- `db.py` concentra TODO el SQL; pestañas no escriben SQL directo.
- Tabla nueva → registrar en `init_db()`. Ventanas: `Toplevel`+`grab_set()`+`transient()`.
- `fuente` en tkcalendar debe ser tupla `("Segoe UI", N)`, no string.
- Maximizar ventana: `attributes("-zoomed", True)` en Linux (NO `state("zoomed")`).
- Rowheight de treeview se setea con `ttk.Style(...).configure("Treeview", rowheight=N)`.
- Correr: `./run.sh` (activa .venv). Test rápido: `source .venv/bin/activate && python -c ...`.