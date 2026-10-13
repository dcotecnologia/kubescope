.DEFAULT_GOAL := help

UV ?= uv

.PHONY: help setup run dev debug preview language screenshot store-screenshots designer ui i18n appimage deb flatpak flatpak-lint flathub-submission windows windows-remote lint format test qt-libs build clean

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

run: qt-libs $(UI_PY) $(LANGUAGE_FILES) ## Start the desktop app
	$(RUN_ENV) $(UV) run kubescope

dev: qt-libs $(UI_PY) $(LANGUAGE_FILES) ## Start the app and restart it whenever the source changes
	$(RUN_ENV) $(UV) run python tools/dev.py

debug: qt-libs $(UI_PY) $(LANGUAGE_FILES) ## Start the app with debug logging, Python dev mode and Qt plugin tracing
	KUBESCOPE_DEBUG=1 QT_LOGGING_RULES="qt.qpa.*=true" $(RUN_ENV) $(UV) run python -X dev main.py

preview: qt-libs $(UI_PY) $(LANGUAGE_FILES) ## Open the UI with fake data, no cluster needed
	$(RUN_ENV) $(UV) run python tools/preview.py

UI_DIR := src/kubescope/ui
UI_FILES := $(wildcard $(UI_DIR)/*.ui)
UI_PY := $(UI_FILES:$(UI_DIR)/%.ui=$(UI_DIR)/ui_%.py)

$(UI_DIR)/ui_%.py: $(UI_DIR)/%.ui
	$(UV) run pyside6-uic $< -o $@

screenshot: $(UI_PY) $(LANGUAGE_FILES) ## Regenerate docs/screenshots/overview.png from the fake data
	mkdir -p docs/screenshots
	QT_QPA_PLATFORM=offscreen $(UV) run python tools/preview.py docs/screenshots/overview.png overview

store-screenshots: $(UI_PY) $(LANGUAGE_FILES) ## Render docs/screenshots/store/ (every theme) for the app stores
	QT_QPA_PLATFORM=offscreen $(UV) run python tools/store_screenshots.py

designer: qt-libs ## Open the .ui files in Qt Designer
	$(RUN_ENV) $(UV) run pyside6-designer -style fusion $(UI_FILES)

ui: $(UI_PY) ## Regenerate ui_*.py from changed .ui files (run/preview/build do it too)

TS_FILES := $(wildcard src/kubescope/translations/*.ts)
LANGUAGE_FILES := $(patsubst src/kubescope/translations/kubescope_%.ts,src/kubescope/languages/%.json,$(TS_FILES))
I18N_SOURCES := src/kubescope/window.py src/kubescope/log_tab.py src/kubescope/errors.py src/kubescope/theme_editor.py $(UI_FILES)

src/kubescope/languages/%.json: src/kubescope/translations/kubescope_%.ts
	$(UV) run python tools/ts_to_json.py

language: ## Start a new translation: make language CODE=es NAME=Español (then translate the .ts)
	@test -n "$(CODE)" -a -n "$(NAME)" || { echo "Usage: make language CODE=<code> NAME=<name in that language> [RTL=1]"; exit 1; }
	@test ! -e src/kubescope/translations/kubescope_$(CODE).ts || { echo "kubescope_$(CODE).ts already exists"; exit 1; }
	$(UV) run pyside6-lupdate -no-obsolete $(I18N_SOURCES) -ts src/kubescope/translations/kubescope_$(CODE).ts -target-language $(CODE)
	$(UV) run python tools/ts_to_json.py --new $(CODE) "$(NAME)" $(if $(RTL),--rtl)
	@echo "Now translate the .ts, then run: make i18n"

i18n: ## Extract new texts into the .ts files and write the JSON languages (edit .ts in Qt Linguist)
	$(UV) run pyside6-lupdate -no-obsolete $(I18N_SOURCES) -ts $(TS_FILES)
	$(UV) run python tools/ts_to_json.py

appimage: build ## Package the bundle as an AppImage in dist/ (Linux x86_64)
	$(UV) run python tools/build_appimage.py

deb: build ## Package the bundle as a .deb in dist/ (Debian/Ubuntu)
	$(UV) run python tools/build_deb.py

flatpak: ## Build the Flatpak from this working tree into dist/ (needs flatpak-builder)
	$(UV) run python tools/build_flatpak.py

flatpak-lint: ## Validate the Flatpak metainfo, desktop file and manifest like Flathub does
	$(UV) run python tools/flathub.py lint

flathub-submission: ## Gather the files for a Flathub pull request in dist/flathub/ and print the steps
	$(UV) run python tools/flathub.py package

windows: $(UI_PY) $(LANGUAGE_FILES) ## Build the Windows installer and zip (on Linux it runs in Wine)
ifeq ($(shell uname -s),Linux)
	$(UV) run python tools/windows_wine.py
else
	$(UV) run python tools/build_windows.py
endif

windows-remote: ## Build the Windows packages on GitHub Actions and download them to dist/
	$(UV) run python tools/windows_remote.py

lint: ## Check the code with ruff (lint and formatting)
	$(UV) run --extra dev ruff check .
	$(UV) run --extra dev ruff format --check .

format: ## Fix lint issues and format the code with ruff
	$(UV) run --extra dev ruff check --fix .
	$(UV) run --extra dev ruff format .

test: $(UI_PY) $(LANGUAGE_FILES) ## Run the tests
	$(UV) run --extra dev pytest -q

qt-libs: ## Download and extract the Qt/XCB libraries for Linux
ifeq ($(shell uname -s),Linux)
	$(UV) run --extra dev python tools/fetch_linux_qt_libs.py
else
	@echo "Skipping Linux Qt libraries on $(shell uname -s)"
endif

build: qt-libs $(UI_PY) $(LANGUAGE_FILES) ## Build the desktop bundle with the XCB library
	$(UV) run --extra build pyinstaller --noconfirm KubeScope.spec

clean: ## Remove build artifacts and the test cache
	rm -rf build dist .pytest_cache