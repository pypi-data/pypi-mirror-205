import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='JFQ',  # should match the package folder
    packages=setuptools.find_packages(),  # should match the package folder
    version='v0.1.14',  # important for updates
    license='GNU2L',  # should match your chosen license
    description='various utilities',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='',
    author_email='',
    url='', #removed github url
    install_requires=['requests','pandas','matplotlib','xlsxwriter','anytree','blpapi','openpyxl','sqlalchemy==1.4.47'],  # list all packages that your package uses
    keywords=["openAPI"],  # descriptive meta-data
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ]
)