from setuptools import setup, find_packages

import focli

install_requires = [
    'requests>=2.3.0',
    'blessings>=1.6',
    'six>=1.10.0'
]

setup(
    name='focli',
    version=focli.__version__,
    description=focli.__doc__.strip(),
    url='https://github.com/joohoi/focli',
    download_url='https://github.com/joohoi/focli/tarball/0.1',
    author=focli.__author__,
    author_email='joona@kuori.org',
    license=focli.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'focli = focli.__main__:main',
        ],
    },
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
    ],
)
