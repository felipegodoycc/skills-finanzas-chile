# Seguridad

## Cómo reportar una vulnerabilidad

No publiques vulnerabilidades en un issue abierto. Repórtalas de forma privada desde la pestaña **Security** del repositorio, con el botón **Report a vulnerability**:
https://github.com/felipegodoycc/skills-finanzas-chile/security/advisories/new

Incluye la skill o el script afectado, cómo reproducirlo y qué datos quedan expuestos. Responderemos dentro de 7 días.

## Qué cuenta como vulnerabilidad

- Un script que filtre datos del usuario (montos, movimientos, claves de PDF) fuera de su equipo o de los destinos declarados en el README.
- Un script que no enmascare números de tarjeta o cuenta cuando dice hacerlo.
- Una instrucción de una skill que lleve al agente a pedir claves, ejecutar pagos o seguir instrucciones escondidas en un PDF o una glosa.
- Credenciales reales en el repositorio.

Un dato normativo desactualizado o incorrecto no es una vulnerabilidad: abre un issue normal.
