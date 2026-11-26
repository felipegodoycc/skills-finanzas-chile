import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagnostico.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

D = {"ingreso_liquido": 1_000_000, "gastos": {"a": 700_000},
     "deudas": [{"nombre": "c", "saldo": 2_000_000, "cuota": 400_000, "tasa_mensual": 0.02}],
     "objetivos": ["salir de la rotativa", "comprar un computador"], "liquidez": 100_000}

class T(unittest.TestCase):
    def test_flujo_negativo(self):
        r = m.diagnosticar(D)
        self.assertEqual(r["flujo_mensual"], -100_000)
        self.assertEqual(r["tipo_de_problema"], "flujo_negativo")
        self.assertIn("presupuesto-personal", r["skills_en_orden"])
        self.assertIn("plan-refinanciamiento", r["skills_en_orden"])
        self.assertEqual(r["rci"], 0.4)

    def test_flujo_positivo(self):
        d = dict(D, gastos={"a": 300_000})
        r = m.diagnosticar(d)
        self.assertEqual(r["tipo_de_problema"], "flujo_positivo")
        self.assertNotIn("presupuesto-personal", r["skills_en_orden"])

    def test_pregunta_objetivos_si_faltan_y_aviso(self):
        r = m.diagnosticar({"ingreso_liquido": 1_000_000, "gastos": {}, "deudas": []})
        self.assertTrue(any("objetivo" in p for p in r["preguntas_pendientes"]))
        self.assertIn("IA", r["aviso"])

    def test_ingreso_invalido(self):
        with self.assertRaises(ValueError):
            m.diagnosticar({"ingreso_liquido": 0})

if __name__ == "__main__":
    unittest.main()
