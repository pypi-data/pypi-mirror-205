# Poetry Git Version Plugin

Poetry plugin to get package version from git.

## Functionality

- Git tag parsing
- Make alpha version
- Substitution of the project tag (if any) in the poetry.version value
- Maintenance of PEP 440
- Command to output a new version

## Quick start

```bash
poetry self add poetry-git-version-plugin
poetry git-version # Write your git tag
poetry -v git-version # print process
```

## Dependencies

Installed `Git` and:

```toml
[tool.poetry.dependencies]
python = ">=3.8"
poetry = ">=1.2.0"
```

## Setup

```toml
[tool.poetry-git-version-plugin]
# If the tag is not found on the HEAD,
# then the version is built based on the last found tag and the HEAD
# Example: 1.3.2a5
# Default = true
make_alpha_version = true

# Format for alpha version
# Default = '{version}a{distance}'
# Example:
alpha_version_format = '{version}+{distance}' # -> 1.3.2a5
alpha_version_format = '{version}a{distance}+{commit_hash}' # -> 1.3.2a5-5babef6
# Available variables:
# - version: Last found tag
# - distance: Distance from last found tag to HEAD
# - commit_hash: Commit hash

# Ignore mismatch error PEP440 version format
# Default = true
ignore_pep440 = true

# Ignore mismatch error PEP440 public version format
# Default = true
ignore_public_pep440 = true

# Ignore all errors
# including version not found errors
ignore_errors = true
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/poetry-git-version-plugin/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/poetry-git-version-plugin>

Before adding changes:

```bash
make install
```

After changes:

```bash
make format test
```
