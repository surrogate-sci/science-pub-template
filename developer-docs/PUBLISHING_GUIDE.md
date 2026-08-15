# Publishing Guide

This template publishes its Quarto site to GitHub Pages whenever a change reaches `main`.

## Initial setup

1. In *Settings → Actions → General → Workflow permissions*, select **Read and write permissions**.
2. Replace the placeholders in `CITATION.cff`, `authors.yml`, `_variables.yml`, and `README.md`.
3. Render both supported profiles locally:

   ```bash
   make render-warm
   make render-technical
   ```

4. Merge the reviewed publication changes into `main`. The **Quarto Publish** workflow renders the default profile and pushes the generated site to `gh-pages`.
5. After the first successful run, verify that *Settings → Pages* uses **Deploy from a branch**, with `gh-pages` and `/ (root)` selected. GitHub normally detects the generated branch automatically.

The public project URL will normally be `https://<organization>.github.io/<repository>/`. A custom domain is optional and can be configured later in the repository's Pages settings.

## Publishing revisions

Merge each reviewed revision into `main`. GitHub Actions rebuilds the site automatically. Create a Git tag or GitHub release when you want a durable scholarly version, and connect the repository to Zenodo if the release should receive a DOI.

## Optional: enable comments with Giscus

Comments are disabled by default. Giscus stores page discussions in GitHub Discussions and requires a public repository.

1. Enable GitHub Discussions for the repository.
2. Install the [Giscus App](https://github.com/apps/giscus) for the repository.
3. Use the [Giscus configuration tool](https://giscus.app/) to obtain the repository and category identifiers.
4. Add the resulting configuration to `_quarto.yml`:

   ```yaml
   comments:
     giscus:
       repo: surrogate-sci/<repository>
       repo-id: <repository-id>
       category: Announcements
       category-id: <category-id>
       mapping: pathname
       input-position: top
       loading: lazy
   ```

Render locally and confirm the comment box loads without an error before publishing.

## Optional: enable analytics and cookie consent

Analytics and cookie consent are disabled by default. Do not enable a consent banner unless the publication actually loads analytics or another tracking service.

To use Google Analytics, add both settings under `website` in `_quarto.yml`:

```yaml
website:
  google-analytics: G-XXXXXXXXXX
  cookie-consent:
    type: express
    style: simple
```

Use an explicit consent model and update the publication's privacy information before release.
