# Deploy en VPS Ubuntu (Oracle Cloud)

## 1. Conectarte al servidor

```bash
ssh ubuntu@<IP_DEL_SERVIDOR>
```

## 2. Instalar Docker y Git

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose git
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
```

## 3. Clonar el repo

```bash
git clone https://github.com/Hayabusa1002/second_brain_py.git
cd second_brain_py
```

## 4. Crear el .env

```bash
nano backend/.env
```

Pega tus variables:

```env
DATABASE_URL=postgresql://postgres:password@db:5432/second_brain
SECRET_KEY=<tu_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=7
APP_ENV=production
DEBUG=False
```

## 5. Levantar con Docker Compose

```bash
docker compose up -d --build
```

A diferencia de Railway, en el VPS se usa el `docker-compose.yml` completo y levanta `app` + `db` juntos.

## 6. Abrir el puerto en Oracle Cloud

Oracle Cloud bloquea los puertos por defecto. Debes abrir el puerto `8000` en dos lugares:

- **Security List** del VPS en la consola de Oracle -> agregar Ingress Rule para el puerto `8000`
- En el servidor mismo:

```bash
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
```

Tu app queda accesible en `http://<IP_DEL_SERVIDOR>:8000`.

## 7. (Opcional) Dominio + HTTPS

Si quieres un dominio con HTTPS en vez de la IP, agrega **Nginx** como proxy inverso y **Certbot** para el certificado SSL.

Instalar Nginx y Certbot:

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

Configurar Nginx como proxy inverso en `/etc/nginx/sites-available/second_brain`:

```nginx
server {
    listen 80;
    server_name <tu_dominio.com>;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Activar y obtener certificado SSL:

```bash
sudo ln -s /etc/nginx/sites-available/second_brain /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d <tu_dominio.com>
```
