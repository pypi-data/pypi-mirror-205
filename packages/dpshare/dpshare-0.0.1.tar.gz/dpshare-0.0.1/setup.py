from setuptools import setup, find_packages

setup(
    name='dpshare',
    version='0.0.1',
    author='brody715',
    author_email='brody71517@gmail.com',
    description='',
    url='https://github.com/brody715/dpshare',
    packages=find_packages(include=('dpshare',)),

    tests_require=[
        'pytest>=7.2.0',
    ],
    python_requires='>=3.8'
)
