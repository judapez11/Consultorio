import sqlite3
import unicodedata
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "datos.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                direccion TEXT,
                email TEXT
            );

            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL,
                motivo TEXT,
                estado TEXT DEFAULT 'pendiente',
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS historia_odontologica (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                ocupacion TEXT,
                estado_civil TEXT,
                fecha_nacimiento TEXT,
                acudiente_apellido1 TEXT,
                acudiente_apellido2 TEXT,
                acudiente_nombre TEXT,
                acudiente_direccion TEXT,
                acudiente_telefono TEXT,
                acudiente_parentesco TEXT,
                antecedentes_personales TEXT,
                antecedentes_familiares TEXT,
                motivo_consulta TEXT,
                cepillado TEXT,
                seda TEXT,
                enjuague TEXT,
                examen_oral TEXT,
                odontograma TEXT,
                diagnostico_tejido_blando TEXT,
                diagnostico_dental TEXT,
                diagnostico_periodontal TEXT,
                diagnostico_craneofacial TEXT,
                diagnostico_oclusion TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS historia_urgencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                nombre TEXT,
                identificacion TEXT,
                edad TEXT,
                direccion TEXT,
                telefono TEXT,
                acudiente TEXT,
                motivo_consulta TEXT,
                ant_quirurgicos INTEGER DEFAULT 0,
                ant_patologicos INTEGER DEFAULT 0,
                ant_toxicoalergicos INTEGER DEFAULT 0,
                ant_transfusionales INTEGER DEFAULT 0,
                ant_traumaticos INTEGER DEFAULT 0,
                ant_otros INTEGER DEFAULT 0,
                antecedentes_familiares TEXT,
                examen_fisico TEXT,
                examen_radiologico TEXT,
                impresion_diagnostica TEXT,
                plan_tratamiento TEXT,
                firma_paciente TEXT,
                cc_paciente TEXT,
                firma_odontologo TEXT,
                cc_odontologo TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS carta_dental (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                nombre TEXT,
                apellidos TEXT,
                edad TEXT,
                num_documento TEXT,
                tipo_documento TEXT,
                entidad_solicitante TEXT,
                motivo_consulta TEXT,
                caries TEXT,
                obturados TEXT,
                examen TEXT,
                odontograma TEXT,
                plan_tratamiento TEXT,
                firma TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS historia_endodoncia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                nombre TEXT,
                identificacion TEXT,
                edad TEXT,
                direccion TEXT,
                telefono TEXT,
                referido_por TEXT,
                eps TEXT,
                motivo_consulta TEXT,
                antecedentes TEXT,
                pa TEXT,
                fr TEXT,
                fc TEXT,
                observaciones TEXT,
                antecedentes_familiares TEXT,
                diente_tratar TEXT,
                examen_clinico TEXT,
                examen_radiografico TEXT,
                dolor TEXT,
                diagnostico TEXT,
                pronostico TEXT,
                plan_tratamiento TEXT,
                conductos TEXT,
                observaciones_finales TEXT,
                firma_paciente TEXT,
                firma_endodoncista TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS evolucion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                detalle TEXT,
                firma_paciente TEXT,
                firma_profesional TEXT,
                FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
            );
            """
        )


def _sin_tildes(texto):
    texto = texto.lower()
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )


def listar_pacientes(busqueda=""):
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM pacientes ORDER BY nombre").fetchall()
    if busqueda:
        b = _sin_tildes(busqueda.strip())
        rows = [r for r in rows if b in _sin_tildes(r["nombre"])]
    return rows


def guardar_paciente(datos):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO pacientes (nombre, telefono, direccion, email)"
            " VALUES (?, ?, ?, ?)",
            (datos["nombre"], datos["telefono"], datos["direccion"], datos["email"]),
        )
        return cur.lastrowid


def actualizar_paciente(pid, datos):
    with get_conn() as conn:
        conn.execute(
            "UPDATE pacientes SET nombre=?, telefono=?, direccion=?, email=?"
            " WHERE id=?",
            (datos["nombre"], datos["telefono"], datos["direccion"], datos["email"], pid),
        )


def borrar_paciente(pid):
    with get_conn() as conn:
        conn.execute("DELETE FROM pacientes WHERE id=?", (pid,))


def listar_citas(fecha=None):
    with get_conn() as conn:
        if fecha:
            cur = conn.execute(
                "SELECT c.*, p.nombre AS paciente_nombre"
                " FROM citas c JOIN pacientes p ON p.id = c.paciente_id"
                " WHERE c.fecha = ? ORDER BY c.hora",
                (fecha,),
            )
        else:
            cur = conn.execute(
                "SELECT c.*, p.nombre AS paciente_nombre"
                " FROM citas c JOIN pacientes p ON p.id = c.paciente_id"
                " ORDER BY c.fecha, c.hora"
            )
        return cur.fetchall()


def guardar_cita(paciente_id, fecha, hora, motivo):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO citas (paciente_id, fecha, hora, motivo)"
            " VALUES (?, ?, ?, ?)",
            (paciente_id, fecha, hora, motivo),
        )
        return cur.lastrowid


def actualizar_cita(cid, paciente_id, hora, motivo):
    with get_conn() as conn:
        conn.execute(
            "UPDATE citas SET paciente_id=?, hora=?, motivo=? WHERE id=?",
            (paciente_id, hora, motivo, cid),
        )


def borrar_cita(cid):
    with get_conn() as conn:
        conn.execute("DELETE FROM citas WHERE id=?", (cid,))


def hora_ocupada(fecha, hora, excluir_id=None):
    with get_conn() as conn:
        if excluir_id:
            cur = conn.execute(
                "SELECT id FROM citas WHERE fecha=? AND hora=? AND id!=?",
                (fecha, hora, excluir_id),
            )
        else:
            cur = conn.execute(
                "SELECT id FROM citas WHERE fecha=? AND hora=?", (fecha, hora)
            )
        return cur.fetchone() is not None


COLUMNAS_HISTORIA_OD = [
    "fecha", "ocupacion", "estado_civil", "fecha_nacimiento",
    "acudiente_apellido1", "acudiente_apellido2", "acudiente_nombre",
    "acudiente_direccion", "acudiente_telefono", "acudiente_parentesco",
    "antecedentes_personales", "antecedentes_familiares", "motivo_consulta",
    "cepillado", "seda", "enjuague",
]


def listar_historias_od(paciente_id):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, fecha, motivo_consulta FROM historia_odontologica"
            " WHERE paciente_id=? ORDER BY fecha DESC",
            (paciente_id,),
        )
        return cur.fetchall()


def get_historia_od(hid):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT * FROM historia_odontologica WHERE id=?", (hid,)
        )
        fila = cur.fetchone()
        if not fila:
            return None
        datos = dict(fila)
        for clave in ("examen_oral", "odontograma"):
            datos[clave] = json.loads(datos[clave] or "{}")
        return datos


def guardar_historia_od(paciente_id, datos):
    valores = [datos.get(c, "") for c in COLUMNAS_HISTORIA_OD]
    extras = (
        json.dumps(datos.get("examen_oral") or {}),
        json.dumps(datos.get("odontograma") or {}),
        datos.get("diagnostico_tejido_blando", ""),
        datos.get("diagnostico_dental", ""),
        datos.get("diagnostico_periodontal", ""),
        datos.get("diagnostico_craneofacial", ""),
        datos.get("diagnostico_oclusion", ""),
    )
    columnas = COLUMNAS_HISTORIA_OD + [
        "examen_oral", "odontograma", "diagnostico_tejido_blando",
        "diagnostico_dental", "diagnostico_periodontal",
        "diagnostico_craneofacial", "diagnostico_oclusion",
    ]
    with get_conn() as conn:
        cur = conn.execute(
            f"INSERT INTO historia_odontologica (paciente_id, {', '.join(columnas)})"
            f" VALUES (?, {', '.join('?' * len(columnas))})",
            (paciente_id, *valores, *extras),
        )
        return cur.lastrowid


def actualizar_historia_od(hid, datos):
    valores = [datos.get(c, "") for c in COLUMNAS_HISTORIA_OD]
    extras = (
        json.dumps(datos.get("examen_oral") or {}),
        json.dumps(datos.get("odontograma") or {}),
        datos.get("diagnostico_tejido_blando", ""),
        datos.get("diagnostico_dental", ""),
        datos.get("diagnostico_periodontal", ""),
        datos.get("diagnostico_craneofacial", ""),
        datos.get("diagnostico_oclusion", ""),
    )
    columnas = COLUMNAS_HISTORIA_OD + [
        "examen_oral", "odontograma", "diagnostico_tejido_blando",
        "diagnostico_dental", "diagnostico_periodontal",
        "diagnostico_craneofacial", "diagnostico_oclusion",
    ]
    asignacion = ", ".join(f"{c}=?" for c in columnas)
    with get_conn() as conn:
        conn.execute(
            f"UPDATE historia_odontologica SET {asignacion} WHERE id=?",
            (*valores, *extras, hid),
        )


def borrar_historia_od(hid):
    with get_conn() as conn:
        conn.execute("DELETE FROM historia_odontologica WHERE id=?", (hid,))


COLUMNAS_HISTORIA_URGENCIA = [
    "fecha", "nombre", "identificacion", "edad", "direccion", "telefono",
    "acudiente", "motivo_consulta",
    "ant_quirurgicos", "ant_patologicos", "ant_toxicoalergicos",
    "ant_transfusionales", "ant_traumaticos", "ant_otros",
    "antecedentes_familiares", "examen_fisico", "examen_radiologico",
    "impresion_diagnostica", "plan_tratamiento",
    "firma_paciente", "cc_paciente", "firma_odontologo", "cc_odontologo",
]


def listar_historias_urgencia(paciente_id):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, fecha, motivo_consulta FROM historia_urgencia"
            " WHERE paciente_id=? ORDER BY fecha DESC",
            (paciente_id,),
        )
        return cur.fetchall()


def get_historia_urgencia(hid):
    with get_conn() as conn:
        cur = conn.execute("SELECT * FROM historia_urgencia WHERE id=?", (hid,))
        fila = cur.fetchone()
        return dict(fila) if fila else None


def guardar_historia_urgencia(paciente_id, datos):
    columnas = COLUMNAS_HISTORIA_URGENCIA
    valores = [datos.get(c, "") for c in columnas]
    with get_conn() as conn:
        cur = conn.execute(
            f"INSERT INTO historia_urgencia (paciente_id, {', '.join(columnas)})"
            f" VALUES (?, {', '.join('?' * len(columnas))})",
            (paciente_id, *valores),
        )
        return cur.lastrowid


def actualizar_historia_urgencia(hid, datos):
    columnas = COLUMNAS_HISTORIA_URGENCIA
    valores = [datos.get(c, "") for c in columnas]
    asignacion = ", ".join(f"{c}=?" for c in columnas)
    with get_conn() as conn:
        conn.execute(
            f"UPDATE historia_urgencia SET {asignacion} WHERE id=?",
            (*valores, hid),
        )


def borrar_historia_urgencia(hid):
    with get_conn() as conn:
        conn.execute("DELETE FROM historia_urgencia WHERE id=?", (hid,))


COLUMNAS_EVOLUCION = ["fecha", "detalle", "firma_paciente", "firma_profesional"]


def listar_evolucion(paciente_id):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, fecha, detalle AS motivo_consulta FROM evolucion"
            " WHERE paciente_id=? ORDER BY fecha DESC",
            (paciente_id,),
        )
        return cur.fetchall()


def get_evolucion(eid):
    with get_conn() as conn:
        cur = conn.execute("SELECT * FROM evolucion WHERE id=?", (eid,))
        fila = cur.fetchone()
        return dict(fila) if fila else None


def guardar_evolucion(paciente_id, datos):
    columnas = COLUMNAS_EVOLUCION
    valores = [datos.get(c, "") for c in columnas]
    with get_conn() as conn:
        cur = conn.execute(
            f"INSERT INTO evolucion (paciente_id, {', '.join(columnas)})"
            f" VALUES (?, {', '.join('?' * len(columnas))})",
            (paciente_id, *valores),
        )
        return cur.lastrowid


def actualizar_evolucion(eid, datos):
    columnas = COLUMNAS_EVOLUCION
    valores = [datos.get(c, "") for c in columnas]
    asignacion = ", ".join(f"{c}=?" for c in columnas)
    with get_conn() as conn:
        conn.execute(
            f"UPDATE evolucion SET {asignacion} WHERE id=?",
            (*valores, eid),
        )


def borrar_evolucion(eid):
    with get_conn() as conn:
        conn.execute("DELETE FROM evolucion WHERE id=?", (eid,))


COLUMNAS_CARTA = [
    "fecha", "nombre", "apellidos", "edad", "num_documento", "tipo_documento",
    "entidad_solicitante", "motivo_consulta", "caries", "obturados",
    "plan_tratamiento", "firma",
]


def listar_carta(paciente_id):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, fecha, motivo_consulta FROM carta_dental"
            " WHERE paciente_id=? ORDER BY fecha DESC",
            (paciente_id,),
        )
        return cur.fetchall()


def get_carta(cid):
    with get_conn() as conn:
        cur = conn.execute("SELECT * FROM carta_dental WHERE id=?", (cid,))
        fila = cur.fetchone()
        if not fila:
            return None
        datos = dict(fila)
        for clave in ("examen", "odontograma"):
            datos[clave] = json.loads(datos[clave] or "{}")
        return datos


def guardar_carta(paciente_id, datos):
    columnas = COLUMNAS_CARTA + ["examen", "odontograma"]
    valores = [datos.get(c, "") for c in COLUMNAS_CARTA]
    extras = (json.dumps(datos.get("examen") or {}),
              json.dumps(datos.get("odontograma") or {}))
    with get_conn() as conn:
        cur = conn.execute(
            f"INSERT INTO carta_dental (paciente_id, {', '.join(columnas)})"
            f" VALUES (?, {', '.join('?' * len(columnas))})",
            (paciente_id, *valores, *extras),
        )
        return cur.lastrowid


def actualizar_carta(cid, datos):
    columnas = COLUMNAS_CARTA + ["examen", "odontograma"]
    valores = [datos.get(c, "") for c in COLUMNAS_CARTA]
    extras = (json.dumps(datos.get("examen") or {}),
              json.dumps(datos.get("odontograma") or {}))
    asignacion = ", ".join(f"{c}=?" for c in columnas)
    with get_conn() as conn:
        conn.execute(
            f"UPDATE carta_dental SET {asignacion} WHERE id=?",
            (*valores, *extras, cid),
        )


def borrar_carta(cid):
    with get_conn() as conn:
        conn.execute("DELETE FROM carta_dental WHERE id=?", (cid,))


COLUMNAS_ENDODONCIA = [
    "fecha", "nombre", "identificacion", "edad", "direccion", "telefono",
    "referido_por", "eps", "motivo_consulta", "pa", "fr", "fc",
    "observaciones", "antecedentes_familiares", "diente_tratar",
    "diagnostico", "pronostico", "plan_tratamiento",
    "observaciones_finales", "firma_paciente", "firma_endodoncista",
]
JSON_ENDODONCIA = ["antecedentes", "examen_clinico", "examen_radiografico",
                   "dolor", "conductos"]


def listar_historias_endodoncia(paciente_id):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, fecha, motivo_consulta FROM historia_endodoncia"
            " WHERE paciente_id=? ORDER BY fecha DESC",
            (paciente_id,),
        )
        return cur.fetchall()


def get_historia_endodoncia(hid):
    with get_conn() as conn:
        cur = conn.execute("SELECT * FROM historia_endodoncia WHERE id=?", (hid,))
        fila = cur.fetchone()
        if not fila:
            return None
        datos = dict(fila)
        for clave in JSON_ENDODONCIA:
            datos[clave] = json.loads(datos[clave] or "{}")
        return datos


def guardar_historia_endodoncia(paciente_id, datos):
    columnas = COLUMNAS_ENDODONCIA + JSON_ENDODONCIA
    valores = [datos.get(c, "") for c in COLUMNAS_ENDODONCIA]
    extras = [json.dumps(datos.get(c) or {}) for c in JSON_ENDODONCIA]
    with get_conn() as conn:
        cur = conn.execute(
            f"INSERT INTO historia_endodoncia (paciente_id, {', '.join(columnas)})"
            f" VALUES (?, {', '.join('?' * len(columnas))})",
            (paciente_id, *valores, *extras),
        )
        return cur.lastrowid


def actualizar_historia_endodoncia(hid, datos):
    columnas = COLUMNAS_ENDODONCIA + JSON_ENDODONCIA
    valores = [datos.get(c, "") for c in COLUMNAS_ENDODONCIA]
    extras = [json.dumps(datos.get(c) or {}) for c in JSON_ENDODONCIA]
    asignacion = ", ".join(f"{c}=?" for c in columnas)
    with get_conn() as conn:
        conn.execute(
            f"UPDATE historia_endodoncia SET {asignacion} WHERE id=?",
            (*valores, *extras, hid),
        )


def borrar_historia_endodoncia(hid):
    with get_conn() as conn:
        conn.execute("DELETE FROM historia_endodoncia WHERE id=?", (hid,))