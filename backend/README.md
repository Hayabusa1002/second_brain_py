# Backend

API REST para la gestión de finanzas en pareja.

## Responsabilidades
- Autenticación
- Usuarios y parejas
- Ingresos y gastos
- Categorías y presupuestos

## Stack
- FastAPI
- PostgreSQL
- Docker

## Requisitos
- Python 3.10+

## Documentación técnica inicial

### Instalación
```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Ejecutar servidor
```
uvicorn app.main:app --reload
```

### Detener servidor
```
Ctrl + C
```

### Endpoint
```
http://127.0.0.1:8000/health
```