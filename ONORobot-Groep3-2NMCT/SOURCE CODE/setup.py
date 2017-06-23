"""OPSORO platform.

See:
https://github.com/opsoro/
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
from os import path

here = path.abspath(path.dirname(__file__))

#-----------------------------------------------------------------------------------------------------------------------

# Requirements for our application
INSTALL_REQUIRES = [
    "flask>=0.9,<0.11",
    "Flask-Login==0.2.2",
    # "Flask-Principal==0.3.5",
    # "Flask-Babel==0.9",
    # "Flask-Assets==0.10",
    # "Flask-Markdown==0.3",
    # "werkzeug==0.8.3",
    "tornado==4.0.1",
    "sockjs-tornado==1.0.1",
    "PyYAML==3.10",
    # "pyserial==2.7",
    # "netaddr==0.7.17",
    # "watchdog==0.8.3",
    # "sarge==0.1.4",
    # "netifaces==0.10",
    # "pylru==1.0.9",
    # "rsa==3.2",
    # "pkginfo==1.2.1",
    # "requests==2.7.0",
    # "semantic_version==2.4.2",
    # "psutil==3.2.1",
    # "awesome-slugify>=1.6.5,<1.7",
    # "feedparser>=5.2.1,<5.3"
    "simplejson>=3.8.0,<3.8.3",
    # "lupa>=1.0,<1.3",
    # "spidev==3.2",
    # "scipy>=0.16,<0.17.1",
    "pluginbase==0.4",
    "numpy>=1.9.3,<1.11.1"
]

# Additional requirements for optional install options
EXTRA_REQUIRES = dict(
    # # Dependencies for developing OPSORO
    develop=[
        # 	# Testing dependencies
        # 	"mock>=1.0.1",
        # 	"nose>=1.3.0",
        # 	"ddt",
        #
        # 	# Documentation dependencies
        # 	"sphinx>=1.3",
        # 	"sphinxcontrib-httpdomain",
        # 	"sphinx_rtd_theme",
        #
        # 	# PyPi upload related
        # 	"pypandoc"
    ],
    #
    # # Dependencies for developing OPSORO plugins
    plugins=[
        # 	"cookiecutter"
    ])

# Additional requirements for setup
SETUP_REQUIRES = []

# Dependency links for any of the aforementioned dependencies
DEPENDENCY_LINKS = []

#-----------------------------------------------------------------------------------------------------------------------
# Anything below here is just command setup and general setup configuration


def package_data_dirs(source, sub_folders):
    import os
    dirs = []

    for d in sub_folders:
        folder = os.path.join(source, d)
        if not os.path.exists(folder):
            continue

        for dirname, _, files in os.walk(folder):
            dirname = os.path.relpath(dirname, source)
            for f in files:
                dirs.append(os.path.join(dirname, f))

    return dirs


def params():
    name = 'opsoro'

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version = '0.1.0'

    description = 'Open Source Social Robotics Platform'
    long_description = 'Open Source Social Robotics Platform'  #open("README.md").read(),

    install_requires = INSTALL_REQUIRES
    extras_require = EXTRA_REQUIRES
    dependency_links = DEPENDENCY_LINKS
    setup_requires = SETUP_REQUIRES

    # The project's main homepage.
    url = 'https://github.com/opsoro/'

    # Author details
    author = 'OPSORO'
    author_email = 'info@opsoro.be'

    # Choose your license
    license = 'MIT'

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        "Environment :: Web Environment",
        "Framework :: Flask",

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        "Natural Language :: English",

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        "Programming Language :: JavaScript",
    ]

    # What does your project relate to?
    keywords = 'opsoro social robotics'

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages = find_packages(where="src")
    package_dir = {"": "src", }

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    # install_requires=['peppercorn'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    # 	'dev': ['check-manifest'],
    # 	'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data = {
        # 'opsoro': ['package_data.dat'],
        "opsoro":
        package_data_dirs('src/opsoro', ['static', 'templates', 'apps'])
    }

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    include_package_data = True
    zip_safe = False

    if os.environ.get('READTHEDOCS', None) == 'True':
        # we can't tell read the docs to please perform a pip install -e .[develop], so we help
        # it a bit here by explicitly adding the development dependencies, which include our
        # documentation dependencies
        install_requires = install_requires + extras_require['develop']

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points = {'console_scripts': ['opsoro=opsoro:main']}

    return locals()


setup(**params())
