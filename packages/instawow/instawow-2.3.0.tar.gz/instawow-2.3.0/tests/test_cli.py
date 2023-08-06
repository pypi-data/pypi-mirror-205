from __future__ import annotations

import asyncio
import json
import shutil
from collections.abc import Callable as C
from functools import partial
from textwrap import dedent
from unittest import mock

import pytest
from click.testing import CliRunner, Result
from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from instawow import __version__
from instawow.cli import cli
from instawow.config import Config


@pytest.fixture(autouse=True, scope='module')
def __mock_pt_progress_bar():
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr('prompt_toolkit.shortcuts.progress_bar.ProgressBar', mock.MagicMock())
    yield
    monkeypatch.undo()


@pytest.fixture
def feed_pt():
    with create_pipe_input() as input_, create_app_session(input=input_, output=DummyOutput()):
        yield input_.send_text


@pytest.fixture
def run(
    monkeypatch: pytest.MonkeyPatch,
    event_loop: asyncio.AbstractEventLoop,
    iw_config: Config,
):
    monkeypatch.setattr('asyncio.run', event_loop.run_until_complete)
    return partial(CliRunner().invoke, cli, catch_exceptions=False)


@pytest.fixture
def install_molinari_and_run(
    run: C[[str], Result],
):
    run('install curse:molinari')
    return run


@pytest.fixture
def pretend_install_molinari_and_run(
    iw_config: Config,
    run: C[[str], Result],
):
    molinari = iw_config.addon_dir / 'Molinari'
    molinari.mkdir()
    (molinari / 'Molinari.toc').write_text(
        '''\
## X-Curse-Project-ID: 20338
## X-WoWI-ID: 13188
'''
    )
    return run


@pytest.mark.parametrize(
    'alias',
    [
        'curse:molinari',
        'wowi:13188-molinari',
        'tukui:1',
        'github:p3lim-wow/Molinari',
    ],
)
def test_valid_pkg_lifecycle(
    run: C[[str], Result],
    alias: str,
):
    assert run(f'install {alias}').output.startswith(f'✓ {alias}\n  installed')
    assert run(f'install {alias}').output == f'✗ {alias}\n  package already installed\n'
    assert run(f'update {alias}').output == f'✗ {alias}\n  package is up to date\n'
    assert run(f'remove {alias}').output == f'✓ {alias}\n  removed\n'
    assert run(f'update {alias}').output == f'✗ {alias}\n  package is not installed\n'
    assert run(f'remove {alias}').output == f'✗ {alias}\n  package is not installed\n'


@pytest.mark.parametrize('alias', ['curse:gargantuan-wigs'])
def test_nonexistent_pkg_lifecycle(
    run: C[[str], Result],
    alias: str,
):
    assert run(f'install {alias}').output == f'✗ {alias}\n  package does not exist\n'
    assert run(f'update {alias}').output == f'✗ {alias}\n  package is not installed\n'
    assert run(f'remove {alias}').output == f'✗ {alias}\n  package is not installed\n'


@pytest.mark.parametrize('alias', ['foo:bar'])
def test_invalid_source_lifecycle(
    run: C[[str], Result],
    alias: str,
):
    assert run(f'install {alias}').output == f'✗ {alias}\n  package source is invalid\n'
    assert run(f'update {alias}').output == f'✗ {alias}\n  package is not installed\n'
    assert run(f'remove {alias}').output == f'✗ {alias}\n  package is not installed\n'


def test_reconciled_folder_conflict_on_install(
    run: C[[str], Result],
):
    assert run('install curse:molinari').output.startswith('✓ curse:molinari\n  installed')
    assert run('install wowi:13188-molinari').output == (
        '✗ wowi:13188-molinari\n'
        '  package folders conflict with installed package Molinari\n'
        '    (curse:20338)\n'
    )


def test_unreconciled_folder_conflict_on_install(
    iw_config: Config,
    run: C[[str], Result],
):
    iw_config.addon_dir.joinpath('Molinari').mkdir()
    assert (
        run('install curse:molinari').output
        == "✗ curse:molinari\n  package folders conflict with 'Molinari'\n"
    )
    assert run('install --replace curse:molinari').output.startswith(
        '✓ curse:molinari\n  installed'
    )


def test_keep_folders_on_remove(
    iw_config: Config,
    install_molinari_and_run: C[[str], Result],
):
    assert (
        install_molinari_and_run('remove --keep-folders curse:molinari').output
        == '✓ curse:molinari\n  removed\n'
    )
    assert iw_config.addon_dir.joinpath('Molinari').is_dir()


