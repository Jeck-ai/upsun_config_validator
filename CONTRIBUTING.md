# Contributing

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

- [Types of Contributions](#types-of-contributions)
- [Contributor Setup](#setting-up-the-code-for-local-development)
- [Contributor Guidelines](#contributor-guidelines)
- [Contributor Testing](#testing-with-tox)
- [Core Committer Guide](#core-committer-guide)

## Types of Contributions

You can contribute in many ways:

### Report Bugs

Report bugs at [https://github.com/Jeck-ai/upsun_config_validator/issues](https://github.com/Jeck-ai/upsun_config_validator/issues).

If you are reporting a bug, please complete the issue template and include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- If you can, provide detailed steps to reproduce the bug.
- If you don't have steps to reproduce the bug, just note your observations in as much detail as you can.
  Questions to start a discussion about the issue are welcome.

### Fix Bugs

Look through the GitHub issues for bugs.
Anything tagged with the "bug" label is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features.
Anything tagged with "enhancement" and "please-help" is open to whoever wants to implement it.

Please do not combine multiple feature enhancements into a single pull request.

### Write Documentation

Upsun Validator could always use more documentation, whether as part of the official Cookiecutter docs, in docstrings, or even on the web in blog posts, articles, and such.

<!-- If you want to review your changes on the documentation locally, you can do:

```bash
pip install -r docs/requirements.txt
make servedocs
```

This will compile the documentation, open it in your browser and start watching the files for changes, recompiling as you save. -->

### Submit Feedback

The best way to send feedback is to file an issue at [https://github.com/Jeck-ai/upsun_config_validator/issues](https://github.com/Jeck-ai/upsun_config_validator/issues).

If you are proposing a feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Setting Up the Code for Local Development

Here's how to set up `upsunvalidator` for local development.

1. Fork the `upsunvalidator` repo on GitHub.
2. Clone your fork locally:

   ```bash
   git clone git@github.com:your_name_here/upsunvalidator.git
   ```

3. Install your local copy into a virtualenv.
   Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development:

   ```bash
   cd upsunvalidator
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -e .
   ```

   As you make changes to core, you will likely need to run `pip install -e .` again to test your revisions.

4. Create a branch for local development:

   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```

Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests and lint check:

   ```bash
   pytest
   ```

<!-- 6. Ensure that your feature or commit is fully covered by tests. Check report after regular `tox` run.
   You can also run coverage only report and get html report with statement by statement highlighting:

   ```bash
   make coverage
   ```

   You report will be placed to `htmlcov` directory. Please do not include this directory to your commits.
   By default this directory in our `.gitignore` file. -->

6. Commit your changes and push your branch to GitHub:

   ```bash
   git add .
   git commit -m "Your detailed description of your changes."
   git push origin name-of-your-bugfix-or-feature
   ```

8. Submit a pull request through the GitHub website.

## Contributor Guidelines

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. The pull request should be contained:
   if it's too big consider splitting it into smaller pull requests.
3. If the pull request adds functionality, the docs should be updated.
   Put your new functionality into a function with a docstring, and add the feature to the list in README.md.
4. The pull request must pass all CI/CD jobs before being ready for review.
5. If one CI/CD job is failing for unrelated reasons you may want to create another PR to fix that first.

<!-- ### Coding Standards

- PEP8
- Functions over classes except in tests
- Quotes via [http://stackoverflow.com/a/56190/5549](http://stackoverflow.com/a/56190/5549)

  - Use double quotes around strings that are used for interpolation or that are natural language messages
  - Use single quotes for small symbol-like strings (but break the rules if the strings contain quotes)
  - Use triple double quotes for docstrings and raw string literals for regular expressions even if they aren't needed.
  - Example:

    ```python
    LIGHT_MESSAGES = {
        'English': "There are %(number_of_lights)s lights.",
        'Pirate':  "Arr! Thar be %(number_of_lights)s lights."
    }
    def lights_message(language, number_of_lights):
        """Return a language-appropriate string reporting the light count."""
        return LIGHT_MESSAGES[language] % locals()
    def is_pirate(message):
        """Return True if the given message sounds piratical."""
        return re.search(r"(?i)(arr|avast|yohoho)!", message) is not None
    ```

## Testing with tox

`tox` uses `pytest` under the hood, hence it supports the same syntax for selecting tests.

For further information please consult the [pytest usage docs](http://pytest.org/en/latest/example/index.html).

To run a particular test class with `tox`:

```bash
tox -e py310 -- '-k TestFindHooks'
```

To run some tests with names matching a string expression:

```bash
tox -e py310 -- '-k generate'
```

Will run all tests matching "generate", test_generate_files for example.

To run just one method:

```bash
tox -e py310 -- '-k "TestFindHooks and test_find_hook"'
```

To run all tests using various versions of Python, just run `tox`:

```bash
tox
```

This configuration file setup the pytest-cov plugin and it is an additional dependency.
It generate a coverage report after the tests.

It is possible to test with specific versions of Python. To do this, the command is:

```bash
tox -e py37,py38
```

This will run `py.test` with the `python3.7` and `python3.8` interpreters. -->

