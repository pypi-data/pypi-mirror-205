from setuptools import setup, find_packages

setup(
    name='chan127-demo',
    version= '0.0.3',
    description='show one row of dataframe',
    install_requires=['pandas','click'],
    entry_points="""
    [console_scripts]
    showdf=showdf.main:main
    """,
    author='ck',
    author_email=None,
    packages=find_packages()
)