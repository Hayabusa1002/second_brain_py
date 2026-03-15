# Correr el Seed en Railway

## Opcion A — CLI de Railway

### 1. Instalar la CLI

```bash
npm install -g @railway/cli
```

### 2. Login y link al proyecto

```bash
railway login
railway link
```

Selecciona el proyecto `second_brain_py` cuando lo pida.

### 3. Correr el seed

```bash
railway run python -m app.db.seed
```

---

## Opcion B — Start Command temporal en el panel

- Ve a **second_brain_py -> Settings -> Deploy -> Start Command**
- Reemplaza el comando actual por:

```bash
python -m app.db.seed && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

- Haz **Redeploy** y espera que el seed corra
- Vuelve a **Start Command** y deja solo:

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

- Haz **Redeploy** nuevamente

---

## Verificar

Abre la app y confirma que las categorias y cuentas por defecto aparecen:

```html
https://secondbrain-hayabusa.up.railway.app
```
