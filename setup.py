from setuptools import setup

setup(
    name='bgpwatch',
    version='0.1',
    py_modules=['bgpwatch'],
    install_requires=[
        'pytricia',
        'pyyaml',
        'pybgpstream',
    ],
    entry_points='''
        [console_scripts]
        bgpwatch=bgpwatch:main
    ''',
)
