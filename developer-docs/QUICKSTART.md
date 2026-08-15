## Quick Start

1. **Create a repo from this template**

    In the top-right of this GitHub repo, select the green button that says "*Use this template*".

    Leave *Include all branches* unchecked. The publication workflows create the `publish` and `gh-pages` branches when they are needed, so a new publication should begin from `main` only.

2. **Configure your publication**

    * Replace the variables in `_variables.yml`
      - The `google_analytics_id` field can be left blank during development, but should be populated before publishing. See the [Publishing Guide](PUBLISHING_GUIDE.md) for more details.
    * Feel free to edit the variables in `authors.yml`.
      - Replace the example author information with the people and contributor roles for your publication before release.

3. **Install Quarto**

    The publication is rendered with [Quarto](https://quarto.org/). If you don't have it installed (check with `quarto --version`), you can [install it here](https://quarto.org/docs/get-started/).

4. **Set up your environment**

    See the [Environment Setup Guide](ENVIRONMENT_SETUP.md) for complete instructions.

5. **Choose a publication theme**

    Warm Journal is the default theme:

    ```bash
    make preview-warm
    ```

    To use the Technical Notebook theme instead:

    ```bash
    make preview-technical
    ```

    The matching render commands are `make render-warm` and `make render-technical`. In CI, set `QUARTO_PROFILE=technical-notebook` to select the technical theme.

6. **Prepare publication metadata**

    Before release, replace the placeholders in `CITATION.cff`, `authors.yml`, `_variables.yml`, and `README.md` with accurate publication details.

7. **Create your publication**

    Edit `index.ipynb` to create your publication. As you work, you can render a live preview of your changes with:

    ```bash
    make preview
    ```

    Then, commit your changes to a development branch and merge them into `main` using our usual PR-based workflow.

    As you work, please be careful to avoid modifying any files in the following directories:

      - `/_extensions` (Quarto extensions)
      - `/_freeze` (Generated execution results)
      - `/_site` (Generated website files)

    These files are all either necessary to build the publication or are automatically generated during the publication process.

8. **Publishing**

    See the [Publishing Guide](PUBLISHING_GUIDE.md) for complete instructions on the publishing process.
