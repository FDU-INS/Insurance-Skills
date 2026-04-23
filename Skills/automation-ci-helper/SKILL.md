---
name: automation-ci-helper
description: Instructions for managing CI pipelines, GitHub Actions workflows, Airflow DAGs, and automation scripts in the insurance analytics project.
---

# Automation & CI Helper Skill

This skill covers all automation in the insurance analytics project: GitHub Actions CI workflows, the Apache Airflow data pipeline, the Makefile task runner, pre-commit hooks, and quality-gate tooling.

## Automation components at a glance

| Component | Location | Purpose |
|---|---|---|
| GitHub Actions – CI | `.github/workflows/ci-postgres.yml` | Lint → test → SonarCloud on every push/PR |
| GitHub Actions – Release | `.github/workflows/release.yml` | Manual workflow dispatch: bumps patch version tag and creates a GitHub Release (no build artifact is uploaded) |
| GitHub Actions – Scheduled | `.github/workflows/scheduled-pipeline.yml` | Runs the pipeline on a schedule (now delegates to a reusable workflow) |
| GitHub Actions – Reusable pipeline | `.github/workflows/run-pipeline.yml` | Reusable workflow that owns Postgres service and runs ingest/ETL/upload |
| Composite actions | `.github/actions/setup-python-env`, `.github/actions/run-etl` | Shared actions for Python setup and running ETL steps |
| Airflow DAG | `airflow/dags/insurance_pipeline_dag.py` | Orchestrates the ETL end-to-end |
| Makefile | `Makefile` | Developer task runner (local shortcuts) |
| Pre-commit hooks | `.pre-commit-config.yaml` | Auto-formats and lints on every `git commit` |

## GitHub Actions: CI workflow (`ci-postgres.yml`)

The CI workflow has **three sequential jobs**:

```
lint  →  etl  →  sonarcloud
```

### Job 1 – `lint` (static analysis)

Runs on every **push** to `main`/`master` that touches `src/**`, `tests/**`, `src/sql/**`, `requirements.txt`, `pyproject.toml`, `sonar-project.properties`, or `.github/workflows/ci-postgres.yml`. **Pull requests** to those branches trigger `lint` only when `src/**`, `tests/**`, `requirements.txt`, or `pyproject.toml` are changed (`src/sql/**` and other config files do **not** trigger CI on PRs).

Steps:
1. `ruff format --check` – formatting check
2. `ruff check` + `pylint` – linting (ruff is non-blocking on auto-fixable issues; pylint is non-blocking)
3. `mypy src` – static type checking
4. `bandit -r src` – security scan
5. `radon cc` + `radon mi` – cyclomatic complexity and maintainability index

### Job 2 – `etl` (ETL smoke test with PostgreSQL)

The project now centralises the integration pipeline in a reusable workflow: `.github/workflows/run-pipeline.yml`.

Key points:

- The reusable workflow owns the **Postgres 15 service** and offers two modes via inputs:
	- `seed-db: true` — initialise and seed the DB with stable fixtures (used by CI tests)
	- `seed-db: false` — run a live Kaggle ingest via `src.load` (used by the scheduled run)
- Schema application is no longer performed with runner `psql -f ...` in multiple places; the loader/seed script executes the canonical DDL (`src/sql/ddl_create_tables.sql`) via the same Python helper (`_apply_ddl()`), so CI and scheduled runs share the exact schema logic.
- The test flow (CI) typically calls the reusable workflow with `seed-db: true`, runs the ETL steps, and then a dedicated coverage job collects and uploads coverage artifacts.

Key environment variable set by the workflow:

```yaml
DATABASE_URL: postgresql+psycopg2://postgres:postgres@localhost:5432/insurdb
```

### Job 3 – `sonarcloud`

Downloads the test artifacts (coverage + JUnit XML) and runs SonarCloud analysis. The Sonar job now depends on the CI coverage job (which produces `build/reports/coverage.xml` and `build/reports/junit-report.xml`).

Secrets used:

- `SONAR_TOKEN` – SonarCloud authentication
- `CODECOV_TOKEN` – Codecov upload (used by the CI coverage job)

### Triggering CI manually

Push any change to a file under `src/`, `tests/`, `src/sql/`, `requirements.txt`, `pyproject.toml`, `sonar-project.properties`, or `.github/workflows/ci-postgres.yml` on a branch targeting `main`/`master`. A pull request against those branches also triggers CI when `src/**`, `tests/**`, `requirements.txt`, or `pyproject.toml` are modified.

Note: because the ETL and service logic are now in a reusable workflow, changes to the pipeline are tested more consistently across CI and scheduled runs.

## Makefile: local task runner

Run `make help` to see all targets. Most-used ones:

