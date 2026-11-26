import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comparar.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

from datetime import date

def cuota(monto, i, n):
    return monto * i / (1 - (1 + i) ** -n)

class T(unittest.TestCase):
    def test_tasa_periodica(self):
        self.assertAlmostEqual(m.tasa_periodica(1_000_000, cuota(1_000_000, 0.02, 12), 12), 0.02, places=6)

    def test_dias_habiles(self):
        self.assertEqual(m.dias_habiles(date(2026, 11, 23), date(2026, 11, 26)), 3)
        self.assertEqual(m.dias_habiles(date(2026, 11, 20), date(2026, 11, 23)), 1)  # fin de semana no cuenta

    def test_orden_por_ctc_y_diferencia(self):
        a = {"entidad": "A", "monto": 1_000_000, "n": 12, "cuota": round(cuota(1_000_000, 0.03, 12)), "fecha_emision": "2026-11-25"}
        b = {"entidad": "B", "monto": 1_000_000, "n": 12, "cuota": round(cuota(1_000_000, 0.02, 12)), "fecha_emision": "2026-11-25"}
        r = m.comparar([a, b], date(2026, 11, 26))
        self.assertTrue(r["comparables"])
        self.assertEqual(r["filas"][0]["entidad"], "B")
        self.assertEqual(r["menor_ctc_bajo_estos_datos"], "B")
        self.assertGreater(r["diferencia_ctc_mayor_menor"], 0)

    def test_no_comparables_si_plazo_distinto(self):
        a = {"entidad": "A", "monto": 1_000_000, "n": 12, "cuota": 95_000, "fecha_emision": "2026-11-25"}
        b = {"entidad": "B", "monto": 1_000_000, "n": 24, "cuota": 50_000, "fecha_emision": "2026-11-25"}
        r = m.comparar([a, b], date(2026, 11, 26))
        self.assertFalse(r["comparables"])
        self.assertIn("advertencia", r)

    def test_alertas_vencida_cae_y_tmc(self):
        a = {"entidad": "A", "monto": 1_000_000, "n": 12, "cuota": 95_000, "fecha_emision": "2026-11-02", "cae_informada": 0.10}
        b = {"entidad": "B", "monto": 1_000_000, "n": 12, "cuota": 120_000, "fecha_emision": "2026-11-25"}
        r = m.comparar([a, b], date(2026, 11, 26), tmc=0.30)
        txt = " ".join(" ".join(f["alertas"]) for f in r["filas"])
        self.assertIn("vencida", txt)
        self.assertIn("difiere", txt)
        self.assertIn("TMC", txt)

    def test_gastos_aparte_suben_ctc(self):
        base = {"entidad": "A", "monto": 1_000_000, "n": 12, "cuota": 95_000, "fecha_emision": "2026-11-25"}
        con = dict(base, entidad="B", gastos_aparte=30_000)
        r = m.comparar([base, con], date(2026, 11, 26))
        ctc = {f["entidad"]: f["ctc"] for f in r["filas"]}
        self.assertEqual(ctc["B"] - ctc["A"], 30_000)

if __name__ == "__main__":
    unittest.main()
