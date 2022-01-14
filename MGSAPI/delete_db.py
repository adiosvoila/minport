import sqlite3, datetime

with sqlite3.connect("/home/MGSAPI/app/main/flask_boilerplate_prod.db") as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("DELETE from MGS_LEASE")
        cur.execute("DELETE from MGS_NODE")
        conn.commit()
        cur.close()