def test_version_strategy_lifecycle(
    run: C[[str], Result],
):
    assert run('install curse:molinari').output.startswith(
        '✓ curse:molinari\n  installed 90200.82-Release'
    )
    assert (
        run('install --version foo curse:molinari').output
        == '✗ curse:molinari\n  package already installed\n'
    )
    assert run('update curse:molinari').output == '✗ curse:molinari\n  package is up to date\n'
    assert run('remove curse:molinari').output == '✓ curse:molinari\n  removed\n'
    assert run('install --version foo curse:molinari').output == dedent(
        '''\
        ✗ curse:molinari
          no files found for: any_flavour=None; any_release_type=None;
            version_eq='foo'
        '''
    )
    assert (
        run('install --version 80000.57-Release curse:molinari').output
        == '✓ curse:molinari\n  installed 80000.57-Release\n'
    )
    assert run('update').output == '✗ curse:molinari\n  package is pinned\n'
    assert run('update curse:molinari').output == '✗ curse:molinari\n  package is pinned\n'
    assert run('remove curse:molinari').output == '✓ curse:molinari\n  removed\n'


def test_install_options(
    run: C[[str], Result],
):
    assert run(
        'install' ' --any-release-type' ' --any-flavour' ' curse:molinari'
    ).output == dedent(
        '''\
        ✓ curse:molinari
          installed 90200.82-Release
        '''
    )


@pytest.mark.parametrize('step', [1, -1])
def test_install_order_is_stable(
    run: C[[str], Result],
    step: int,
):
    assert run(
        'install '
        + ' '.join(
            (
                'curse:molinari',
                '--version 80000.57-Release curse:molinari',
            )[::step]
        )
    ).output == dedent(
        '''\
        ✓ curse:molinari
          installed 80000.57-Release
        ✗ curse:molinari
          package folders conflict with installed package Molinari
            (curse:20338)
        '''
    )


def test_install_argument_is_optional(
    run: C[[str], Result],
):
    assert run('install --version 80000.57-Release curse:molinari').output == dedent(
        '''\
        ✓ curse:molinari
          installed 80000.57-Release
        '''
    )


def test_install_invalid_defn(
    run: C[[str], Result],
):
    result = run('install foo')
    assert result.exit_code == 2
    assert result.output.endswith("Error: Invalid value for '[ADDONS]...': foo\n")


def test_configure__show_active_profile(
    iw_config: Config,
    run: C[[str], Result],
):
    assert run('configure --show-active').output == iw_config.encode_for_display() + '\n'


@pytest.mark.parametrize('command', ['configure', 'list'], ids=['explicit', 'implicit'])
def test_configure__create_new_profile(
    feed_pt: C[[str], None],
    iw_config: Config,
    run: C[[str], Result],
    command: str,
):
    feed_pt(f'{iw_config.addon_dir}\r\rY\r')
    assert run(f'-p foo {command}').output == (
        'Navigate to https://github.com/login/device and paste the code below:\n'
        '  WDJB-MJHT\n'
        'Waiting...\n'
        'Configuration written to:\n'
        f'  {iw_config.global_config.config_dir / "config.json"}\n'
        f'  {iw_config.global_config.config_dir / "profiles/foo/config.json"}\n'
    )


def test_configure__update_existing_profile_interactively(
    feed_pt: C[[str], None],
    iw_config: Config,
    run: C[[str], Result],
):
    feed_pt('Y\r')
    assert run('configure global_config.auto_update_check').output == (
        'Configuration written to:\n'
        f'  {iw_config.global_config.config_dir / "config.json"}\n'
        f'  {iw_config.global_config.config_dir / "profiles/__default__/config.json"}\n'
    )


def test_configure__update_existing_profile_directly(
    iw_config: Config,
    run: C[[str], Result],
):
    assert run('configure global_config.auto_update_check=0').output == (
        'Configuration written to:\n'
        f'  {iw_config.global_config.config_dir / "config.json"}\n'
        f'  {iw_config.global_config.config_dir / "profiles/__default__/config.json"}\n'
    )


@pytest.mark.parametrize('options', ['', '--undo'])
def test_rollback__pkg_not_installed(
    run: C[[str], Result],
    options: str,
):
    assert (
        run(f'rollback {options} curse:molinari').output
        == '✗ curse:molinari\n  package is not installed\n'
    )


