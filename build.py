from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")

default_task = ['install_dependencies', 'clean', 'publish']


@init
def set_properties(project):
    project.depends_on_requirements("requirements.txt")
    project.build_depends_on_requirements("requirements-build.txt")
    project.depends_on("pyItunes", url="git+https://github.com/liamks/pyitunes.git#egg=pyItunes-1.4")

