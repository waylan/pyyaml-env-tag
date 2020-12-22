# pyyaml_env_tag

A custom YAML tag for referencing environment variables in YAML files.

[![PyPI Version][pypi-image]][pypi-link]
[![Build Status][GHAction-image]][GHAction-link]
[![Coverage Status][codecov-image]][codecov-link]

[pypi-image]: https://img.shields.io/pypi/v/pyyaml-env-tag.svg
[pypi-link]: https://pypi.org/project/pyyaml-env-tag/
[GHAction-image]: https://github.com/waylan/pyyaml-env-tag/workflows/CI/badge.svg?branch=master&event=push
[GHAction-link]: https://github.com/waylan/pyyaml-env-tag/actions?query=event%3Apush+branch%3Amaster
[codecov-image]: https://codecov.io/github/waylan/pyyaml-env-tag/coverage.svg?branch=master
[codecov-link]: https://codecov.io/github/waylan/pyyaml-env-tag?branch=master

## Installation

Install `PyYAML` and the `pyyaml_env_tag` package with pip:

```bash
pip install pyyaml pyyaml_env_tag
```

### Enabling the tag

To enable the tag, import and add the `construct_env_tag` constructor to your YAML
loader of choice.

```python
import yaml
from yaml_env_tag import construct_env_tag

yaml.Loader.add_constructor('!ENV', construct_env_tag)
```

Then you may use the loader as per usual. For example:

```python
yaml.load(data, Loader=yaml.Loader)
```

## Using the tag

Include the tag `!ENV` followed by the name of an environment variable in a YAML
file and the value of the environment variable will be used in its place.

```yaml
key: !ENV SOME_VARIABLE
```

If `SOME_VARIABLE` is set to `A string!`, then the above YAML would result in the
following Python object:

```python
{'key': 'A string!'}
```

The content of the variable is parsed using YAML's implicit scalar types, such as
string, bool, integer, float, datestamp and null. More complex types are not
recognized and simply passed through as a string. For example, if `SOME_VARIABLE`
was set to the string `true`, then the above YAML would result in the following:

```python
{'key': True}
```

If the variable specified is not set, then a `null` value is assigned as a default.
You may define your own default as the last item in a sequence.

```yaml
key: !ENV [SOME_VARIABLE, default]
```

In the above example, if `SOME_VARIABLE` is not defined, the string `default` would
be used instead, as follows:

```python
{'key': 'default'}
```

You may list multiple variables as fallbacks. The first variable which is set is
used. In any sequance with more than one item, the last item must always be a
default value and will not be resolved as an environment variable.

```yaml
key: !ENV [SOME_VARIABLE, FALLBACK, default]
```

As with variable contents, the default is resolved to a Python object of the
implied type (string, bool, integer, float, datestamp and null).

When `SOME_VARIABLE` is not set, all four of the following items will resolve to
the same value (`None`):

```yaml
- !ENV SOME_VARIABLE
- !ENV [SOME_VARIABLE]
- !ENV [SOME_VARIABLE, ~]
- !ENV [SOME_VARIABLE, null]
```

## Related

pyyaml_env_tag was inspired by the Ruby package [yaml-env-tag].

An alternate method of referencing environment variables in YAML files is
implemented by [pyyaml-tags] and [python_yaml_environment_variables].
Each of those libraries use a template string and replace the template tag with
the content of the variable. While this allows a single value to reference
multiple variables and to contain additional content, it restricts all values
to strings only and does not provide a way to define defaults.

[yaml-env-tag]: https://github.com/jirutka/yaml-env-tag
[pyyaml-tags]: https://github.com/meiblorn/pyyaml-tags
[python_yaml_environment_variables]: https://gist.github.com/mkaranasou/ba83e25c835a8f7629e34dd7ede01931

## License

pyyaml_env_tag is licensed under the [MIT License] as defined in `LICENSE`.

[MIT License]: https://opensource.org/licenses/MIT

## Changelog

### Version 0.1 (released 2020-11-11)

The initial release.
