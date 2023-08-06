from setuptools import setup

setup(
    name='request5',
    version='0.0.2',
    py_modules=['request5'],
    entry_points={
        'console_scripts': [
            'request5=request5:main'
        ]
    },
    install_requires=[],
    author='H454NSec',
    author_email='mrhasan660066@gmail.com',
    description='Enjoy!',
    url='https://github.com/H454NSec',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
