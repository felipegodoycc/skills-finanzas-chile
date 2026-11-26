-- Plantilla: rol de SOLO LECTURA para que una IA/agente consulte tus finanzas en PostgreSQL.
-- Ejecútala tú, como administrador, y adapta los nombres. NO la ejecuta ninguna skill.
-- Fuentes: documentación de PostgreSQL (GRANT, ALTER DEFAULT PRIVILEGES, vistas, RLS) y
-- OWASP Top 10 LLM 2025 (LLM02 divulgación de información sensible, LLM06 agencia excesiva).
-- Principio: la seguridad la da el ROL de la base, no el "modo solo lectura" de la herramienta
-- (el servidor MCP de Postgres de referencia envolvía las consultas en BEGIN READ ONLY y fue
-- evadido con "COMMIT; DROP SCHEMA ..."; Datadog Security Labs, 21-08-2025).

-- 1) Rol sin privilegios especiales. Contraseña: genérala con tu gestor y guárdala en un secreto,
--    nunca en el prompt, en el repo ni en el chat.
CREATE ROLE asesor_ro LOGIN PASSWORD 'CAMBIAR_POR_SECRETO_LARGO'
  NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;

-- 2) Defensa extra (no es la barrera principal): transacciones de solo lectura y tiempo máximo.
ALTER ROLE asesor_ro SET default_transaction_read_only = on;
ALTER ROLE asesor_ro SET statement_timeout = '10s';
ALTER ROLE asesor_ro CONNECTION LIMIT 3;

-- 3) Nada por defecto: PUBLIC no debe poder crear objetos ni leer tus tablas base.
REVOKE ALL ON SCHEMA public FROM asesor_ro;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM asesor_ro;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

-- 4) Esquema aparte con VISTAS que exponen solo lo necesario y ya enmascarado.
--    (Ajusta columnas a tu modelo; esta vista usa el formato genérico de movimientos.)
CREATE SCHEMA IF NOT EXISTS asesor;

CREATE OR REPLACE VIEW asesor.movimientos AS
SELECT id, fecha, monto, tipo, producto, fuente,
       left(comercio, 60) AS comercio   -- sin contraparte, RUT, correo ni n.º de cuenta
FROM public.movimientos                   -- <- tu tabla real
WHERE fecha >= now() - interval '24 months';

GRANT USAGE ON SCHEMA asesor TO asesor_ro;
GRANT SELECT ON asesor.movimientos TO asesor_ro;   -- lista explícita; sin ALL TABLES
-- ALTER DEFAULT PRIVILEGES solo si quieres que vistas FUTURAS sean legibles; por defecto NO lo hagas.

-- 5) Comprobaciones (deben fallar / devolver lo esperado):
--    SET ROLE asesor_ro;  SELECT * FROM public.movimientos;  -- ERROR permission denied
--    DELETE FROM asesor.movimientos;                          -- ERROR (sin privilegio)
--    SELECT pg_read_file('/etc/passwd');                      -- ERROR (sin pg_read_server_files)
--    SELECT count(*) FROM asesor.movimientos;                 -- OK
-- Verifica además: SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname='asesor_ro'; -- ambos f
-- Si tu base guarda datos de varias personas, usa además ROW LEVEL SECURITY por usuario.
