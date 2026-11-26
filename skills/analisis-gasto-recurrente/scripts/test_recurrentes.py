import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recurrentes.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

import csv, tempfile
from datetime import date, timedelta

class T(unittest.TestCase):
    def _csv(self, filas):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="", encoding="utf-8")
        w = csv.writer(f); w.writerow(["fecha", "monto", "comercio"]); w.writerows(filas); f.close()
        self.addCleanup(os.unlink, f.name)
        return f.name

    def test_normalizar(self):
        self.assertEqual(m.normalizar("STREAMCO *123 / CL"), "streamco cl")

    def test_detecta_suscripcion_y_hormiga(self):
        filas = [("2026-%02d-05" % mes, 12000, "STREAMCO %d" % mes) for mes in (7, 8, 9, 10)]
        d0 = date(2026, 7, 1)
        filas += [((d0 + timedelta(days=3 * k)).isoformat(), 3000, "Cafe Central") for k in range(40)]
        r = m.analizar(m.leer(self._csv(filas)))
        self.assertEqual([x["comercio"] for x in r["recurrentes"]], ["streamco"])
        self.assertEqual(r["recurrentes"][0]["gasto_anual"], 12000 * 12)
        self.assertEqual([x["comercio"] for x in r["hormiga"]], ["cafe central"])

    def test_variacion_de_monto_no_es_recurrente(self):
        filas = [("2026-%02d-10" % mes, v, "Luz") for mes, v in zip((7, 8, 9, 10), (20000, 45000, 12000, 60000))]
        r = m.analizar(m.leer(self._csv(filas)))
        self.assertEqual(r["recurrentes"], [])

    def test_sin_datos(self):
        with self.assertRaises(ValueError):
            m.analizar([])

if __name__ == "__main__":
    unittest.main()