@pytest.mark.parametrize('options', ['', '--undo'])
def test_rollback__unsupported(
    run: C[[str], Result],
    options: str,
):
    assert run('install wowi:13188-molinari').exit_code == 0
    assert (
        run(f'rollback {options} wowi:13188-molinari').output
        == '✗ wowi:13188-molinari\n  strategies are not valid for source: version_eq\n'
    )


def test_rollback__single_version(
    run: C[[str], Result],
):
    assert run('install curse:molinari').exit_code == 0
    assert (
        run('rollback curse:molinari').output == '✗ curse:molinari\n  cannot find older versions\n'
    )


def test_rollback__multiple_versions(
    feed_pt: C[[str], None],
    run: C[[str], Result],
):
    assert run('install --version 80000.57-Release curse:molinari').exit_code == 0
    assert run('remove curse:molinari').exit_code == 0
    assert run('install curse:molinari').exit_code == 0
    feed_pt('\r\r')
    assert run('rollback curse:molinari').output == dedent(
        '''\
        ✓ curse:molinari
          updated 90200.82-Release to 80000.57-Release
        '''
    )


def test_rollback__multiple_versions_promptless(
    run: C[[str], Result],
):
    assert run('install --version 80000.57-Release curse:molinari').exit_code == 0
    assert run('remove curse:molinari').exit_code == 0
    assert run('install curse:molinari').exit_code == 0
    assert run('rollback --version 80000.57-Release curse:molinari').output == dedent(
        '''\
        ✓ curse:molinari
          updated 90200.82-Release to 80000.57-Release
        '''
    )


@pytest.mark.parametrize('options', ['', '--undo'])
def test_rollback__rollback_multiple_versions(
    feed_pt: C[[str], None],
    run: C[[str], Result],
    options: str,
):
    assert run('install curse:molinari').exit_code == 0
    assert run('remove curse:molinari').exit_code == 0
    assert run('install --version 80000.57-Release curse:molinari').exit_code == 0
    feed_pt('\r\r')
    assert run(f'rollback {options} curse:molinari').output == dedent(
        '''\
        ✓ curse:molinari
          updated 80000.57-Release to 90200.82-Release
        '''
    )


def test_rollback__cannot_use_version_with_undo(
    run: C[[str], Result],
):
    result = run('rollback --version foo --undo curse:molinari')
    assert result.exit_code == 2
    assert 'Cannot use "--version" with "--undo"' in result.output


def test_reconcile__list_unreconciled(
    pretend_install_molinari_and_run: C[[str], Result],
):
    assert pretend_install_molinari_and_run('reconcile --list-unreconciled').output == (
        # fmt: off
        'unreconciled\n'
        '------------\n'
        'Molinari    \n'
        # fmt: on
    )


def test_reconcile_leftovers(
    feed_pt: C[[str], None],
    pretend_install_molinari_and_run: C[[str], Result],
):
    feed_pt('sss')  # Skip
    assert pretend_install_molinari_and_run('reconcile').output.endswith(
        # fmt: off
        'unreconciled\n'
        '------------\n'
        'Molinari    \n'
        # fmt: on
    )


def test_reconcile__auto_reconcile(
    pretend_install_molinari_and_run: C[[str], Result],
):
    assert pretend_install_molinari_and_run('reconcile --auto').output == dedent(
        '''\
        ✓ curse:molinari
          installed 90200.82-Release
        '''
    )


def test_reconcile__abort_interactive_reconciliation(
    feed_pt: C[[str], None],
    pretend_install_molinari_and_run: C[[str], Result],
):
    feed_pt('\x03')  # ^C
    assert pretend_install_molinari_and_run('reconcile').output.endswith('Aborted!\n')


def test_reconcile__complete_interactive_reconciliation(
    feed_pt: C[[str], None],
    pretend_install_molinari_and_run: C[[str], Result],
):
    feed_pt('\r\r')
    assert pretend_install_molinari_and_run('reconcile').output.endswith(
        dedent(
            '''\
            ✓ curse:molinari
              installed 90200.82-Release
            '''
        )
    )


def test_reconcile__reconciliation_complete(
    run: C[[str], Result],
):
    assert run('reconcile').output == 'No add-ons left to reconcile.\n'


def test_reconcile__rereconcile(
    feed_pt: C[[str], None],
    install_molinari_and_run: C[[str], Result],
):
    feed_pt('\r\r')
    assert install_molinari_and_run('reconcile --installed').output == dedent(
        '''\
        ✓ curse:molinari
          removed
        ✓ github:p3lim-wow/molinari
          installed 90200.82-Release
        '''
    )


