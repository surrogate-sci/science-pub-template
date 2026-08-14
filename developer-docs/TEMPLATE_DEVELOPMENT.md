# Template Development Guide

This guide is for people **developing the science-pub-template itself** — adding extensions, updating the demo notebook, modifying `_quarto.yml`, or changing how the template works. If you're using the template to create a publication, see the [Quickstart Guide](QUICKSTART.md) instead.

## Environment setup

You need [Quarto](https://quarto.org/docs/get-started/) installed separately — it's not included in `env.yml`.

```bash
conda env create -n science-pub-template --file env.yml
conda activate science-pub-template
pip install -e .
pre-commit install
```

Verify with `make preview` — the site should open in your browser.

## Development workflow

1. Create a branch off `main`.
2. Make your changes (extensions, config, demo notebook, etc.).
3. Preview locally with `make preview`.
4. Test with `make execute-demo` (re-executes the demo notebook).
5. Run `make pre-commit` to ensure linting and formatting pass.
6. Open a PR for review.

## The demo notebook

After modifying the demo notebook (`examples/demo.ipynb`) or anything that affects its rendering (filters, theme, `_quarto.yml`), re-execute it:

```bash
make execute-demo
```

This runs `quarto render examples/demo.ipynb --execute` and updates the freeze results in `_freeze/`. Commit the updated freeze output alongside your changes.

## Updating the theme

The theme is vendored at `_extensions/surrogate-sci/ss-pub-theme/`. Make deliberate, reviewed changes there and render both supported profiles before merging. There is no automatic upstream theme updater.

## Testing changes

Before opening a PR, run through this checklist:

1. `make preview` — site renders without errors and your changes look correct.
2. `make execute-demo` — the demo notebook executes and renders successfully.
3. `make pre-commit` — all pre-commit hooks pass (linting, formatting, etc.).
