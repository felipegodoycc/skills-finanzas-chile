import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refinanciar.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

D = [{"nombre": "A", "saldo": 1000, "tasa_mensual": 0.05, "cuota_minima": 100},
     {"nombre": "B", "saldo": 500, "tasa_mensual": 0.01, "cuota_minima": 50}]

def cuota(monto, i, n):
    return monto * i / (1 - (1 + i) ** -n)

class T(unittest.TestCase):
    def test_avalancha_no_paga_mas_intereses_que_nieve(self):
        a = m.simular_pago(D, 300, "avalancha"); n = m.simular_pago(D, 300, "nieve")
        self.assertTrue(a["completo"] and n["completo"])
        self.assertLessEqual(a["intereses_total"], n["intereses_total"])

    def test_orden_de_cierre_avalancha(self):
        # con avalancha el excedente va a A (5% mensual): A cierra antes que B
        r = m.simular_pago(D, 300, "avalancha")
        self.assertEqual(r["orden_de_cierre"][0]["nombre"], "A")

    def test_presupuesto_insuficiente(self):
        with self.assertRaises(ValueError):
            m.simular_pago(D, 100, "avalancha")

    def test_tasa_implicita_y_prepago(self):
        c = cuota(1_000_000, 0.02, 12)
        self.assertAlmostEqual(m.tasa_implicita(1_000_000, c, 12), 0.02, places=6)
        r = m.ahorro_prepago(1_000_000, c, 12)
        self.assertAlmostEqual(r["ahorro_neto"], round(c * 12 - 1_000_000), delta=1)
        con = m.ahorro_prepago(1_000_000, c, 12, comision_pct=0.01)
        self.assertEqual(r["ahorro_neto"] - con["ahorro_neto"], 10_000)

    def test_compra_cartera_plazo_mayor(self):
        deudas = [{"nombre": "x", "cuota": 100_000, "cuotas_restantes": 10},
                  {"nombre": "y", "cuota": 50_000, "cuotas_restantes": 5}]
        r = m.compra_cartera(deudas, {"monto": 1_300_000, "cuota": 120_000, "n": 12, "gastos": 30_000})
        self.assertEqual(r["pagarias_si_sigues"], 1_250_000)
        self.assertEqual(r["pagarias_con_la_oferta"], 1_470_000)
        self.assertEqual(r["diferencia_total"], -220_000)
        self.assertTrue(any("plazo nuevo es mayor" in a for a in r["alertas"]))

if __name__ == "__main__":
    unittest.main()
