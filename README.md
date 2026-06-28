# Generador de Horarios Escolares

API REST (FastAPI + PostgreSQL) que arma las grillas de horarios de los grados
asignando docentes curriculares mediante un solver CSP (backtracking).

## Stack
- FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- Solver: backtracking CSP (MRV + forward checking)