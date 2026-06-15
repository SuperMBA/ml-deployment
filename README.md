# ML Deployment with FastAPI, Docker, Blue/Green Strategy, Nginx and GitHub Actions

## Project Overview

This project demonstrates a simple machine learning deployment workflow using FastAPI, Docker, Nginx, Blue/Green deployment and GitHub Actions.

The repository contains a minimal ML inference service that trains a simple model, exposes prediction endpoints and demonstrates how two application versions can be deployed in parallel and switched through an Nginx reverse proxy.

The project focuses on practical ML engineering concepts:

* serving ML models with FastAPI;
* containerizing applications with Docker;
* routing traffic through Nginx;
* implementing a Blue/Green deployment strategy;
* building and pushing Docker images through GitHub Actions;
* running a basic smoke test after deployment.

## Key Features

* Simple model training script: `train_model.py`
* Saved model artifact: `model.pkl`
* FastAPI inference service
* `/health` endpoint for service status checks
* `/predict` endpoint for model predictions
* Blue/Green deployment with two service versions
* Nginx reverse proxy for traffic switching
* Docker Compose setup for local orchestration
* GitHub Actions workflow for image build, push and smoke testing

## Blue/Green Deployment

The project uses a Blue/Green deployment strategy.

* **Blue** is the current production-like version of the service, for example `v1.0.0`.
* **Green** is the new version of the service, for example `v1.1.0`.

Both versions run simultaneously in the same Docker network:

```text
blue:8080
green:8080
```

External traffic is exposed only through Nginx on port `8080`.

Nginx forwards requests either to the Blue service or to the Green service. Switching between versions is done by updating the Nginx configuration and reloading Nginx without stopping both application containers.

This approach allows:

* safer rollout of a new version;
* separate testing of the Green version;
* fast rollback to the Blue version;
* reduced deployment risk.

## Architecture

```text
Client
  |
  v
Nginx reverse proxy
  |
  |---> Blue service: FastAPI app, model version v1.0.0
  |
  |---> Green service: FastAPI app, model version v1.1.0
```

The Green version additionally returns `"color": "green"` in the `/health` response to make the active version easier to identify.

## Repository Structure

```text
ml-deployment/
├── app/                         # Blue version of the FastAPI application
├── app_green/                   # Green version of the FastAPI application
├── nginx/
│   └── default.conf             # Nginx routing configuration
├── Dockerfile                   # Docker image for the Blue version
├── Dockerfile.green             # Docker image for the Green version
├── docker-compose.bg.yml        # Blue/Green + Nginx local setup
├── train_model.py               # Model training script
├── model.pkl                    # Serialized model artifact
└── .github/
    └── workflows/
        └── deploy.yml           # GitHub Actions workflow
```

## Local Run

### Start Blue, Green and Nginx

```bash
docker compose -f docker-compose.bg.yml up --build -d
```

### Check Service Health

```bash
curl -s http://127.0.0.1:8080/health && echo
```

### Run Prediction Request

```bash
curl -s -X POST http://127.0.0.1:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"x":[1,2,3]}' && echo
```

## Switching Between Blue and Green

To switch traffic, update the upstream target in `nginx/default.conf`.

Route traffic to Blue:

```nginx
proxy_pass http://blue:8080;
```

Route traffic to Green:

```nginx
proxy_pass http://green:8080;
```

After updating the configuration, reload Nginx:

```bash
docker compose -f docker-compose.bg.yml exec nginx nginx -s reload
```

## Model Versions

```text
Blue:  MODEL_VERSION=v1.0.0
Green: MODEL_VERSION=v1.1.0
```

The Green version returns an additional `"color": "green"` field in the `/health` response to confirm that traffic has been switched successfully.

## Logs

Docker collects logs from all running containers.

View Blue service logs:

```bash
docker compose -f docker-compose.bg.yml logs -f blue
```

View Green service logs:

```bash
docker compose -f docker-compose.bg.yml logs -f green
```

View Nginx logs:

```bash
docker compose -f docker-compose.bg.yml logs -f nginx
```

## CI/CD with GitHub Actions

The GitHub Actions workflow demonstrates a basic CI/CD process:

* build Docker image;
* push image to GitHub Container Registry;
* run a smoke test to verify that the service starts correctly.

This provides a minimal but practical example of automated ML service validation before deployment.

## Tech Stack

* Python
* FastAPI
* scikit-learn
* Docker
* Docker Compose
* Nginx
* GitHub Actions
* GitHub Container Registry
* REST API
* Blue/Green deployment

## Relevance

This project demonstrates practical ML engineering and deployment skills. It shows how a machine learning model can be wrapped into an API service, containerized, routed through a reverse proxy and tested through an automated CI workflow.

The same principles are applicable to healthcare analytics, Medical AI prototypes and production-oriented ML services.

## Author

**Margarita Balandina**
Medical Data Scientist | Dentist with German Approbation | MSc Data Science

Focus areas: Medical AI, Healthcare Analytics, Clinical Data, Machine Learning, MedTech and ML Engineering.
