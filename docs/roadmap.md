# Roadmap – Second Brain (Finanzas)

## Visión
Aplicación privada para gestionar finanzas personales y compartidas en pareja,
con separación clara entre gastos individuales y conjuntos, y preparada para escalar.

---

## Alcance inicial
- Web primero
- Registro manual de ingresos y gastos
- Uso privado (2 usuarios)
- Escalable a futuro

---

## Fase 0 – Fundaciones
**Objetivo:** base técnica sólida

- Git y documentación
- Backend y frontend separados
- Docker y Docker Compose
- PostgreSQL
- Variables de entorno

---

## Fase 1 – Usuarios y Parejas
**Objetivo:** dos usuarios, una pareja

- Registro y login
- Autenticación JWT
- Crear pareja
- Invitar / unir pareja
- Roles (owner / member)

---

## Fase 2 – Ingresos y Gastos
**Objetivo:** núcleo del sistema

- Ingresos personales
- Gastos personales
- Ingresos compartidos
- Gastos compartidos
- CRUD de transacciones

---

## Fase 3 – Categorías y Presupuestos
**Objetivo:** entender en qué se va el dinero

- Categorías personales
- Categorías compartidas
- Presupuestos mensuales
- Alertas visuales

---

## Fase 4 – Dashboards
**Objetivo:** visibilidad clara

- Totales personales
- Totales compartidos
- Comparativo entre usuarios
- Gastos por categoría

---

## Fase 5 – Importación CSV / Excel
**Objetivo:** carga masiva

- Subida de archivos
- Mapeo de columnas
- Preview antes de guardar

---

## Fase 6 – Seguridad y Calidad
- Logs
- Backups
- Rate limiting
- Tests básicos

---

## Fase 7 – Deploy
- Ubuntu Server
- AWS Free Tier
- HTTPS
- CI/CD simple

---

## Fase 8 – Mobile
- Flutter o React Native
- Reutilización total del backend