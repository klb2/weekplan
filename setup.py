from setuptools import setup, find_packages

from weekplan import __version__, __author__, __email__

with open("README.md", encoding="utf8") as rm:
    long_desc = rm.read()

setup(
    name = "weekplan",
    version = __version__,
    author = __author__,
    author_email = __email__,
    description = "Week Project Planner",
    #keywords = ["rearrangement algorithm", "quantitative risk management"],
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license='GPLv3',
    #url='https://gitlab.com/klb2/rearrangement-algorithm',
    #project_urls={
    #    'Documentation': "https://rearrangement-algorithm.readthedocs.io",
    #    'Source Code': 'https://gitlab.com/klb2/rearrangement-algorithm'
    #    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        ],
    packages=find_packages(),
    tests_require=['pytest', 'tox'],
    entry_points={
        'console_scripts': [
            'weekplan = weekplan.__main__:main_cmd'
        ],
},
)
