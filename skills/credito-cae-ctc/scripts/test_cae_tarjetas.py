import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_d = os.path.dirname(os.path.abspath(__file__))
def _carga(nombre):
    s = importlib.util.spec_from_file_location(nombre, os.path.join(_d, nombre + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
t = _carga("cae_tarjetas")
c = _carga("cae")

UF = 40_000.0  # valor ficticio, solo para los tests


class T(unittest.TestCase):
    def test_sin_cargos_cae_rotativo_es_tasa_efectiva_anual(self):
        flujos = t.construir_flujo(20 * UF, 0.02)
        r = t.cae_rotativo_o_cuotas(UF, flujos)
        self.assertAlmostEqual(r["tasa_mensual"], 0.02, places=8)
        self.assertAlmostEqual(r["CAE"], 1.02 ** 12 - 1, places=8)

    def test_avance_es_nominal_i_por_12(self):
        flujos = t.construir_flujo(20 * UF, 0.02)
        r = t.cae_avance(UF, flujos)
        self.assertAlmostEqual(r["CAE"], 0.24, places=8)

    def test_cargos_suben_la_cae(self):
        sin = t.cae_rotativo_o_cuotas(UF, t.construir_flujo(20 * UF, 0.02))
        con = t.cae_rotativo_o_cuotas(UF, t.construir_flujo(20 * UF, 0.02, 3000))
        self.assertGreater(con["CAE"], sin["CAE"])

    def test_vp_de_los_flujos_iguala_el_capital(self):
        flujos = t.construir_flujo(20 * UF, 0.015, 2500)
        r = t.cae_rotativo_o_cuotas(UF, flujos)
        vp = sum(x / (1 + r["tasa_mensual"]) ** m for m, x in enumerate(flujos, 1))
        self.assertAlmostEqual(vp, 20 * UF, places=3)

    def test_m_debe_ser_12(self):
        with self.assertRaises(ValueError):
            t.cae_rotativo_o_cuotas(UF, [100_000.0] * 11)

    def test_r0_cero_equivale_a_m_1_a_12(self):
        flujos = t.construir_flujo(20 * UF, 0.02)
        a = t.cae_rotativo_o_cuotas(UF, flujos, r0=0.0)
        b = t.cae_rotativo_o_cuotas(UF, flujos)
        self.assertEqual(a["CAE"], b["CAE"])

    def test_caep_renta_vencida(self):
        cuota = 1_000_000 * 0.02 / (1 - 1.02 ** -12)
        r = t.caep(1_000_000, [cuota] * 12)
        self.assertAlmostEqual(r["tasa_periodica"], 0.02, places=8)
        self.assertAlmostEqual(r["CAEP"], 0.24, places=7)

    def test_concuerda_con_el_solver_general_de_cae_py(self):
        flujos = t.construir_flujo(20 * UF, 0.018, 1500)
        i_tarjeta = t.cae_rotativo_o_cuotas(UF, flujos)["tasa_mensual"]
        i_general = c.tasa_periodica([(0, 20 * UF)],
                                     [(m, x) for m, x in enumerate(flujos, 1)])
        self.assertAlmostEqual(i_tarjeta, i_general, places=8)

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            t.caep(0, [1.0, 2.0])


if __name__ == "__main__":
    unittest.main()
