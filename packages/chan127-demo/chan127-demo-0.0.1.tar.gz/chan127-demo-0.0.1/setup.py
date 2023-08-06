from setuptools import setup, find_packages

# this grabs the requirements from requirements.txt
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='chan127-demo',
    version= '0.0.1',
    description='show one row of dataframe',
    install_requires=[REQUIREMENTS],
    entry_points="""
    [console_scripts]
    showdf=showdf.main:main
    """,
    author='ck',
    author_email=None,
    packages=find_packages()
)