def test_reconcile__cannot_use_auto_with_installed(
    run: C[[str], Result],
):
    result = run('reconcile --auto --installed')
    assert result.exit_code == 2
    assert 'Cannot use "--auto" with "--installed"' in result.output


def test_search__no_results(
    run: C[[str], Result],
):
    assert run('search ∅').output == 'No results found.\n'


def test_search__exit_without_selecting(
    feed_pt: C[[str], None],
    run: C[[str], Result],
):
    feed_pt('\r')  # enter
    assert run('search molinari').output == ''


def test_search__exit_after_selection(
    feed_pt: C[[str], None],
    run: C[[str], Result],
):
    feed_pt(' \rn')  # space, enter, "n"
    assert run('search molinari').output == ''


def test_search__install_one(
    feed_pt: C[[str], None],
    run: C[[str], Result],
):
    feed_pt(' \r\r')  # space, enter, enter
    assert run('search molinari --source curse').output == dedent(
        '''\
        ✓ curse:molinari
          installed 90200.82-Release
        '''
    )


def test_search__install_multiple_conflicting(
    feed_pt: C[[str], None],
    run: C[[str], Result],
):
    feed_pt(' \x1b[B \r\r')  # space, arrow down, space, enter, enter
    assert run('search molinari').output == dedent(
        '''\
        ✓ wowi:13188-molinari
          installed 90200.82-Release
        ✗ curse:molinari
          package folders conflict with installed package Molinari
            (wowi:13188)
        '''
    )


def test_changelog_output(
    install_molinari_and_run: C[[str], Result],
):
    output = (
        'Changes in 90200.82-Release:'
        if shutil.which('pandoc')
        else '<h3>Changes in 90200.82-Release:</h3>'
    )
    assert install_molinari_and_run('view-changelog curse:molinari').output.startswith(output)


def test_changelog_output_no_convert(
    install_molinari_and_run: C[[str], Result],
):
    assert install_molinari_and_run(
        'view-changelog --no-convert curse:molinari'
    ).output.startswith('<h3>Changes in 90200.82-Release:</h3>')


def test_argless_changelog_output(
    install_molinari_and_run: C[[str], Result],
):
    output = (
        'curse:molinari:\n  Changes in 90200.82-Release:'
        if shutil.which('pandoc')
        else 'curse:molinari:\n  <h3>Changes in 90200.82-Release:</h3>'
    )
    assert install_molinari_and_run('view-changelog').output.startswith(output)


def test_argless_changelog_output_no_convert(
    install_molinari_and_run: C[[str], Result],
):
    assert install_molinari_and_run('view-changelog --no-convert').output.startswith(
        'curse:molinari:\n  <h3>Changes in 90200.82-Release:</h3>'
    )


@pytest.mark.parametrize(
    ('command', 'exit_code'),
    [
        ('list mol', 0),
        ('info foo', 0),
        ('reveal mol', 0),
        ('reveal foo', 1),
    ],
)
def test_exit_codes_with_substr_match(
    monkeypatch: pytest.MonkeyPatch,
    install_molinari_and_run: C[[str], Result],
    command: str,
    exit_code: int,
):
    monkeypatch.setattr('instawow.cli.reveal_folder', lambda *_, **__: ...)
    assert install_molinari_and_run(command).exit_code == exit_code


def test_can_list_with_substr_match(
    install_molinari_and_run: C[[str], Result],
):
    assert install_molinari_and_run('list mol').output == 'curse:molinari\n'
    assert install_molinari_and_run('list foo').output == ''
    assert install_molinari_and_run('list -f detailed mol').output.startswith('curse:molinari')
    (molinari,) = json.loads(install_molinari_and_run('list -f json mol').output)
    assert (molinari['source'], molinari['slug']) == ('curse', 'molinari')


def test_json_export(
    install_molinari_and_run: C[[str], Result],
):
    output = install_molinari_and_run('list -f json').output
    assert json.loads(output)[0]['name'] == 'Molinari'


def test_show_version(
    run: C[[str], Result],
):
    assert run('--version').output == f'instawow, version {__version__}\n'


def test_plugin_hook_command_can_be_invoked(
    run: C[[str], Result],
):
    pytest.importorskip('instawow_test_plugin')
    assert run('foo').output == 'success!\n'
