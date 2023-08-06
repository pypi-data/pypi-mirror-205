import os
from setuptools import setup, find_packages

path = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(path, 'README.md')) as f:
        long_description = f.read()

except Exception as e:
    long_description = "MDLS建模"

setup(

    name="fischer",

    version="0.1.0",

    description="MDLS建模",

    long_description=long_description,

    long_description_content_type='text/markdown',

    python_requires=">=3.6.0",

    license="MIT Licence",

    url="https://github.com/Fischer-pixel/MDLS",

    author="Fischer-pixel",

    packages=find_packages(),

    include_package_data=True,

    install_requires=["numpy", "scikit-learn", "PyMieScatt", "tqdm", "scipy"],

    platforms="any",

    py_modules=["fischer_mdls"],

)
