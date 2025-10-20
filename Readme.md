
# Dockerized Django Project

This project demonstrates how to run a Django web application using Docker and Docker Compose with environment variables and an external PostgreSQL database.

## 🐳 Dockerfile Overview

This `Dockerfile` builds a Docker image for the Django project:

```Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 🔍 Explanation

- `FROM python:3.10-slim`: Uses a lightweight Python 3.10 base image.
- `WORKDIR /app`: Sets the working directory inside the container.
- `COPY requirements.txt .`: Copies the dependency file.
- `RUN pip install ...`: Installs required packages.
- `COPY . .`: Copies all source code to the container.
- `EXPOSE 8000`: Exposes port 8000 (Django default).
- `CMD`: Runs the Django development server.

---

## 🧩 Docker Compose File

This is the `docker-compose.yml` to run your app container with `.env` support and no PostgreSQL container (you are using an online DB):

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - .:/app
```

### 🔍 Explanation

- `build: .`: Builds the image from the local `Dockerfile`.
- `ports`: Maps container port 8000 to host port 8000.
- `env_file`: Loads your `.env` file (with DB credentials, secret keys, etc.).
- `volumes`: Mounts your code directory for hot reloading.

---

## 📦 How to Use

1. Place your `.env` file with your PostgreSQL connection info in the root directory.
2. Run the following command to build and start your Django app:

```bash
docker compose up --build
```

3. Visit `http://localhost:8000` in your browser.

---

## 🧹 Cleanup

To stop and remove containers, run:

```bash
docker compose down
```

---

## ✅ Example `.env`

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-online-postgresql-url
```

Make sure your Django settings file reads these variables using `os.getenv()`.

---

## 🧠 Notes

- This setup is for development. For production, use Gunicorn + Nginx.
- Docker Compose version key (`version:`) is no longer needed (Docker will infer it).

---

Happy coding! 🎉

