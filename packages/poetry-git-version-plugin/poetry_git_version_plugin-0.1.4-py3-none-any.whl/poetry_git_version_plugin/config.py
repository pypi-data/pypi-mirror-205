from copy import deepcopy

from poetry.core.pyproject.toml import PyProjectTOML

PLUGIN_NAME = 'poetry-git-version-plugin'


class PluginConfig(object):
    """Обертка над конфигурацией pyproject"""

    pyproject: PyProjectTOML

    _default_setting = {
        # Игнорирование отсутствия тега
        'ignore_errors': True,
        # При отсутствии тега генерировать alpha version
        'make_alpha_version': True,
        # Alpha Version Format
        'alpha_version_format': '{version}a{distance}',
        # 'alpha_version_format': '{version}a{distance}+{commit_hash}',
        # Ignore PEP440
        'ignore_pep440': True,
        # Ignore public format PEP440
        'ignore_public_pep440': True,
    }

    def __init__(self, pyproject: PyProjectTOML) -> None:
        self.pyproject = pyproject

    @property
    def settings(self):
        settings = self.pyproject.data.get('tool', {}).get(PLUGIN_NAME, {})
        new_settings = deepcopy(self._default_setting)
        new_settings.update(settings)
        return new_settings

    @property
    def ignore_errors(self) -> bool:
        return self.settings['ignore_errors']

    @property
    def make_alpha_version(self) -> bool:
        return self.settings['make_alpha_version']

    @property
    def alpha_version_format(self) -> str:
        return self.settings['alpha_version_format']

    @property
    def ignore_pep440(self) -> bool:
        return self.settings['ignore_pep440']

    @property
    def ignore_public_pep440(self) -> bool:
        return self.settings['ignore_public_pep440']
