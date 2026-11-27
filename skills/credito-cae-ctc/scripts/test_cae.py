import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_d = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("cae", os.path.join(_d, "cae.py"))
c = importlib.util.module_from_spec(_s); _s.loader.exec_module(c)


def cuota_francesa(p, i, n):
    """Fórmula de anualidad, independiente del solver del script."""
    return p * i / (1 - (1 + i) ** -n)


class Pruebas(unittest.TestCase):
    def test_cae_recupera_la_tasa_de_una_cuota_francesa(self):
        cuota = cuota_francesa(1_000_000, 0.02, 12)
        r = c.cae_credito(1_000_000, cuota, 12)
        self.assertAlmostEqual(r["tasa_periodica"], 0.02, places=8)
        self.assertAlmostEqual(r["CAE_nominal_i_por_f"], 0.24, places=7)
        self.assertAlmostEqual(r["tasa_efectiva_anual"], 1.02 ** 12 - 1, places=7)
        self.assertAlmostEqual(r["CTC"], cuota * 12)
        self.assertAlmostEqual(r["costo_total_sobre_neto"], cuota * 12 - 1_000_000)

    def test_pago_inicial_sube_la_tasa_y_el_ctc(self):
        cuota = cuota_francesa(1_000_000, 0.02, 12)
        sin = c.cae_credito(1_000_000, cuota, 12)
        con = c.cae_credito(1_000_000, cuota, 12, pago_inicial=30_000)
        self.assertGreater(con["tasa_periodica"], sin["tasa_periodica"])
        self.assertAlmostEqual(con["CTC"], sin["CTC"] + 30_000)

    def test_saldo_capital(self):
        cuota = cuota_francesa(1_000_000, 0.02, 12)
        self.assertAlmostEqual(c.saldo_capital(cuota, 12, 0, 0.02), 1_000_000, places=4)
        self.assertAlmostEqual(c.saldo_capital(cuota, 12, 12, 0.02), 0.0)
        # tras 6 cuotas, el saldo es el VP de las 6 restantes
        self.assertAlmostEqual(c.saldo_capital(cuota, 12, 6, 0.02),
                               cuota_francesa(1, 0.02, 6) ** -1 * cuota, places=4)

    def test_reemplazo_tasa_ponderada_y_diferencia(self):
        cuota = cuota_francesa(1_000_000, 0.015, 24)
        r = c.reemplazo([{"nombre": "a", "saldo": 600_000, "tasa_mensual": 0.03},
                         {"nombre": "b", "saldo": 400_000, "tasa_mensual": 0.02}],
                        {"monto_neto": 1_000_000, "cuota": cuota, "n": 24})
        self.assertAlmostEqual(r["tasa_mensual_ponderada_actual"], 0.026)
        self.assertAlmostEqual(r["tasa_periodica_nuevo_credito"], 0.015, places=8)
        self.assertAlmostEqual(r["diferencia_costo_primer_mes_aprox"], 26_000 - 15_000, places=2)

    def test_errores(self):
        with self.assertRaises(ValueError):
            c.reemplazo([{"nombre": "a", "saldo": 0, "tasa_mensual": 0.03}],
                        {"monto_neto": 1, "cuota": 1, "n": 1})
        with self.assertRaises(ValueError):
            c.tasa_periodica([(0, 100)], [])


if __name__ == "__main__":
    unittest.main()
