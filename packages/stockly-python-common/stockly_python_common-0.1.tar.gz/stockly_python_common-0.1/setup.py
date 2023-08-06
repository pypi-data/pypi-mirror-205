from distutils.core import setup

with open('./README.md') as readme_file:
    README = readme_file.read()

with open('./HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='stockly_python_common',
    packages=['stockly_python_common'],
    version='0.1',
    license='MIT',
    description='All useful utils for external stockly developers',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    author='Stockly',
    author_email='dev@stockly.us',
    url='https://gitlab.com/vzinjuvadia/stockly-python',
    download_url='https://gitlab.com/vzinjuvadia/stockly-python/-/archive/1.0.3/stockly-python-1.0.3.tar.gz',
    keywords=['BOT', 'STOCKLY', 'PYTHON', 'STOCKLY_UTILS'],
    install_requires=[
        'requests',
        'matrix-client',
        'opsdroid-get-image-size',

    ],
    python_requires='>= 3.7',
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    package_data={'stockly_python_common': ['config/*', ]},
    setup_requires=['wheel']
)
