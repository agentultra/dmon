from setuptools import setup, find_packages

try:
    import multiprocessing
except ImportError:
    pass

__author__ = "James King"
__email__ = "james@agentultra.com"
__version__ = "0.1.1"
__license__ = "MIT"


setup(
    name="dmon",
    version=__version__,
    packages=find_packages(),

    setup_requires = [
        'nose'
    ],

    install_requires = [
        'eventlet',
    ],

    tests_require = [
        'nose',
        'mock',
    ],
    test_suite = 'nose.collector',

    author=__author__,
    author_email=__email__,
    license=__license__,
    description="A stream processing service for monitoring distributed clusters.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],

    entry_points={
        'console_scripts': [
            'dmon_shell = dmon.shell:run',
        ]
    }
)
