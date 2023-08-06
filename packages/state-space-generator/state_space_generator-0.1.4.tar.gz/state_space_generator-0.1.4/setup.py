import os
import subprocess
import shutil
from pathlib import Path

from setuptools import setup, Extension, find_packages
from setuptools.command.install import install as install
from setuptools.command.build_py import build_py


__version__ = "0.1.4"


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):

        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package
            self.root_is_pure = False

        def get_tag(self):
            python, abi, plat = _bdist_wheel.get_tag(self)
            # We don't link with python ABI, but require python3
            python, abi = 'py3', 'none'
            return python, abi, plat
except ImportError:
    bdist_wheel = None


class CustomBuild(build_py):
    def run(self):
        curr_dir = os.getcwd()
        print(curr_dir)

        os.chdir('state_space_generator/scorpion')
        print(os.getcwd())

        subprocess.check_call(["python", "build.py"])

        os.chdir(curr_dir)

        super().run()

setup(
    name="state_space_generator",
    version=__version__,
    license='GNU',
    author="Dominik Drexler, Jendrik Seipp",
    author_email="dominik.drexler@liu.se, jendrik.seipp@liu.se",
    url="https://github.com/drexlerd/state-space-generator",
    description="A tool for state space exploration of PDDL files",
    long_description="",
    packages=["state_space_generator"],
    package_data={"state_space_generator":
        ["scorpion/fast-downward.py",
         "scorpion/README.md",
         "scorpion/LICENSE.md",
         "scorpion/builds/release/bin/*",
         "scorpion/builds/release/bin/translate/*",
         "scorpion/builds/release/bin/translate/pddl/*",
         "scorpion/builds/release/bin/translate/pddl_parser/*",
         "scorpion/driver/*"]
    },
    cmdclass={
        'bdist_wheel': bdist_wheel,
        'build_py': CustomBuild},
    has_ext_modules=lambda: True,  # to not obtain pure python wheels
    include_package_data=True,  # To copy the package data after build
    zip_safe=False,  # contains platform specific code
)
