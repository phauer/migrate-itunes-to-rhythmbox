from pybuilder.core import use_plugin, init, Author
from migrate_itunes_to_rhythmbox import settings

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")

default_task = ['install_dependencies', 'clean', 'publish']

name = "migrate-itunes-to-rhythmbox"
version = "1.0"
summary = settings.PROJECT_DESCRIPTION
authors = (Author("Philipp Hauer")),
url = "https://github.com/phauer/migrate-itunes-to-rhythmbox"


@init
def set_properties(project):
    project.depends_on_requirements("requirements.txt")
    project.build_depends_on_requirements("requirements-build.txt")
    project.depends_on("pyItunes", url="git+https://github.com/liamks/pyitunes.git#egg=pyItunes-1.4") # use my fork to ensure stability
    project.set_property('distutils_classifiers', [
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3.5',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
    ])


