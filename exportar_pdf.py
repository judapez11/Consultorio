import html
import os
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / "historias_pdf"

SECTORES = ["vestibular", "mesial", "oclusal", "distal", "lingual"]
SECTOR_NOMBRE = {"vestibular": "Vestibular", "mesial": "Mesial",
                 "oclusal": "Oclusal", "distal": "Distal",
                 "lingual": "Lingual"}

ESTILOS = getSampleStyleSheet()
ESTILOS.add(ParagraphStyle("TituloDoc", parent=ESTILOS["Title"], fontSize=16,
                           spaceAfter=4))
ESTILOS.add(ParagraphStyle("SubDoc", parent=ESTILOS["Normal"], fontSize=10,
                           textColor=colors.grey, spaceAfter=10))
ESTILOS.add(ParagraphStyle("Seccion", parent=ESTILOS["Heading2"], fontSize=12,
                           spaceBefore=8, spaceAfter=4))
ESTILOS.add(ParagraphStyle("Celda", parent=ESTILOS["Normal"], fontSize=9,
                           leading=11))
ESTILOS.add(ParagraphStyle("CeldaBold", parent=ESTILOS["Normal"], fontSize=9,
                           leading=11, fontName="Helvetica-Bold"))


def _e(texto):
    return html.escape(str(texto or ""))


def _par(texto, estilo="Celda"):
    return Paragraph(_e(texto), ESTILOS[estilo])


def _nombre_archivo(tipo, paciente, fecha):
    limpio = re.sub(r"[^A-Za-z0-9_.-]+", "_", paciente).strip("_")
    return f"{tipo}_{limpio}_{fecha}.pdf"


def _documento(ruta, titulo, subtitulo, story):
    PDF_DIR.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(str(ruta), pagesize=A4,
                            topMargin=15 * mm, bottomMargin=15 * mm,
                            leftMargin=15 * mm, rightMargin=15 * mm)
    head = [Paragraph(_e(titulo), ESTILOS["TituloDoc"]),
            Paragraph(_e(subtitulo), ESTILOS["SubDoc"]),
            Spacer(1, 4 * mm)]
    doc.build(head + story)
    return str(ruta)


def _tabla_pares(pares, anchos=(55 * mm, 125 * mm)):
    filas = []
    for etiqueta, valor in pares:
        filas.append([_par(etiqueta, "CeldaBold"), _par(valor)])
    tabla = Table(filas, colWidths=list(anchos))
    tabla.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, colors.lightgrey),
    ]))
    return tabla


def _seccion(titulo, pares):
    return [Paragraph(_e(titulo), ESTILOS["Seccion"]), _tabla_pares(pares)]


def _tabla_odontograma(d):
    """Tabla por cuadrante: 16 dientes por arco, sectores no-Sano por celda."""
    sup = ["18", "17", "16", "15", "14", "13", "12", "11"] + \
          ["21", "22", "23", "24", "25", "26", "27", "28"]
    inf = ["38", "37", "36", "35", "34", "33", "32", "31"] + \
          ["41", "42", "43", "44", "45", "46", "47", "48"]
    datos = d or {}

    def celda(diente):
        sectores = datos.get(diente) or {}
        if all(v == "Ausente" for v in sectores.values()):
            return _par("AUSENTE")
        lineas = [diente]
        pintados = [(SECTOR_NOMBRE[z], v) for z, v in sectores.items()
                    if v and v != "Sano"]
        if not pintados:
            lineas.append("OK")
        else:
            lineas.extend(f"{n}: {v}" for n, v in pintados)
        return Paragraph("<br/>".join(_e(x) for x in lineas), ESTILOS["Celda"])

    t_sup = Table([[celda(d) for d in sup]], colWidths=[16 * mm] * 16)
    t_inf = Table([[celda(d) for d in inf]], colWidths=[16 * mm] * 16)
    for t in (t_sup, t_inf):
        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
        ]))
    return [Paragraph("SUPERIOR", ESTILOS["CeldaBold"]), t_sup,
            Spacer(1, 2 * mm),
            Paragraph("INFERIOR", ESTILOS["CeldaBold"]), t_inf]


