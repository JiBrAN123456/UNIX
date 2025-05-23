# 🧠 Unix-Style Task Manager (Django REST)

A simple REST API that mimics Unix-style task management (e.g., `fork`, `ls`, `rm`) using Django and DRF.

---

## 🚀 Features

- Create (fork) tasks
- List tasks (`ls`)
- Delete tasks (`rm`)
- Simulate task execution (running → completed)
- Filter by status
- Optional JWT-based authentication
- Logging & health check endpoint

---

## ⚙️ Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/JiBrAN123456/UNIX
cd task-manager




Design Choices
Django + DRF: Rapid development and clean API structuring.

SQLite: Simple and lightweight for testing (can be swapped to PostgreSQL for scaling).

Multi-user Support: JWT auth allows per-user task visibility.