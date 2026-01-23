# Entidades del Dominio

Este documento define las entidades centrales del dominio para el proyecto *Second Brain*.  
Es la fuente de verdad sobre qué existe en el sistema y cómo se relacionan los conceptos.

---

## Principios de diseño

* Simplicidad antes que sofisticación
* Relaciones explícitas
* Sin reglas de negocio implícitas
* Backend-driven, web primero

---

## Usuario

Representa a una persona que puede acceder al sistema y operar según su rol.

**Campos:**

* `id`: Identificador único del usuario.
* `nombre`: Nombre completo.
* `email`: Correo electrónico (único).
* `password_hash`: Hash de la contraseña.
* `estado`: Estado del usuario dentro del sistema. Valores posibles: `activo`, `inactivo`, `baneado`, `suspendido`, etc.
* `rol`: Rol asignado (admin, usuario, etc.).
* `fecha_creacion`: Fecha de creación del usuario.
* `fecha_actualizacion`: Última modificación.

**Notas:**

* El campo `estado` controla el acceso y comportamiento del usuario en el sistema.
* Un usuario con estado distinto de `activo` no debería poder autenticarse.
* Un usuario puede ser dueño de una o más cuentas.

---

## Cuenta

Agrupa transacciones y define si el dinero es individual o compartido.

**Campos:**

* `id`: Identificador único de la cuenta.
* `nombre`: Nombre descriptivo de la cuenta.
* `tipo`: Tipo de cuenta. Valores posibles: `individual`, `compartida`.
* `propietarios`: Lista de usuarios asociados a la cuenta.
* `fecha_creacion`: Fecha de creación de la cuenta.
* `fecha_actualizacion`: Última modificación.

**Notas:**

* Toda transacción pertenece exactamente a una cuenta.
* Las cuentas compartidas deben tener más de un propietario.
* Las cuentas individuales tienen exactamente un propietario.
* Un usuario puede ser propietario de múltiples cuentas.

---

## Categoría

Clasifica una transacción según su naturaleza.

**Campos:**

* `id`: Identificador único de la categoría.
* `nombre`: Nombre de la categoría.
* `tipo`: Tipo de categoría. Valores posibles: `ingreso`, `gasto`.
* `fecha_creacion`: Fecha de creación de la categoría.
* `fecha_actualizacion`: Última modificación.

**Notas:**

* Una transacción tiene exactamente una categoría.
* En v0.2 las categorías son globales (no específicas por usuario).
* El tipo de la categoría debe ser consistente con el tipo de la transacción.

---

## Transacción

Representa un movimiento financiero dentro de una cuenta.

**Campos:**

* `id`: Identificador único de la transacción.
* `fecha`: Fecha en la que ocurre la transacción.
* `monto`: Valor numérico siempre positivo.
* `tipo`: Tipo de transacción. Valores posibles: `ingreso`, `gasto`.
* `categoria`: Categoría asociada a la transacción.
* `cuenta`: Cuenta a la que pertenece la transacción.
* `creado_por`: Usuario que registró la transacción.
* `descripcion`: Texto opcional para mayor detalle.
* `fecha_creacion`: Fecha de creación del registro.
* `fecha_actualizacion`: Última modificación.

**Notas:**

* El signo del monto se deriva del tipo (`ingreso` o `gasto`), no se almacena.
* No pueden existir transacciones sin cuenta o categoría.
* `creado_por` indica quién registró la transacción, no necesariamente el propietario de la cuenta.

---

## Relación entre entidades

Usuario → Cuenta → Transacción → Categoría

* Los usuarios son dueños de cuentas.
* Las cuentas agrupan transacciones.
* Las transacciones se clasifican por categorías.

---

Este documento debe actualizarse antes de modificar o agregar conceptos del dominio.