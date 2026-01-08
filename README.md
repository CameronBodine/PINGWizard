# PINGWizard
Light-weight interface for running PING ecosystem (PINGMapper, etc.)

- Update flow auto-updates `pinginstaller` in the base environment before applying PINGMapper updates, preventing nested env creation and ensuring the main `ping` environment stays current.

## Verbosity
- Default: Updates run with maximum verbosity (debug) when triggered from the wizard.
- Quiet mode: Set environment variable `PINGINSTALLER_VERBOSITY=quiet` before launching PINGWizard to suppress extra solver output, or use `python -m pinginstaller -q` when running from the terminal.

[![PyPI - Version](https://img.shields.io/pypi/v/pingwizard?style=flat-square&label=Latest%20Version%20(PyPi))](https://pypi.org/project/pingwizard/)
