SRC_DIR=.

format:
	uv run ruff format $(SRC_DIR)
	uv run ruff check $(SRC_DIR) --fix

lint:
	uv run mypy $(SRC_DIR)
	uv run ruff check $(SRC_DIR)
	uv run ruff format $(SRC_DIR) --check

run-cli:
	uv run run_cli.py

run:
	uv run run_http.py

plot:
	uv run python plot_dependencies.py