```bash
make install        # pip install all dependencies
make test           # pytest with coverage
make lint           # flake8 + ruff + pylint
make format         # black + isort + ruff format + docformatter
make check-types    # mypy --strict
make quality        # bandit + radon + xenon + cohesion + vulture
make check          # lint + check-types + test + quality (full gate)

make db-init        # apply src/sql/ddl_create_tables.sql
make db-reset       # DROP SCHEMA + re-apply DDL
make kaggle-load    # download Kaggle dataset and load into PostgreSQL
make setup          # install + db-init + kaggle-load (full first-time setup)

make airflow-up     # start Airflow via Docker Compose (port 8080)
make airflow-down   # stop Airflow
make airflow-logs   # tail scheduler logs
```

## Airflow DAG

The DAG is defined in `airflow/dags/insurance_pipeline_dag.py` and orchestrates:

```
kaggle_ingest  →  [run_transform_kpis, run_ml_model]  →  generate_excel_report
```

| Task | Module invoked | Notes |
|---|---|---|
| `kaggle_ingest` | `src.load --kaggle-config` | Downloads dataset from Kaggle and loads into DB; requires `KAGGLE_USERNAME` + `KAGGLE_KEY` env vars |
| `run_transform_kpis` | `src.transform` | Runs in parallel with `run_ml_model` |
| `run_ml_model` | `src.model` | Runs in parallel with `run_transform_kpis` |
| `generate_excel_report` | `src.report` | Runs after both transform and model complete |

The schedule defaults to daily at 06:00 UTC and can be overridden via the `AIRFLOW_PIPELINE_SCHEDULE` environment variable. The project directory is set via `AIRFLOW_PROJECT_DIR`.

### Starting Airflow locally

```bash
make airflow-up
# Airflow UI → http://localhost:8080   login: admin / admin
make airflow-down   # stop when done
```

Airflow runs via Docker Compose (`airflow/docker-compose-airflow.yml`) on a dedicated `insurance-network` Docker network.

## Pre-commit hooks (`.pre-commit-config.yaml`)

Pre-commit runs automatically on `git commit`. To run it manually against all files:

```bash
make pre-commit
# or directly:
pre-commit run --all-files
```

This project uses **Ruff** as the unified linter and formatter in pre-commit, replacing the
former `black`, `isort`, and `flake8` hooks. Typical hooks: `ruff` (lint + fix),
`ruff-format`, trailing-whitespace / end-of-file fixers.

First-time setup:

```bash
pip install pre-commit
pre-commit install   # installs the git hook
```

## Quality gate script (`scripts/check_quality.sh`)

A shell script that aggregates multiple quality checks in one pass:

```bash
make quality-check
# or directly:
./scripts/check_quality.sh
```

Run this locally before opening a pull request to catch issues that CI will also catch.

## Adding a new CI step

Prefer adding new behaviour as a composite action or to the reusable workflow so it can be exercised by both CI and scheduled runs. General steps:

1. If the change affects runtime/test behaviour (DB, ETL), update `./.github/workflows/run-pipeline.yml` or add a new composite action under `./.github/actions/` so callers can reuse it.
2. Otherwise add a step in `ci-postgres.yml` (lint/coverage) or in `run-pipeline.yml` for runtime steps.
3. Add required Python tooling to `requirements.txt` and/or `pyproject.toml`.
4. Test locally (run `make test`) and push to a feature branch to validate the workflow in Actions.

## Common CI failures and fixes

| Failure | Likely cause | Fix |
|---|---|---|
| `ruff format --check` fails | Code not formatted | Run `make format` locally, then commit |
| `mypy` errors | Missing type annotations or wrong types | Add/fix type hints in `src/` |
| `bandit` security warning | Use of a flagged function (e.g. `subprocess`, `pickle`) | Refactor or add `# nosec` with justification |
| Postgres connection refused | Service container not ready | The reusable workflow uses health-checks on the Postgres service; if you see failures, confirm the `run-pipeline.yml` service definition and health options. |
| `pytest` collection error | Import error in `src/` | Run `pytest -q` locally with the same `DATABASE_URL` to reproduce |
| SonarCloud gate fails | Coverage below threshold or new bugs found | Fix the issues reported in the SonarCloud PR comment |

## Secrets required in GitHub repository settings

| Secret name | Used by |
|---|---|
| `SONAR_TOKEN` | SonarCloud scan (job 3) |
| `CODECOV_TOKEN` | Codecov coverage upload (job 2) |
| `KAGGLE_USERNAME` | Scheduled pipeline — Kaggle dataset ingest |
| `KAGGLE_KEY` | Scheduled pipeline — Kaggle dataset ingest |

Additional notes:

- The canonical DDL lives in `src/sql/ddl_create_tables.sql` (loaded via `importlib.resources` in `src.load`). The Python helpers `_apply_ddl()` and `_table_columns()` (in `src.load`) are the preferred way to apply and reflect the schema programmatically; the seed script `.github/scripts/seed_test_db.py` reuses them.
- Test and coverage artifacts are written to `build/reports/` by default (`junit-report.xml`, `coverage.xml`, `htmlcov/`). Update `pyproject.toml` / `Makefile` if you need a different location.
