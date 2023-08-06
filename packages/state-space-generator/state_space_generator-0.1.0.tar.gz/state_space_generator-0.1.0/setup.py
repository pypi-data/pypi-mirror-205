import os
import subprocess
from pathlib import Path

from setuptools import setup, Extension, find_packages
from setuptools.command.install import install as install


__version__ = "0.1.0"
HERE = Path(__file__).resolve().parent


class CustomInstall(install):
    def run(self):
        # Get the build directory
        build_dir = Path(self.build_lib).resolve()
        print("Build directory:", build_dir)
        subprocess.check_call([build_dir / "state_space_generator/scorpion/build.py"])

        # this copies package data
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
    packages=['state_space_generator'],
    package_data={
          "": ["src/state_space_generator/scorpion/fast-downward.py",
               "src/state_space_generator/scorpion/build.py",
              "src/state_space_generator/scorpion/README.md", 
              "src/state_space_generator/scorpion/LICENSE.md",
              "src/state_space_generator/scorpion/builds/release/bin/*",
              "src/state_space_generator/scorpion/builds/release/bin/translate/*",
              "src/state_space_generator/scorpion/builds/release/bin/translate/pddl/*",
              "src/state_space_generator/scorpion/builds/release/bin/translate/pddl_parser/*",
              "src/state_space_generator/scorpion/driver/*"]
      },
    package_dir={'state_space_generator': 'src/state_space_generator'},
    cmdclass={"install": CustomInstall},
    has_ext_modules=lambda: True,
    include_package_data=True,
    zip_safe=False,
)
