# Contributing

Contributions to the [BridgeMap App] <https://github.com/austin-shih/BridgeMap>  are welcome, and any feedback, input, or bug reports are greatly appreciated! Every little bit helps, and credit will always be given.

## Types of Contributions

### Report Bugs

If you are reporting a bug, please open an issue and include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

You can never have enough documentation! Please feel free to contribute to any
part of the documentation, such as the official docs, docstrings, or even
on the web in blog posts, articles, and such.

### Submit Feedback

We are open to ideas and recommendations of enhancements to our app platform:

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome!

## Get Started

Ready to contribute? Here's how to set up `BridgeMap` for local development.

1. Fork the [BridgeMap] <https://github.com/austin-shih/BridgeMap> repo on GitHub.

2. Clone your fork and use `git` (or similar) to create a development branch:
    ```console
    git switch -c name-of-your-bugfix-or-feature
    ```

3. Create conda environment and activate it
    ``` console
    conda env create -f bridgemap.yaml
    conda bridgemap
    ```
4. The `app.py` scipt contains the dashboard scripts in `plotly dash`.

5. Start contributing! The [Plotly Dash Python User Guide](https://dash.plotly.com/) is a great online resource for reference.

6. Commit your changes and open a pull request.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include additional tests if appropriate.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for all currently supported operating systems and versions of Python.

## Code of Conduct

Please note that the `BridgeMap` project is released with a
Code of Conduct. By contributing to this project you agree to abide by its terms.

## Attribution

These contribution guidelines were adapted from the [Cookiecutter Repository contribution file](https://github.com/cookiecutter/cookiecutter/blob/main/CONTRIBUTING.md).
