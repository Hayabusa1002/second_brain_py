# Reglas de Negocio del Dominio

Este documento define las **reglas e invariantes del dominio** del proyecto *Second Brain*.
Estas reglas deben cumplirse siempre, independientemente de la interfaz, API o tecnología utilizada.

---

## Principios

* Las reglas viven en el dominio, no en la UI
* Deben ser explícitas y verificables
* No dependen de la base de datos
* Cualquier violación es un error del sistema

---

## Reglas sobre Usuario

1. Un usuario con `estado` distinto de `activo` no puede autenticarse.
2. Un usuario `baneado` no puede realizar ninguna acción dentro del sistema.
3. Un usuario `inactivo` no puede crear ni modificar información.
4. El cambio de estado de un usuario debe quedar registrado (auditable en el futuro).

---

## Reglas sobre Cuenta

5. Toda cuenta debe tener al menos un propietario.
6. Las cuentas de tipo `individual` deben tener exactamente un propietario.
7. Las cuentas de tipo `compartida` deben tener dos o más propietarios.
8. Solo los propietarios de una cuenta pueden visualizarla.
9. Solo los propietarios de una cuenta pueden registrar transacciones en ella.

---

## Reglas sobre Categoría

10. Toda categoría debe tener un tipo (`ingreso` o `gasto`).
11. El tipo de la categoría debe ser consistente con el tipo de la transacción.
12. Las categorías no pueden eliminarse si existen transacciones asociadas.

---

## Reglas sobre Transacción

13. Toda transacción debe pertenecer a una cuenta válida.
14. Toda transacción debe tener una categoría válida.
15. El monto de una transacción debe ser siempre positivo.
16. El signo del movimiento se deriva del tipo de transacción y no se almacena.
17. El usuario que crea una transacción debe ser propietario de la cuenta.
18. No se permite modificar el tipo de una transacción una vez creada.

---

## Reglas de Acceso y Visibilidad

19. Un usuario solo puede acceder a información de cuentas donde sea propietario.
20. En cuentas compartidas, todos los propietarios tienen el mismo nivel de acceso.
21. Las acciones deben validarse tanto por estado del usuario como por pertenencia a la cuenta.

---

## Evolución del Dominio

22. Toda nueva funcionalidad debe respetar estas reglas o extenderlas explícitamente.
23. Si una regla cambia, este documento debe actualizarse antes de implementar el cambio.

---
_
Este documento complementa a `entities.md` y `use_cases.md` y define el comportamiento obligatorio del dominio.