.DEFAULT_GOAL := help

UV ?= uv

.PHONY: help setup run test kubectl qt-libs build clean

help: ## Lista os comandos disponíveis
	@awk 'BEGIN { FS = ":.*##" } /^[a-zA-Z_-]+:.*##/ { printf "  %-12s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

setup: ## Sincroniza as dependências do projeto
	$(UV) sync --extra dev --extra build

ifeq ($(shell uname -s),Linux)
QT_XCB_LIB_DIR := $(CURDIR)/vendor/linux/$(shell uname -m)
RUN_ENV := LD_LIBRARY_PATH="$(QT_XCB_LIB_DIR):$${LD_LIBRARY_PATH}"
else
RUN_ENV :=
endif

run: qt-libs ## Inicia a aplicação desktop
	$(RUN_ENV) $(UV) run kubescope

test: ## Executa os testes
	$(UV) run --extra dev pytest -q

kubectl: ## Baixa e verifica o kubectl oficial
	$(UV) run --extra dev python tools/fetch_kubectl.py

qt-libs: ## Baixa e extrai bibliotecas Qt/XCB para Linux
ifeq ($(shell uname -s),Linux)
	$(UV) run --extra dev python tools/fetch_linux_qt_libs.py
else
	@echo "Skipping Linux Qt libraries on $(shell uname -s)"
endif

build: qt-libs ## Gera o bundle desktop com kubectl e dependência XCB
	$(UV) run --extra build pyinstaller --noconfirm KubeScope.spec

clean: ## Remove os artefatos de build e cache de testes
	rm -rf build dist .pytest_cache