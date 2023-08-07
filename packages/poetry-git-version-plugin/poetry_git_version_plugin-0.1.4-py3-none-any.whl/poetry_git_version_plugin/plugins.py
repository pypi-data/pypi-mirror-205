from __future__ import annotations

from cleo.io.io import IO
from cleo.io.outputs.output import Verbosity
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry

from poetry_git_version_plugin import config
from poetry_git_version_plugin.commands import GitVersionCommand
from poetry_git_version_plugin.exceptions import PluginException, plugin_exception_wrapper
from poetry_git_version_plugin.services import GitVersionService
from poetry.core.constraints.version import Version


class PoetryGitVersionPlugin(Plugin):
    """Плагин определения версии по гит тегу"""

    @plugin_exception_wrapper
    def activate(self, poetry: Poetry, io: IO):
        io.write_line(f'<b>{config.PLUGIN_NAME}</b>: Init', Verbosity.VERBOSE)

        plugin_config = config.PluginConfig(poetry.pyproject)

        try:
            version = GitVersionService(io, plugin_config).get_version()
            poetry.package.version = Version.parse(version)

        except Exception as ex:
            if plugin_config.ignore_errors:
                if not isinstance(ex, PluginException):
                    ex = PluginException(ex)

                io.write_error_line(f'{ex}. Ignore Exception\n', Verbosity.VERBOSE)

                return

            raise ex

        io.write_error_line(f'<b>{config.PLUGIN_NAME}</b>: Finished\n', Verbosity.VERBOSE)


class PoetryGitVersionApplicationPlugin(ApplicationPlugin):
    commands = [GitVersionCommand]