def exportar_odontologica(paciente, datos, ruta):
    fecha = datos.get("fecha", "")
    story = _seccion("1. Identificacion", [
        ("Paciente", paciente), ("Fecha", fecha),
        ("Ocupacion", datos.get("ocupacion")),
        ("Estado civil", datos.get("estado_civil")),
        ("Fecha de nacimiento", datos.get("fecha_nacimiento")),
    ])
    acu = [datos.get("acudiente_apellido1"), datos.get("acudiente_apellido2"),
           datos.get("acudiente_nombre")]
    if any(acu):
        story += _seccion("Acudiente", [
            ("Nombre", " ".join(x for x in acu if x)),
            ("Parentesco", datos.get("acudiente_parentesco")),
            ("Direccion", datos.get("acudiente_direccion")),
            ("Telefono", datos.get("acudiente_telefono")),
        ])
    story += _seccion("2. Anamnesis", [
        ("Antecedentes personales", datos.get("antecedentes_personales")),
        ("Antecedentes familiares", datos.get("antecedentes_familiares")),
        ("Motivo de la consulta", datos.get("motivo_consulta")),
    ])
    story += _seccion("3. Habitos", [
        ("Cepillado", datos.get("cepillado")),
        ("Uso de seda dental", datos.get("seda")),
        ("Uso de enjuague", datos.get("enjuague")),
    ])
    story += [Paragraph("4. Odontograma", ESTILOS["Seccion"])]
    story += _tabla_odontograma(datos.get("odontograma"))
    examen = datos.get("examen_oral") or {}
    story += _seccion("5. Examen de cavidad oral", [
        (item, "Alterado" if examen.get(item) == "AN" else "Normal")
        for item in ("Labios", "Encias", "Lengua", "Paladar", "Maxilares")
    ])
    story += _seccion("6. Diagnostico", [
        ("Tejido blando", datos.get("diagnostico_tejido_blando")),
        ("Dental", datos.get("diagnostico_dental")),
        ("Periodontal", datos.get("diagnostico_periodontal")),
        ("Craneofacial", datos.get("diagnostico_craneofacial")),
        ("Oclusion", datos.get("diagnostico_oclusion")),
    ])
    return _documento(ruta, "HISTORIA CLINICA ODONTOLOGICA",
                      f"Paciente: {paciente}  ·  Fecha: {fecha}", story)


def exportar_urgencia(paciente, datos, ruta):
    fecha = datos.get("fecha", "")
    story = _seccion("Datos del paciente", [
        ("Paciente", datos.get("nombre") or paciente),
        ("Identificacion", datos.get("identificacion")),
        ("Edad", datos.get("edad")), ("Direccion", datos.get("direccion")),
        ("Telefono", datos.get("telefono")),
        ("Acudiente", datos.get("acudiente")),
    ])
    story += _seccion("Motivo de la consulta", [
        ("", datos.get("motivo_consulta"))])
    ant = [k for k in ("ant_quirurgicos", "ant_patologicos",
                       "ant_toxicoalergicos", "ant_transfusionales",
                       "ant_traumaticos", "ant_otros") if datos.get(k)]
    story += _seccion("Antecedentes personales", [("Marcados",
                     ", ".join(ant) or "Ninguno")])
    story += _seccion("Antecedentes familiares", [
        ("", datos.get("antecedentes_familiares"))])
    story += _seccion("Examen fisico", [("", datos.get("examen_fisico"))])
    story += _seccion("Examen radiologico", [("", datos.get("examen_radiologico"))])
    story += _seccion("Impresion diagnostica", [
        ("", datos.get("impresion_diagnostica"))])
    story += _seccion("Plan de tratamiento", [("", datos.get("plan_tratamiento"))])
    story += _seccion("Firmas", [
        ("Paciente", datos.get("firma_paciente")),
        ("Odontologo", datos.get("firma_odontologo"))])
    return _documento(ruta, "HISTORIA CLINICA POR URGENCIA",
                      f"Paciente: {paciente}  ·  Fecha: {fecha}", story)


def exportar_evolucion(paciente, datos, ruta):
    fecha = datos.get("fecha", "")
    story = _seccion("Evolucion del paciente", [
        ("Paciente", paciente), ("Fecha", fecha),
        ("Detalle", datos.get("detalle"))])
    return _documento(ruta, "EVOLUCION DEL PACIENTE",
                      f"Paciente: {paciente}  ·  Fecha: {fecha}", story)


def exportar_carta(paciente, datos, ruta):
    fecha = datos.get("fecha", "")
    story = _seccion("Datos del certificado", [
        ("Paciente", datos.get("nombre") or paciente),
        ("Apellidos", datos.get("apellidos")), ("Edad", datos.get("edad")),
        ("Documento", f"{datos.get('tipo_documento')} {datos.get('num_documento')}"),
        ("Entidad solicitante", datos.get("entidad_solicitante")),
    ])
    story += _seccion("Motivo de la consulta", [
        ("", datos.get("motivo_consulta"))])
    story += [Paragraph("Odontograma", ESTILOS["Seccion"])]
    story += _tabla_odontograma(datos.get("odontograma"))
    story += _seccion("Resumen", [
        ("Caries", datos.get("caries")), ("Obturados", datos.get("obturados"))])
    examen = datos.get("examen") or {}
    story += _seccion("Examen de cavidad oral", [
        (k.replace("_", " ").capitalize(), v) for k, v in examen.items()])
    story += _seccion("Plan de tratamiento", [("", datos.get("plan_tratamiento"))])
    story += _seccion("Firma", [("", datos.get("firma"))])
    return _documento(ruta, "CERTIFICACION DE CARTA DENTAL",
                      f"Paciente: {paciente}  ·  Fecha: {fecha}", story)


