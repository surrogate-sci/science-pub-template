.PHONY: lint
lint:
	ruff check --exit-zero .
	ruff format --check .

.PHONY: format
format:
	ruff check --fix .
	ruff format .

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: test
test:
	pytest -v .

.PHONY: execute
execute:
	# Project-wide render without executing code cells.
	# Instead, rely on pre-computed results present in `_freeze/`.
	quarto render

	# Now, render `index.ipynb` with code execution.
	# This will populate `_freeze/index/` with pre-computed results.
	quarto render index.ipynb --execute

.PHONY: preview
preview:
	quarto preview

.PHONY: preview-warm
preview-warm:
	quarto preview --profile warm-journal

.PHONY: preview-technical
preview-technical:
	quarto preview --profile technical-notebook

.PHONY: render-warm
render-warm:
	quarto render --profile warm-journal

.PHONY: render-technical
render-technical:
	quarto render --profile technical-notebook

.PHONY: execute-demo
execute-demo:
	# This command is only necessary when changes are made to the demo notebook
	# for development of the notebook pub template.
	quarto render examples/demo.ipynb --execute
