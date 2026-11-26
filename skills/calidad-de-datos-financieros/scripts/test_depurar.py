import importlib.util, os, sys, unittest
sys.dont_write_bytecode = True
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "depurar.py")
_s = importlib.util.spec_from_file_location("m", _p)
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)

def mov(i, fecha, fuente, monto=5000, producto="A", **kw):
    return dict(id=i, fecha=fecha, monto=monto, producto=producto, fuente=fuente, tipo=kw.pop("tipo", "gasto"), **kw)

class T(unittest.TestCase):
    def test_enlace_uno_a_uno_sin_cruzar(self):
        movs = [mov(1, "2026-10-02", "tiempo_real"), mov(2, "2026-10-03", "tiempo_real"),
                mov(10, "2026-10-04", "cartola"), mov(11, "2026-10-06", "cartola")]
        pares = {(p["conservar"], p["duplicado"]) for p in m.marcar_duplicados(movs)}
        self.assertEqual(pares, {(10, 2), (11, 1)})

    def test_ventana_asimetrica(self):
        ok = [mov(1, "2026-10-10", "tiempo_real"), mov(2, "2026-10-08", "cartola")]   # rt 2 días después
        no = [mov(1, "2026-10-11", "tiempo_real"), mov(2, "2026-10-08", "cartola")]   # rt 3 días después
        self.assertEqual(len(m.marcar_duplicados(ok)), 1)
        self.assertEqual(len(m.marcar_duplicados(no)), 0)

    def test_distinto_monto_o_producto_no_enlaza(self):
        movs = [mov(1, "2026-10-02", "tiempo_real", monto=5000), mov(2, "2026-10-03", "cartola", monto=5001),
                mov(3, "2026-10-03", "cartola", producto="B")]
        self.assertEqual(m.marcar_duplicados(movs), [])

    def test_reembolso_y_verificacion(self):
        movs = [mov(1, "2026-10-05", "cartola", monto=50000, tipo="ingreso", contraparte="X"),
                mov(2, "2026-10-05", "cartola", monto=50000, tipo="ingreso", contraparte="Y")]
        c = m.netear_reembolsos(movs, {"X"})
        self.assertEqual(c, [{"id": 1, "tipo_nuevo": "gasto/devolucion", "monto_nuevo": -50000}])
        v = m.verificar_reembolso(85_000, 73_000, descuento_acordado=0)
        self.assertEqual(v["brecha"], -12_000)
        self.assertIn("estimacion", v["estado"])
        self.assertEqual(m.verificar_reembolso(80_000, 80_000)["estado"], "calza")

if __name__ == "__main__":
    unittest.main()
