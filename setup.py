"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='mnpolarity',
    version='0.0.1',
    description='Polarity Detection in Mongolian',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bayartsogt-ya/mnpolarity',
    author='Bayartsogt Yadamsuren',
    author_email='bayartsogt.yadamsuren@gmail.com',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='snorkel, weaksupervised, classification',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.6, <4',
    install_requires=[
        'joblib==1.0.1',
        'scikit-learn==0.24.2',
    ],
    extras_require={  # Optional
        'dev': [
            'snorkel==0.9.7',
            'tqdm==4.60.0',
            'twint==2.1.21',
            'PyYAML==5.4.1',
            'pytest==6.2.4',
        ],
        'test': [],
    },
    package_data={  # Optional
        # 'mnpolarity': ['package_data.dat'],
    },
    entry_points={  # Optional
        # 'console_scripts': [
        #     'sample=sample:main',
        # ],
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/bayartsogt-ya/mnpolarity/issues',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/bayartsogt-ya/mnpolarity/',
    },
)
