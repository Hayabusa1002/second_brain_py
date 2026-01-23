# Casos de Uso del Dominio

Este documento describe los casos de uso principales del sistema *Second Brain*.
Define **qué puede hacer el usuario** y **cómo interactúa con las entidades**, sin entrar en detalles técnicos de implementación.

---

## Principios

* Centrados en el usuario
* Independientes de la UI
* Basados en el dominio, no en la base de datos
* Evolutivos

---

## UC-01: Registro de usuario

**Actor:** Usuario

**Descripción:**
Permite a una persona crear una cuenta para acceder al sistema.

**Flujo principal:**

1. El usuario ingresa nombre, email y contraseña.
2. El sistema valida que el email no exista.
3. Se crea el usuario con estado `activo`.

**Reglas:**

* El email debe ser único.
* La contraseña se almacena como hash.

---

## UC-02: Crear cuenta

**Actor:** Usuario autenticado

**Descripción:**
Permite crear una cuenta financiera individual o compartida.

**Flujo principal:**

1. El usuario define nombre y tipo de cuenta.
2. Asigna uno o más propietarios.
3. El sistema crea la cuenta.

**Reglas:**

* Las cuentas individuales deben tener un único propietario.
* Las cuentas compartidas deben tener al menos dos propietarios.

---

## UC-03: Registrar transacción

**Actor:** Usuario autenticado

**Descripción:**
Permite registrar un ingreso o gasto en una cuenta.

**Flujo principal:**

1. El usuario selecciona cuenta y categoría.
2. Define fecha, monto y tipo.
3. El sistema registra la transacción.

**Reglas:**

* El monto debe ser positivo.
* El tipo determina el signo lógico del movimiento.

---

## UC-04: Consultar movimientos

**Actor:** Usuario autenticado

**Descripción:**
Permite visualizar transacciones propias o compartidas.

**Flujo principal:**

1. El usuario selecciona una cuenta.
2. Aplica filtros por fecha, tipo o categoría.
3. El sistema muestra el listado.

**Reglas:**

* El usuario solo puede ver cuentas donde sea propietario.

---

Este documento debe mantenerse alineado con `entities.md`.