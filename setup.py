from setuptools import setup, find_packages


setup(
    name="da.utils.hierarchy",
    version="0.0.1",
    namespace_packages=['da', 'da.utils'],
    packages=find_packages('src'),
    package_dir={
        '': 'src',
    },
    install_requires=['da.utils'],
)
