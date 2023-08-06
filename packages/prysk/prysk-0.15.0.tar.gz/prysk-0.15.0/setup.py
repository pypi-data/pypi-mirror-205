# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prysk', 'pytest_prysk']

package_data = \
{'': ['*']}

install_requires = \
['rich>=13.3.1,<14.0.0']

extras_require = \
{'pytest-plugin': ['pytest>=7.0.1']}

entry_points = \
{'console_scripts': ['prysk = prysk:main'],
 'pytest11': ['prysk = pytest_prysk']}

setup_kwargs = {
    'name': 'prysk',
    'version': '0.15.0',
    'description': 'Functional tests for command line applications',
    'long_description': 'Prysk\n======================\n.. image:: https://img.shields.io/github/actions/workflow/status/nicoretti/prysk/verifier.yaml\n    :target: https://github.com/Nicoretti/prysk/actions\n\n.. image:: https://img.shields.io/coverallsCoverage/github/Nicoretti/prysk\n    :target: https://coveralls.io/github/Nicoretti/prysk\n\n.. image:: https://img.shields.io/badge/imports-isort-ef8336.svg\n    :target: https://pycqa.github.io/isort/\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n\n.. image:: https://img.shields.io/pypi/v/prysk\n    :target: https://pypi.org/project/prysk/\n\n.. image:: https://img.shields.io/badge/docs-available-blue.svg\n    :target: https://nicoretti.github.io/prysk/\n\nPrysk is a fork of the popular snapshot testing tool Cram_.\nEven though Cram_ is pretty complete and mature for everyday use,\nPrysk wants to continue pushing its development forward.\n\n.. _Cram: https://bitheap.org/cram\n\nPrysk tests look like snippets of interactive shell sessions. Prysk runs\neach command and compares the command output in the test with the\ncommand\'s actual output.\n\nHere\'s a snippet from `Prysk\'s own test suite`_:\n\n.. code-block:: console\n\n    Set up prysk alias and example tests:\n\n      $ . "$TESTDIR"/setup.sh\n\n    Usage:\n\n      $ prysk -h\n      [Uu]sage: prysk \\[OPTIONS\\] TESTS\\.\\.\\. (re)\n\n      [Oo]ptions: (re)\n        -h, --help          show this help message and exit\n        -V, --version       show version information and exit\n        -q, --quiet         don\'t print diffs\n        -v, --verbose       show filenames and test status\n        -i, --interactive   interactively merge changed test output\n        -d, --debug         write script output directly to the terminal\n        -y, --yes           answer yes to all questions\n        -n, --no            answer no to all questions\n        -E, --preserve-env  don\'t reset common environment variables\n        --keep-tmpdir       keep temporary directories\n        --shell=PATH        shell to use for running tests (default: /bin/sh)\n        --shell-opts=OPTS   arguments to invoke shell with\n        --indent=NUM        number of spaces to use for indentation (default: 2)\n        --xunit-file=PATH   path to write xUnit XML output\n\nThe format in a nutshell:\n\n* Prysk tests use the ``.t`` file extension.\n\n* Lines beginning with two spaces, a dollar sign (``$``), and a space are run\n  in the shell.\n\n* Lines beginning with two spaces, a greater than sign (``>``), and a space\n  allow multi-line commands.\n\n* All other lines beginning with two spaces are considered command\n  output.\n\n* Output lines ending with a space and the keyword ``(re)`` are\n  matched as `Perl-compatible regular expressions`_.\n\n* Lines ending with a space and the keyword ``(glob)`` are matched\n  with a glob-like syntax. The only special characters supported are\n  ``*`` and ``?``. Both characters can be escaped using ``\\``, and the\n  backslash can be escaped itself.\n\n* Output lines ending with either of the above keywords are always\n  first matched literally with actual command output.\n\n* Lines ending with a space and the keyword ``(no-eol)`` will match\n  actual output that doesn\'t end in a newline.\n\n* Actual output lines containing unprintable characters are escaped\n  and suffixed with a space and the keyword ``(esc)``. Lines matching\n  unprintable output must also contain the keyword.\n\n* Anything else is a comment.\n\n.. _Prysk\'s own test suite: https://github.com/Nicoretti/prysk/blob/master/test/integration/prysk/usage.t\n.. _Perl-compatible regular expressions: https://en.wikipedia.org/wiki/Perl_Compatible_Regular_Expressions\n\nUsage\n-----\n\nPrysk will print a dot for each passing test. If a test fails, a\n`unified context diff`_ is printed showing the test\'s expected output\nand the actual output. Skipped tests (empty tests and tests that exit\nwith return code ``80``) are marked with ``s`` instead of a dot.\n\nFor example, if we run Prysk on `its own example tests`_:\n\n.. code-block:: diff\n\n    .s.!\n    --- examples/fail.t\n    +++ examples/fail.t.err\n    @@ -3,21 +3,22 @@\n       $ echo 1\n       1\n       $ echo 1\n    -  2\n    +  1\n       $ echo 1\n       1\n\n     Invalid regex:\n\n       $ echo 1\n    -  +++ (re)\n    +  1\n\n     Offset regular expression:\n\n       $ printf \'foo\\nbar\\nbaz\\n\\n1\\nA\\n@\\n\'\n       foo\n    +  bar\n       baz\n\n       \\d (re)\n       [A-Z] (re)\n    -  #\n    +  @\n    s.\n    # Ran 6 tests, 2 skipped, 1 failed.\n\nPrysk will also write the test with its actual output to\n``examples/fail.t.err``, allowing you to use other diff tools. This\nfile is automatically removed the next time the test passes.\n\nWhen you\'re first writing a test, you might just write the commands\nand run the test to see what happens. If you run Prysk with ``-i`` or\n``--interactive``, you\'ll be prompted to merge the actual output back\ninto the test. This makes it easy to quickly prototype new tests.\n\nIs the same as invoking Prysk with ``--verbose`` and ``--indent=4``.\n\nNote that the following environment variables are reset before tests\nare run:\n\n* ``TMPDIR``, ``TEMP``, and ``TMP`` are set to the test runner\'s\n  ``tmp`` directory. In test output, occurrences of this directory are\n  replaced by ``$TMPDIR``.\n\n* ``LANG``, ``LC_ALL``, and ``LANGUAGE`` are set to ``C``.\n\n* ``TZ`` is set to ``GMT``.\n\n* ``COLUMNS`` is set to ``80``. (Note: When using ``--shell=zsh``,\n  this cannot be reset. It will reflect the actual terminal\'s width.)\n\n* ``CDPATH`` and ``GREP_OPTIONS`` are set to an empty string.\n\nPrysk also provides the following environment variables to tests:\n\n* ``PRYSK_TEMP``, set to the test runner\'s temporary directory.\n\n* ``TESTDIR``, set to the directory containing the test file.\n\n* ``TESTFILE``, set to the basename of the current test file.\n\n* ``TESTSHELL``, set to the value specified by ``--shell``.\n\nAlso note that care should be taken with commands that close the test\nshell\'s ``stdin``. For example, if you\'re trying to invoke ``ssh`` in\na test, try adding the ``-n`` option to prevent it from closing\n``stdin``. Similarly, if you invoke a daemon process that inherits\n``stdout`` and fails to close it, it may cause Prysk to hang while\nwaiting for the test shell\'s ``stdout`` to be fully closed.\n\n.. _unified context diff: https://en.wikipedia.org/wiki/Diff#Unified_format\n.. _its own example tests: https://github.com/nicoretti/prysk/tree/master/examples\n',
    'author': 'Nicola Coretti',
    'author_email': 'nico.coretti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://nicoretti.github.io/prysk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
