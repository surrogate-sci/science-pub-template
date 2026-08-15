# GitHub Actions

The repository has one publishing workflow: `.github/workflows/publish.yml`.

## Quarto Publish

The workflow runs on every push to `main` and can also be started manually. It:

1. checks out the current `main` revision;
2. creates the generated `gh-pages` branch when necessary;
3. installs the supported Quarto version;
4. renders the publication; and
5. pushes the generated site to `gh-pages`.

GitHub Pages then deploys the contents of `gh-pages`. The rendered `_site` directory is not committed to `main`.

Repository administrators must grant GitHub Actions read/write workflow permissions so the publishing action can update `gh-pages`.

## Reproducible computation

The workflow renders committed source and frozen outputs; it does not recreate an author's complete scientific environment. Execute notebooks locally in the pinned project environment, inspect the results, and commit the relevant notebook and `_freeze` updates before merging.

Use Git tags and GitHub releases for versioned scholarly releases. Release management is independent of the Pages deployment workflow.
