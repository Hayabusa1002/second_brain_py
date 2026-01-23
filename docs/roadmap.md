# Roadmap – Second Brain (Finanzas)

Roadmap vivo, incremental y pragmático.
Cada versión debe dejar el proyecto usable, aunque sea mínimo.

---

## Objetivo del proyecto

Crear una aplicación para gestionar finanzas compartidas en pareja que permita:

* Ver ingresos y gastos individuales y conjuntos
* Clasificar movimientos por categorías
* Mantener control simple, claro y privado
* Escalar gradualmente (web → mobile, manual → masivo)

---

## v0.1 – Base técnica y conceptual (MVP técnico)

Objetivo: Tener la base del proyecto lista y funcional a nivel técnico.

Alcance:

* Proyecto inicializado
* Estructura definida
* API levantando
* Documentación base

Tareas:

* [x] Inicializar repositorio Git
* [x] Definir estructura del proyecto
* [x] Crear .gitignore
* [x] Crear README.md general
* [ ] Backend con FastAPI funcionando
* [ ] Endpoint /health
* [ ] Documentación técnica inicial

---

## v0.2 – Modelo de datos y dominio

Objetivo: Definir claramente el negocio antes de construir UI.

Alcance:

* Entidades claras
* Relaciones definidas
* Datos aún en memoria

Tareas:

* [ ] Definir entidades principales

  * Usuario
  * Cuenta
  * Transacción
  * Categoría
* [ ] Definir qué es compartido vs individual
* [ ] Documentar reglas de negocio
* [ ] Crear modelos en backend

---

## v0.3 – Backend funcional mínimo

Objetivo: Poder registrar y consultar movimientos vía API.

Alcance:

* CRUD básico
* Persistencia simple (memoria / JSON)

Tareas:

* [ ] Crear endpoints de transacciones
* [ ] Crear endpoints de categorías
* [ ] Servicio de cálculo de balances
* [ ] Separación controller / service / repository

---

## v0.4 – Frontend web básico

Objetivo: Usar el sistema sin tocar herramientas externas.

Alcance:

* UI simple
* Sin autenticación todavía

Tareas:

* [ ] Página de listado de gastos
* [ ] Formulario de ingreso manual
* [ ] Filtros por categoría
* [ ] Vista individual vs compartida

---

## v0.5 – Importación masiva

Objetivo: Cargar datos históricos fácilmente.

Alcance:

* CSV / Excel

Tareas:

* [ ] Definir formato de archivo
* [ ] Endpoint de importación
* [ ] Validación de datos
* [ ] Feedback de errores

---

## v0.6 – Usuarios y privacidad

Objetivo: Control de acceso básico.

Alcance:

* Login simple
* Sesiones locales

Tareas:

* [ ] Autenticación básica
* [ ] Asociación de datos por usuario

---

## v1.0 – Escalabilidad

Objetivo: Proyecto usable a largo plazo.

Alcance:

* Mobile-ready
* Backend estable

Ideas futuras:

* App móvil
* Deploy en cloud
* Backups automáticos

---

Regla del roadmap: no avanzar de versión sin que la anterior sea estable.