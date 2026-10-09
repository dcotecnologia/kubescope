.DEFAULT_GOAL := help

UV ?= uv

.PHONY: help setup run preview screenshot designer ui i18n appimage deb flatpak windows windows-remote lint format test kubectl qt-libs build clean

help: ## List the available commands
	@awk 'BEGIN { FS = ":.*##" } /^[a-zA-Z_-]+:.*##/ { printf "  %-12s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

setup: ## Sync the project dependencies
	$(UV) sync --extra dev --extra build

ifeq ($(shell uname -s),Linux)
QT_XCB_LIB_DIR := $(CURDIR)/vendor/linux/$(shell uname -m)
RUN_ENV := LD_LIBRARY_PATH="$(QT_XCB_LIB_DIR):$${LD_LIBRARY_PATH}"
else
RUN_ENV :=
endif

run: qt-libs $(UI_PY) $(QM_FILES) ## Start the desktop app
	$(RUN_ENV) $(UV) run kubescope

preview: qt-libs $(UI_PY) $(QM_FILES) ## Open the UI with fake data, no cluster needed
	$(RUN_ENV) $(UV) run python tools/preview.py

UI_DIR := src/kubescope/ui
UI_FILES := $(wildcard $(UI_DIR)/*.ui)
UI_PY := $(UI_FILES:$(UI_DIR)/%.ui=$(UI_DIR)/ui_%.py)

$(UI_DIR)/ui_%.py: $(UI_DIR)/%.ui
	$(UV) run pyside6-uic $< -o $@

screenshot: $(UI_PY) $(QM_FILES) ## Regenerate docs/screenshots/overview.png from the fake data
	mkdir -p docs/screenshots
	QT_QPA_PLATFORM=offscreen $(UV) run python tools/preview.py docs/screenshots/overview.png overview

designer: qt-libs ## Open the .ui files in Qt Designer
	$(RUN_ENV) $(UV) run pyside6-designer -style fusion $(UI_FILES)

ui: $(UI_PY) ## Regenerate ui_*.py from changed .ui files (run/preview/build do it too)

TS_FILES := $(wildcard src/kubescope/translations/*.ts)
QM_FILES := $(TS_FILES:.ts=.qm)
I18N_SOURCES := src/kubescope/window.py src/kubescope/log_tab.py src/kubescope/errors.py $(UI_FILES)

%.qm: %.ts
	$(UV) run pyside6-lrelease $< -qm $@

i18n: ## Extract new texts into the .ts files and compile the .qm (edit .ts in Qt Linguist)
	$(UV) run pyside6-lupdate -no-obsolete $(I18N_SOURCES) -ts $(TS_FILES)
	$(MAKE) --always-make $(QM_FILES)

appimage: build ## Package the bundle as an AppImage in dist/ (Linux x86_64)
	$(UV) run python tools/build_appimage.py

deb: build ## Package the bundle as a .deb in dist/ (Debian/Ubuntu)
	$(UV) run python tools/build_deb.py

flatpak: build ## Package the bundle as a Flatpak in dist/ (needs flatpak-builder)
	$(UV) run python tools/build_flatpak.py

windows: ## Build the Windows installer and zip (run this on Windows)
	$(UV) run python tools/build_windows.py

windows-remote: ## Build the Windows packages on GitHub Actions and download them to dist/
	$(UV) run python tools/windows_remote.py

lint: ## Check the code with ruff (lint and formatting)
	$(UV) run --extra dev ruff check .
	$(UV) run --extra dev ruff format --check .

format: ## Fix lint issues and format the code with ruff
	$(UV) run --extra dev ruff check --fix .
	$(UV) run --extra dev ruff format .

test: $(UI_PY) $(QM_FILES) ## Run the tests
	$(UV) run --extra dev pytest -q

kubectl: ## Download and verify the official kubectl
	$(UV) run --extra dev python tools/fetch_kubectl.py

qt-libs: ## Download and extract the Qt/XCB libraries for Linux
ifeq ($(shell uname -s),Linux)
	$(UV) run --extra dev python tools/fetch_linux_qt_libs.py
else
	@echo "Skipping Linux Qt libraries on $(shell uname -s)"
endif

build: qt-libs $(UI_PY) $(QM_FILES) ## Build the desktop bundle with kubectl and the XCB library
	$(UV) run --extra build pyinstaller --noconfirm KubeScope.spec

clean: ## Remove build artifacts and the test cache
	rm -rf build dist .pytest_cache
