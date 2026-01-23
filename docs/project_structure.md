# Project Structure v0.1

> Documento vivo que describe la estructura del proyecto y las decisiones detrás de ella.

---

## Estructura general del repositorio

```
second_brain/
│
├─ docs/
│  ├─ roadmap.md
│  ├─ project_structure.md
│  └─ decisions.md
│
├─ backend/
│  ├─ README.md
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py
│  │  │
│  │  ├─ controllers/
│  │  │  └─ health_controller.py
│  │  │
│  │  ├─ services/
│  │  │  └─ __init__.py
│  │  │
│  │  ├─ models/
│  │  │  └─ __init__.py
│  │  │
│  │  └─ repositories/
│  │     └─ __init__.py
│  │
│  └─ requirements.txt
│
├─ frontend/
│  ├─ README.md
│  └─ web/
│     ├─ index.html
│     ├─ css/
│     └─ js/
│
├─ .gitignore
└─ README.md
```

---

## Principios de diseño

- **Primero Web**, luego app móvil
- **Manual input primero**, luego masivo CSV/Excel
- **Uso personal**, luego escalable
- **Separación clara frontend / backend**
- **MVC ligero (pragmático)**

---

## Backend – MVC ligero

### Controllers
Responsables de:
- Recibir requests HTTP
- Validar inputs básicos
- Orquestar servicios
- Retornar responses

### Services
- Lógica de negocio
- Reglas de cálculo
- Agregaciones

### Models
- Entidades del dominio
- Representan conceptos del negocio

### Repositories
- Acceso a datos
- Inicialmente: memoria / CSV
- Luego: base de datos

---

## Frontend

### Fase 1
- HTML + JS
- Fetch API
- Sin framework

### Fase futura
- React / Vue
- Reutiliza backend sin cambios

---

## Evolución esperada

- v0.1 → estructura base
- v0.2 → modelos de datos
- v0.3 → auth básica
- v0.4 → gastos compartidos
- v1.0 → importación masiva + mobile

---

> Este documento debe actualizarse cuando la estructura cambie.