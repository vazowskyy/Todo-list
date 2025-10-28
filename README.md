# 📝 Todo List

A simple, **containerized Todo List application** built with **Flask**, **PostgreSQL**, and **Docker**.  
The project demonstrates a clean, modular architecture for managing tasks (CRUD operations), continuous integration with **GitHub Actions**, and plans for observability using **Prometheus** and **Grafana**.

---

![alt text](https://github.com/vazowskyy/Todo-list/blob/FlaskPostgres/TodoAPP/website/static/images/carousel/todo_tasks.png?raw=true)

---

## 🚀 Project Overview

**Todo List** is a lightweight web application for managing personal tasks.  
It uses **Flask** for the backend, **PostgreSQL** for persistent storage, and **Docker** for consistent development and production environments.

The main goal of this project is to serve as a simple, production-ready example for DevOps practices, CI/CD automation, and scalable application design.

---

## 🧰 Tech Stack
* Flask – Backend Framework
* PostgreSQL – Database
* Docker & Docker Compose – Containerization
* GitHub Actions – CI/CD
* pytest – Testing

---

## ✨ Features

- ✅ Add, view, and delete tasks (**CRUD functionality**)  
- 💾 Persistent data storage with **PostgreSQL**  
- ⚙️ Configurable environment via `.env` file  
- 🐳 Ready-to-run **Dockerfile** and `docker-compose.yml`  
- 🤖 Automated tests executed via **GitHub Actions**  
- 📊 *In progress:* Monitoring and metrics with **Prometheus** and **Grafana**

---

## ⚙️ Installation (Local Setup)

Clone the repository:

```bash
git clone https://github.com/vazowskyy/Todo-list.git
cd Todo-list
```
Install dependencies (you can use a virtual environment if desired):
```bash
pip install -r requirements.txt
```
Configure environment variables:
```bash
cp .env_sample .env
vim .env
```
Run the application:
```
flask run
```

---

## 🐳 Running with Docker
Make sure you have **Docker** and **Docker Compose** installed, then run:
```bash
docker-compose up --build
```

---

## 🧪 Running Tests
Navigate to the app directory and run tests with pytest:
```bash
cd TodoAPP
pytest -v -s
```
Disclaimer: these tests run automatically with GitHub Actions -> **./github/workflows/main.yml**
