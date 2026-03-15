# Deploy en Railway

## 1. Preparar el Dockerfile

Ajusta el `CMD` para usar el puerto dinámico que Railway asigna:

```dockerfile
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

## 2. Crear el proyecto en Railway

1. Entra a [railway.app](https://railway.app) y crea una cuenta
2. **New Project → Deploy from GitHub repo**
3. Conecta tu cuenta de GitHub y selecciona `second_brain_py`
4. Railway detecta el `Dockerfile` y empieza a buildear el servicio `app`

## 3. Agregar PostgreSQL

1. En el mismo proyecto, click en **+ New Service → Database → PostgreSQL**
2. Railway genera automáticamente la variable `DATABASE_URL`
3. En el servicio `app`, ve a **Variables** y agrega:

```text
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

## 4. Variables de entorno

Agrega el resto de variables de tu `.env` en la pestana **Variables** del servicio `app`:

```text
SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 5. Ejecutar el seed

Opcion A — desde la terminal de Railway:

```bash
railway run python -m app.db.seed
```

Opcion B — como parte del Start Command en **Service → Settings → Deploy**:

```bash
python -m app.db.seed && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```
