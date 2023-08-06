from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()
    

REQUIREMENTS = ['click', 
                'requests>=2.28',
                'pandas==1.5.3',
                'mlflow[extras]==2.1',
                'python-dotenv==0.21',
                'minio==7.1',
                'scikit-learn==1.2']

SETUP_REQUIRES = ['flake8', 'pytest-runner']


setup(
    name='dhuolib',
    version='0.1.0',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Antonio Carlos de Lima Junior',
    author_email='antonio.lima@engdb.com.br',
    url='https://gitlab.engdb.com.br/dhuo-plat/dhuo-data/data-science/dhuolib',
    packages=find_packages(include=['dhuolib', 'dhuolib.*']),
    install_requires=REQUIREMENTS,
    setup_requires=SETUP_REQUIRES,
    tests_require=['pytest'],
    entry_points={
      'console_scripts': ['dh = dhuolib.cli:main']
    },
    classifiers=[               
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',        
        'Operating System :: OS Independent',
        'Natural Language :: Portuguese (Brazilian)',
        'Natural Language :: English',

      ],
    keywords='datascience datapipeline mlops',
    license='MIT',
)
