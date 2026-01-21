---
title: Production Deployment Guide
description: Comprehensive guide for deploying Python applications to production
audience:
  - users
  - contributors
tags:
  - deployment
  - production
  - operations
---

# Production Deployment Guide

This guide covers best practices for deploying Python applications built with this template to production environments.

## Pre-deployment Checklist

Before deploying to production, verify the following:

- [ ] All tests passing (`doit test`)
- [ ] Security scan clean (`doit security` or `bandit`)
- [ ] Dependencies audited (`uv pip audit` or `pip-audit`)
- [ ] Environment variables documented
- [ ] Secrets management configured
- [ ] Logging configured for production
- [ ] Health check endpoints implemented
- [ ] Error reporting configured

## Environment Configuration

### Production vs Development Settings

Use environment variables to distinguish between environments:

```python
import os

# Environment detection
ENV = os.getenv("APP_ENV", "development")
DEBUG = ENV == "development"

# Environment-specific settings
if ENV == "production":
    LOG_LEVEL = "INFO"
    DATABASE_POOL_SIZE = 20
else:
    LOG_LEVEL = "DEBUG"
    DATABASE_POOL_SIZE = 5
```

### Environment Variable Management

**Required variables for production:**

| Variable | Purpose | Example |
|----------|---------|---------|
| `APP_ENV` | Environment identifier | `production` |
| `DATABASE_URL` | Database connection string | `postgresql://...` |
| `SECRET_KEY` | Application secret | (generated) |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

**Best practices:**

- Never commit `.env` files with secrets
- Use `.env.example` to document required variables
- Validate all required variables on startup

```python
def validate_environment() -> None:
    """Validate required environment variables are set."""
    required = ["DATABASE_URL", "SECRET_KEY"]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {missing}")
```

### Secret Injection Patterns

#### HashiCorp Vault

```python
import hvac

def get_vault_secret(path: str, key: str) -> str:
    """Retrieve secret from HashiCorp Vault."""
    client = hvac.Client(url=os.getenv("VAULT_ADDR"))
    client.token = os.getenv("VAULT_TOKEN")
    secret = client.secrets.kv.v2.read_secret_version(path=path)
    return secret["data"]["data"][key]
```

#### AWS Secrets Manager

```python
import boto3
import json

def get_aws_secret(secret_name: str) -> dict:
    """Retrieve secret from AWS Secrets Manager."""
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])
```

#### Kubernetes Secrets

Mount secrets as environment variables or files:

```yaml
# kubernetes/deployment.yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: database-url
```

### Configuration Validation on Startup

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings with validation."""

    app_env: str = "development"
    database_url: str
    secret_key: str
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

# Validate on import
settings = Settings()
```

## Logging & Monitoring

### Structured Logging (JSON Format)

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Format log records as JSON for aggregation systems."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "correlation_id"):
            log_data["correlation_id"] = record.correlation_id
        return json.dumps(log_data)
```

### Log Levels for Production

| Level | Use Case |
|-------|----------|
| `ERROR` | Failures requiring immediate attention |
| `WARNING` | Unexpected behavior, potential issues |
| `INFO` | Key business events, request/response summaries |
| `DEBUG` | Detailed diagnostic info (disabled in production) |

**Recommendation:** Use `INFO` as the default production log level.

### Correlation IDs for Tracing

```python
import uuid
from contextvars import ContextVar

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

def set_correlation_id(request_id: str | None = None) -> str:
    """Set correlation ID for the current request context."""
    cid = request_id or str(uuid.uuid4())
    correlation_id.set(cid)
    return cid

def get_correlation_id() -> str:
    """Get the current correlation ID."""
    return correlation_id.get()
```

### Integration Points

#### DataDog

```python
from ddtrace import tracer

tracer.configure(
    hostname=os.getenv("DD_AGENT_HOST", "localhost"),
    port=8126,
)
```

#### Prometheus

```python
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total request count",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"]
)

# Start metrics server
start_http_server(8000)
```

### Health Check Endpoints

```python
from dataclasses import dataclass

@dataclass
class HealthStatus:
    status: str
    database: str
    cache: str

async def health_check() -> HealthStatus:
    """Comprehensive health check for all dependencies."""
    db_status = await check_database()
    cache_status = await check_cache()

    overall = "healthy" if all([
        db_status == "healthy",
        cache_status == "healthy"
    ]) else "unhealthy"

    return HealthStatus(
        status=overall,
        database=db_status,
        cache=cache_status
    )
```

## Error Handling

### Exception Reporting

#### Sentry Integration

```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("APP_ENV"),
    traces_sample_rate=0.1,  # 10% of transactions
)
```

#### Rollbar Integration

```python
import rollbar

rollbar.init(
    access_token=os.getenv("ROLLBAR_TOKEN"),
    environment=os.getenv("APP_ENV"),
)
```

### Graceful Degradation Patterns

```python
from functools import wraps
from typing import TypeVar, Callable, Any

T = TypeVar("T")

def with_fallback(fallback_value: T) -> Callable:
    """Decorator that returns fallback value on failure."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"{func.__name__} failed, using fallback: {e}")
                return fallback_value
        return wrapper
    return decorator

@with_fallback(fallback_value=[])
def get_recommendations(user_id: str) -> list:
    """Get personalized recommendations with fallback to empty list."""
    return recommendation_service.get(user_id)
