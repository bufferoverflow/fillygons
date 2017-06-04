from setuptools import setup

setup(
    name='fillygons',
    packages=['fillygons'],
    # Setuptools does not handle transitive dependencies very well and we
    # need to specify `numpy' explicitly as otherwise it won't be installed
    # which makes the installation of numpy-stl fail.
    install_requires=['sympy', 'pillow', 'numpy-stl', 'numpy'],
    entry_points=dict(
        console_scripts=[
            'generate_sources = fillygons.generate_sources:script_main',
            'render_stl = fillygons.testing.render_stl:script_main',
            'compare_images = fillygons.testing.compare_images:script_main',
            'find_failures = fillygons.testing.find_failures:script_main']))
