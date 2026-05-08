HOMEPROJECT := $(CURDIR)
VENV_EXISTS := $(shell if [ -d "$(HOMEPROJECT)/.venv" ]; then echo 1; else echo 0; fi)
SYSTEM_IP := $(shell hostname -I | awk '{print $$1}')
API_URL := http://$(SYSTEM_IP)/api
API_URL_DEV := http://localhost:8000

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
	$(HOMEPROJECT)/.venv/bin/python -m icm database --start
	@echo "Instalando dependencias del frontend..."
	cd $(HOMEPROJECT)/presentation && npm install
	@echo "Compilando aplicación..."
	cd $(HOMEPROJECT)/presentation && NEXT_PUBLIC_API_URL=$(API_URL) npm run build
	@echo "Configuración finalizada."

setup-dev: venv
	@echo "Creando directorios requeridos..."
	mkdir -p $(HOMEPROJECT)/data/logs
	mkdir -p $(HOMEPROJECT)/data/sources
	touch $(HOMEPROJECT)/data/sources/devices.csv
	@echo "Inicializando bases de datos..."
	$(HOMEPROJECT)/.venv/bin/python -m icm database --start
	@echo "Instalando dependencias del frontend..."
	cd $(HOMEPROJECT)/presentation && npm install
	@echo "Compilando aplicación..."
	cd $(HOMEPROJECT)/presentation && NEXT_PUBLIC_API_URL=$(API_URL_DEV) npm run build
	@echo "Configuración finalizada."

build:
	@echo "Deteniendo aplicación..."
	pm2 stop $(HOMEPROJECT)/ecosystem.config.js
	pm2 delete $(HOMEPROJECT)/ecosystem.config.js
	@echo "Compilando aplicación..."
	cd $(HOMEPROJECT)/presentation && NEXT_PUBLIC_API_URL=$(API_URL) npm run build
	@echo "Levantando aplicación..."
	pm2 start $(HOMEPROJECT)/ecosystem.config.js
	@echo "Aplicación levantada."

build-dev:
	@echo "Deteniendo aplicación..."
	pm2 stop $(HOMEPROJECT)/ecosystem.config.js
	pm2 delete $(HOMEPROJECT)/ecosystem.config.js
	@echo "Compilando aplicación..."
	cd $(HOMEPROJECT)/presentation && NEXT_PUBLIC_API_URL=$(API_URL_DEV) npm run build
	@echo "Levantando aplicación..."
	pm2 start $(HOMEPROJECT)/ecosystem.config.js
	@echo "Aplicación levantada."

build-frontend:
	@echo "Compilando aplicación..."
	cd $(HOMEPROJECT)/presentation && NEXT_PUBLIC_API_URL=$(API_URL) npm run build
	@echo "Compilación finalizada."

build-frontend-dev:
	@echo "Compilando aplicación..."
	cd $(HOMEPROJECT)/presentation && NEXT_PUBLIC_API_URL=$(API_URL_DEV) npm run build
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

updater:
	$(HOMEPROJECT)/.venv/bin/python -m icm updater

ip:
	@echo $(SYSTEM_IP)
