# Employee Leave Management - DevOps Project

Project title:

Design and Implementation of an Automated CI/CD Pipeline for a Containerized Web Application with Real-Time Monitoring

## Technology

- Python
- Flask
- SQLite
- Pytest
- Git/GitHub
- Docker
- GitHub Actions
- Prometheus
- Grafana

## Demo accounts

Employee:
- Username: employee
- Password: employee123

Admin:
- Username: admin
- Password: admin123

## Local Python run

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest -q
python app.py
```

Open:
http://127.0.0.1:5000

Metrics:
http://127.0.0.1:5000/metrics

Health:
http://127.0.0.1:5000/health

## Docker + monitoring

Install Docker Desktop first, then run:

```powershell
docker compose up --build -d
```

Open:
- App: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Grafana default local login is normally:
- Username: admin
- Password: admin

Change the password when prompted if Grafana asks.

## Stop containers

```powershell
docker compose down
```

## CI/CD

Push the repository to GitHub and make the default branch `main`.

GitHub Actions will:
1. Install Python
2. Install dependencies
3. Run Pytest
4. Build the Docker image
5. On pushes to main, publish the image to GitHub Container Registry (GHCR)