```

### Circuit Breaker Pattern

```python
import time
from enum import Enum
from dataclasses import dataclass, field

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreaker:
    """Circuit breaker for external service calls."""

    failure_threshold: int = 5
    recovery_timeout: float = 30.0

    _failure_count: int = field(default=0, init=False)
    _last_failure_time: float = field(default=0.0, init=False)
    _state: CircuitState = field(default=CircuitState.CLOSED, init=False)

    def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute function with circuit breaker protection."""
        if self._state == CircuitState.OPEN:
            if time.time() - self._last_failure_time > self.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("Circuit is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        self._failure_count = 0
        self._state = CircuitState.CLOSED

    def _on_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = time.time()
        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
```

## Performance

### Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    os.getenv("DATABASE_URL"),
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections after 1 hour
)
```

### Caching Strategies

```python
import redis
from functools import wraps
import json
from typing import Callable, Any

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

def cached(ttl: int = 300) -> Callable:
    """Cache function results in Redis."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_key = f"{func.__name__}:{hash((args, tuple(kwargs.items())))}"

            cached_value = redis_client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)

            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

### Async Workers

#### Celery

```python
from celery import Celery

app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
```

#### arq (Async)

```python
from arq import create_pool
from arq.connections import RedisSettings

async def startup() -> None:
    redis = await create_pool(
        RedisSettings.from_dsn(os.getenv("REDIS_URL"))
    )
```

### Resource Limits

Set appropriate limits in your deployment configuration:

```yaml
# kubernetes/deployment.yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

## Security Hardening

### Non-root Containers

```dockerfile
# Dockerfile
FROM python:3.12-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app
COPY --chown=appuser:appuser . .

USER appuser

CMD ["python", "-m", "package_name"]
```

### Read-only Filesystems

```yaml
# kubernetes/deployment.yaml
securityContext:
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000

volumeMounts:
  - name: tmp
    mountPath: /tmp

volumes:
  - name: tmp
    emptyDir: {}
```

### Network Policies

```yaml
# kubernetes/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              role: frontend
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              role: database
      ports:
        - protocol: TCP
          port: 5432
```

### Secrets Rotation

Implement periodic secret rotation:

```python
import schedule
import time

def rotate_database_credentials() -> None:
    """Rotate database credentials from secrets manager."""
    new_creds = get_vault_secret("database", "credentials")
    update_connection_pool(new_creds)
    logger.info("Database credentials rotated successfully")

# Schedule rotation
schedule.every().day.at("03:00").do(rotate_database_credentials)
```

## Deployment Strategies

### Blue-Green Deployment

Maintain two identical production environments:

1. **Blue** (current): Serving live traffic
2. **Green** (new): Updated version ready for switch

```bash
# Switch traffic from blue to green
kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'
```

### Canary Releases

Gradually roll out changes to a subset of users:

```yaml
# kubernetes/canary-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1  # Small percentage of traffic
  selector:
    matchLabels:
      app: myapp
      track: canary
```

### Rolling Updates

Default Kubernetes strategy for zero-downtime updates:

```yaml
# kubernetes/deployment.yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

### Rollback Procedures

```bash
# Kubernetes rollback
kubectl rollout undo deployment/myapp

# View rollout history
kubectl rollout history deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=2
```

## Publishing to PyPI

Publishing your package to PyPI makes it available for installation via `pip install`.

### Pre-publish Checklist

- [ ] Version updated (via `doit release` or git tag)
- [ ] All tests passing (`doit test`)
- [ ] CHANGELOG updated
- [ ] README accurate and up-to-date
- [ ] License file present
- [ ] No secrets in source code

### Configure PyPI Credentials

#### Using API Tokens (Recommended)

Generate a token at https://pypi.org/manage/account/token/

```bash
# Configure uv with PyPI token
export UV_PUBLISH_TOKEN=pypi-xxxxxxxxxxxx

# Or use keyring
uv run keyring set https://upload.pypi.org/legacy/ __token__
```

#### Using Trusted Publishing (GitHub Actions)

Configure OIDC in your PyPI project settings, then in your workflow:

```yaml
# .github/workflows/release.yml
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # Required for trusted publishing
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

### Build and Publish

```bash
# Build distribution packages
uv build

# This creates:
# - dist/package_name-x.y.z.tar.gz (source distribution)
# - dist/package_name-x.y.z-py3-none-any.whl (wheel)

# Publish to PyPI
uv publish

# Or with explicit token
uv publish --token pypi-xxxxxxxxxxxx
```

### Verify Publication

```bash
# Check package on PyPI
pip index versions package-name

# Test installation in clean environment
uv venv /tmp/test-install
uv pip install --python /tmp/test-install package-name
```

### Version Management

This template uses git tags as the source of truth for versions:

```bash
# Create a release (updates version from git tag)
doit release

# Version is automatically determined from git tags
# Never manually edit version in pyproject.toml
```

## Quick Reference

### Deployment Checklist

| Step | Command/Action |
|------|----------------|
| Run tests | `doit test` |
| Security scan | `doit security` |
| Audit deps | `uv pip audit` |
| Build image | `docker build -t myapp:version .` |
| Push image | `docker push registry/myapp:version` |
| Deploy | `kubectl apply -f kubernetes/` |
| Verify | `kubectl rollout status deployment/myapp` |

### Common Issues

| Issue | Solution |
|-------|----------|
| Container OOMKilled | Increase memory limits |
| Connection pool exhausted | Increase pool size or fix connection leaks |
| Slow startup | Add readiness probes, optimize imports |
| High latency | Check database queries, add caching |

## See Also

- [Development Deployment Guide](development.md) - Local development setup
- [CI/CD Testing Guide](../development/ci-cd-testing.md) - Automated testing pipelines
- [Release Automation](../development/release-and-automation.md) - Versioning and releases
