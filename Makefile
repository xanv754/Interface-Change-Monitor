HOMEPROJECT := $(CURDIR)
VENV_EXISTS := $(shell if [ -d "$(HOMEPROJECT)/.venv" ]; then echo 1; else echo 0; fi)

.PHONY: venv setup

venv:
ifeq ($(VENV_EXISTS),0)
	@echo "Creando entorno virtual del sistema..."
	python -m venv $(HOMEPROJECT)/.venv
	$(HOMEPROJECT)/.venv/bin/pip install -e .
endif

setup: venv
	@echo "Creando directorios requeridos..."
	mkdir -p $(HOMEPROJECT)/data/logs
	mkdir -p $(HOMEPROJECT)/data/sources
	touch $(HOMEPROJECT)/data/sources/devices.csv
	@echo "Inicializando bases de datos..."
	$(HOMEPROJECT)/.venv/bin/python -m icm database start
	@echo "Instalando dependencias del frontend..."
	cd $(HOMEPROJECT)/presentation && npm install
	@echo "Compilando aplicación..."
	cd $(HOMEPROJECT)/presentation && npm run build
	@echo "Configuración finalizada."

build-frontend:
	@echo "Compilando aplicación..."
	cd $(HOMEPROJECT)/presentation && npm run build
	@echo "Compilación finalizada."

start:
	@echo "Levantando aplicación..."
	pm2 start $(HOMEPROJECT)/ecosystem.config.js
	@echo "Aplicación levantada."

stop:
	@echo "Deteniendo aplicación..."
	pm2 stop $(HOMEPROJECT)/ecosystem.config.js
	pm2 delete $(HOMEPROJECT)/ecosystem.config.js
	@echo "Aplicación detenida."