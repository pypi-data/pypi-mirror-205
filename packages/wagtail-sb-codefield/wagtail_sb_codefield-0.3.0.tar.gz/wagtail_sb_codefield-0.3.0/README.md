![Community-Project](https://gitlab.com/softbutterfly/open-source/open-source-office/-/raw/master/banners/softbutterfly-open-source--banner--community-project.png)

![PyPI - Supported versions](https://img.shields.io/pypi/pyversions/wagtail-sb-codefield)
![PyPI - Package version](https://img.shields.io/pypi/v/wagtail-sb-codefield)
![PyPI - Downloads](https://img.shields.io/pypi/dm/wagtail-sb-codefield)
![PyPI - MIT License](https://img.shields.io/pypi/l/wagtail-sb-codefield)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/2f6661a360234960b1800c0bdac37d3c)](https://app.codacy.com/gl/softbutterfly/wagtail-sb-codefield/dashboard?utm_source=gl&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

# Wagtail CodeField

Use CodeField from [`django-sb-codefield`](https://gitlab.com/softbutterfly/open-source/django-sb-codefield) in Wagtail Admin

## Requirements

- Python 3.8.1 or higher but lower than 4.0.0
- Django lower than 4.0.0
- Wagtail lower than 4.0.0
- django-sb-codefield lower than 1.0.0

## Install

```bash
pip install wagtail-sb-codefield
```

## Usage

Add `wagtail_sb_codefield`, `django_sb_codefield` and `codemirror2` to your `INSTALLED_APPS` settings

```
INSTALLED_APPS = [
  # ...
  "codemirror2",
  "django_sb_codefield",
  "wagtail_sb_codefield",
]
```

## Docs

- [Ejemplos](https://gitlab.com/softbutterfly/open-source/wagtail-sb-codefield/-/wikis)
- [Wiki](https://gitlab.com/softbutterfly/open-source/wagtail-sb-codefield/-/wikis)

## Changelog

All changes to versions of this library are listed in the [change history](CHANGELOG.md).

## Development

Check out our [contribution guide](CONTRIBUTING.md).

## Contributors

See the list of contributors [here](https://gitlab.com/softbutterfly/open-source/wagtail-sb-codefield/-/graphs/develop).
