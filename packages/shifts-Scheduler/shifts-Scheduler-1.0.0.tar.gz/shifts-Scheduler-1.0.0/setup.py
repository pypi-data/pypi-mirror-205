from setuptools import setup, find_packages

setup(
    name='shifts-Scheduler',
    version='1.0.0',
    description='A tool for managing employee shifts and labor costs',
    author='Abdelbaki Berkati',
    author_email='abdelbaki.berkati@gmail.com',
    url='https://github.com/bakissation/ShiftsScheduler',
    packages=find_packages(),
    install_requires=[
        'jsonschema==4.0.1', # Required library for working with JSON data
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='shifts management labor costs',
)