def exportar_endodoncia(paciente, datos, ruta):
    fecha = datos.get("fecha", "")
    story = _seccion("Datos del paciente", [
        ("Paciente", datos.get("nombre") or paciente),
        ("Identificacion", datos.get("identificacion")),
        ("Edad", datos.get("edad")), ("Direccion", datos.get("direccion")),
        ("Telefono", datos.get("telefono")),
        ("Referido por", datos.get("referido_por")),
        ("E.P.S.", datos.get("eps")),
    ])
    story += _seccion("Motivo de la consulta", [
        ("", datos.get("motivo_consulta"))])
    ant = [k for k, v in (datos.get("antecedentes") or {}).items() if v]
    story += _seccion("Antecedentes", [("Marcados",
                     ", ".join(ant) or "Ninguno")])
    story += _seccion("Signos vitales", [
        ("P.A", datos.get("pa")), ("F.R", datos.get("fr")),
        ("F.C", datos.get("fc"))])
    story += _seccion("Observaciones", [("", datos.get("observaciones"))])
    story += _seccion("Antecedentes medico-familiares", [
        ("", datos.get("antecedentes_familiares"))])
    story += _seccion("Diente por tratar", [("", datos.get("diente_tratar"))])
    cli = [k for k, v in (datos.get("examen_clinico") or {}).items() if v]
    rad = [k for k, v in (datos.get("examen_radiografico") or {}).items() if v]
    dol = [k for k, v in (datos.get("dolor") or {}).items() if v]
    story += _seccion("Examen clinico", [("Marcados", ", ".join(cli) or "Ninguno")])
    story += _seccion("Examen radiografico", [("Marcados", ", ".join(rad) or "Ninguno")])
    story += _seccion("Dolor", [("Marcados", ", ".join(dol) or "Ninguno")])
    story += _seccion("Diagnostico", [("", datos.get("diagnostico"))])
    story += _seccion("Pronostico", [("", datos.get("pronostico"))])
    story += _seccion("Plan de tratamiento", [("", datos.get("plan_tratamiento"))])
    conductos = datos.get("conductos") or []
    if any(any(c for c in fila.values()) for fila in conductos):
        cab = ["Long. tentativa", "Long. definitiva", "Referencia",
               "Lima apical", "Sistema de preparacion"]
        filas = [[_par(c, "CeldaBold") for c in cab]]
        for fila in conductos:
            filas.append([_par(fila.get(c, "")) for c in
                          ("long_tentativa", "long_definitiva", "referencia",
                           "lima_apical", "sistema_preparacion")])
        t = Table(filas, colWidths=[34 * mm] * 5)
        t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                               ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        story += [Paragraph("Conductos", ESTILOS["Seccion"]), t]
    story += _seccion("Observaciones finales", [
        ("", datos.get("observaciones_finales"))])
    story += _seccion("Firmas", [
        ("Paciente", datos.get("firma_paciente")),
        ("Endodoncista", datos.get("firma_endodoncista"))])
    return _documento(ruta, "HISTORIA CLINICA DE ENDODONCIA",
                      f"Paciente: {paciente}  ·  Fecha: {fecha}", story)


def exportar_registro(titulo, columnas, filas, ruta):
    cab = [_par(c, "CeldaBold") for c in columnas]
    datos_tabla = [cab]
    for fila in filas:
        datos_tabla.append([_par(fila.get(c[0], "")) for c in columnas])
    ancho = max(40, int(170 * mm / len(columnas)))
    t = Table(datos_tabla, colWidths=[ancho * mm] * len(columnas),
              repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
    ]))
    return _documento(ruta, titulo, "", [t])


def exportar_por_tipo(tipo, paciente, datos, fecha=""):
    """Punto de entrada unico: genera el PDF del formulario y devuelve la ruta."""
    archivo = _nombre_archivo(tipo, paciente, fecha or datos.get("fecha", ""))
    ruta = PDF_DIR / archivo
    funcs = {
        "Historia Odontologica": exportar_odontologica,
        "Historia de Urgencia": exportar_urgencia,
        "Hoja de Evolucion": exportar_evolucion,
        "Certificacion Carta Dental": exportar_carta,
        "Historia de Endodoncia": exportar_endodoncia,
    }
    return funcs[tipo](paciente, datos, ruta)