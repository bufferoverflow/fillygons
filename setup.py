from setuptools import setup

setup(
    name='fillygons',
    packages=['fillygons'],
    install_requires=['sympy'],
    entry_points=dict(
        console_scripts=[
            'generate_sources = fillygons.generate_sources:script_main']))
