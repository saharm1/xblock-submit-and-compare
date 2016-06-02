"""Setup for submit-and-compare xblock"""

import os
from setuptools import setup
from setuptools.command.test import test as TestCommand

def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

setup(
    name='xblock-submit-and-compare',
    version='0.5',
    description='Submit and Compare XBlock for self assessment',
    packages=[
        'submit_and_compare',
    ],
    install_requires=[
        'XBlock',
        'django',
        'mock',
        'django_nose',
        'coverage',
    ],
    entry_points={
        'xblock.v1': [
            'submit-and-compare = submit_and_compare:SubmitAndCompareXBlock',
        ]
    },
    package_data=package_data("submit_and_compare", "static"),
    tests_require=[
    ],
    cmdclass={
        'test': Tox,
    },
)
