# MediQueue – Smart Hospital Queue Manager

A small educational REST API demonstrating patient registration, doctor-wise queues,
digital tokens, token lookup, calling the next patient, and a health endpoint.

## Requirements

- Python 3.12+
- Git
- Docker Desktop (for container build/run)
- Jenkins with a Linux agent that has Python 3 installed
- Ubuntu/Linux with Ansible and systemd for the Ansible stage
- Minikube and kubectl for the Kubernetes stage

## 1. Run locally (Windows PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
in that terminal and activate again.

## 2. Test

```powershell
python -m pytest -v
```

The tests reset the in-memory store between tests. The app itself uses in-memory
storage, so records disappear when the process restarts. This is intentional for
the assignment's simple sample-app scope.

## 3. Git

```bash
git init
git add .
git commit -m "Initial MediQueue application"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
git checkout -b feature/patient-registration
```

Make a small change, commit and push the feature branch, then create and merge a
Pull Request on GitHub. This demonstrates two branches and a merge.

## 4. Jenkins

Create a Pipeline job connected to this Git repository and use `Jenkinsfile` from
SCM. The included Jenkinsfile expects a Linux agent with `python3`, `venv`, `pip`
and the Jenkins JUnit plugin available. Configure SCM polling or a GitHub webhook
so a push triggers the job automatically.

## 5. Docker

```bash
docker build -t mediqueue:v1 .
docker run --rm -p 8000:8000 mediqueue:v1
```

Open http://localhost:8000/docs

## 6. Ansible (Ubuntu/Linux with systemd)

The included playbook uses localhost as its target and requires privilege
escalation. Run it from the repository root:

```bash
cd ansible
ansible-playbook -i inventory playbook.yml --ask-become-pass
```

This role installs Python, copies the app, creates a virtual environment, installs
dependencies, and manages a systemd service. WSL may require systemd to be enabled.
For a separate VM, replace the localhost inventory entry with that host and configure
SSH access.

## 7. Kubernetes with Minikube

Build the image inside Minikube's Docker environment. In PowerShell:

```powershell
minikube start
minikube docker-env --shell powershell | Invoke-Expression
docker build -t mediqueue:v1 .
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl get pods
kubectl get svc
minikube service mediqueue-service
```

Scale from 3 to 5 and capture evidence:

```bash
kubectl scale deployment mediqueue --replicas=5
kubectl get pods
kubectl scale deployment mediqueue --replicas=3
kubectl get pods
```

The Deployment includes liveness and readiness probes against `/health`.

## API quick reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Welcome |
| GET | `/health` | Health check |
| GET | `/doctors` | List departments/doctors |
| POST | `/patients` | Register patient |
| GET | `/queue/{doctor_id}` | View doctor queue |
| GET | `/token/{token_id}` | Check token |
| PUT | `/queue/next/{doctor_id}` | Call next waiting patient |

Example request for `POST /patients`:

```json
{
  "name": "Asha",
  "age": 24,
  "doctor_id": 1
}
```

## Important limitations

This is a classroom demonstration, not a production medical system. It has no
authentication, database, privacy controls, audit logging, or clinical decision
support. Do not enter real patient information. Each container/pod has its own
in-memory data, so queues are not shared across replicas. A production design
would need shared persistent storage and coordinated queue state.
