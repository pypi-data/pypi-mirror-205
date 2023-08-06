from distutils.core import setup

setup(
    name="pyved",
    author="moonb3ndr et al.",
    author_email="contact@kata.games",
    url="https://github.com/wkta/gamedev-pyved",
    package_dir={'':'src'},
    packages=[
        "pyved",
        ],
    include_package_data=True,  # to be sure we get _sm_shelf/legacy.py, etc.

    description='experimental toolbox for game devs who use python',
    license='MIT',
    version=str('0.0.1'),
)
