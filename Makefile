UV_LINK_MODE := copy

install:
	uv venv --python 3.13
	source .venv/bin/activate
	UV_LINK_MODE=$(UV_LINK_MODE) uv sync

run:
	UV_LINK_MODE=$(UV_LINK_MODE) uv run pac_man.py config.json

debug:
	UV_LINK_MODE=$(UV_LINK_MODE) uv run python3 -m pdb pac_man.py config.json

clean:
	find . -not -path "./.venv*" -name "__pycache__" -exec rm -rf {} +
	find . -not -path "./.venv*" -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build dist

lint:
	UV_LINK_MODE=$(UV_LINK_MODE) uv run flake8 . --exclude=.venv
	UV_LINK_MODE=$(UV_LINK_MODE) uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude "(.venv)"

lint-strict:
	UV_LINK_MODE=$(UV_LINK_MODE) uv run flake8 . --exclude=.venv
	UV_LINK_MODE=$(UV_LINK_MODE) uv run mypy . --strict --exclude "(.venv)"

cow:
	UV_LINK_MODE=$(UV_LINK_MODE) uvx pycowsay hello from uv

build:
	rm -rf build dist
	UV_LINK_MODE=$(UV_LINK_MODE) uv run pyinstaller \
		--windowed \
		--name pac_man \
		--add-data "visualizer/views/assets:visualizer/views/assets" \
		--add-data "config.json:." \
		pac_man.py

	rm -rf dist/pac_man/_internal/arcade/VERSION
	cp .venv/lib/python3.13/site-packages/arcade/VERSION dist/pac_man/_internal/arcade/VERSION

	cp config.json dist/pac_man/config.json

	cd dist && zip -r pac_man_linux.zip pac_man