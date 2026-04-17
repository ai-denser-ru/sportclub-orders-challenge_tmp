# ==============================================================================
# AUTOMATION & QUALITY GATES
# ==============================================================================

# EN: Lift the entire project using Docker Compose.
# ES: Levantar el proyecto completo usando Docker Compose.
docker-up:
	docker compose up --build

# ==============================================================================
# INTERACTIVE TESTING (DEVELOPMENT MODE)
# ==============================================================================

# EN: Run backend tests with full console output.
# ES: Correr tests de backend con salida detallada en consola.
test-backend:
	docker build --target builder -q -t sportclub-backend-test ./backend
	docker run --rm sportclub-backend-test uv run pytest -v

# EN: Run frontend tests (Vitest) with full console output.
# ES: Correr tests de frontend (Vitest) con salida detallada en consola.
test-frontend:
	docker build --target builder -q -t sportclub-frontend-test ./frontend
	docker run --rm sportclub-frontend-test npm run test

# EN: Run all tests interactively.
# ES: Correr todos los tests de forma interactiva.
test-all: test-backend test-frontend

# ==============================================================================
# CI/CD SIMULATION (QUALITY GATES)
# ==============================================================================

# EN: Fast verification. Uses Docker cache to validate build integrity.
# ES: Verificación rápida. Usa el caché de Docker para validar la integridad.
verify-cached:
	@echo "===> Running Fast Quality Gate..."
	docker build --target builder -t sportclub-backend-test ./backend
	docker build --target builder -t sportclub-frontend-test ./frontend
	@echo "===> Done!"

# EN: Full verification from scratch. Guaranteed environmental integrity.
# ES: Verificación completa desde cero. Garantiza la integridad del entorno.
verify-clean:
	@echo "===> Running Strict Quality Gate (No Cache)..."
	docker build --target builder --no-cache -t sportclub-backend-test ./backend
	docker build --target builder --no-cache -t sportclub-frontend-test ./frontend
	@echo "===> Done!"