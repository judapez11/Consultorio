import sqlite3
import unicodedata
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