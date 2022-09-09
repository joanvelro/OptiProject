import setuptools

# IMPORTANT: Use --extra-index-url https://pip.localsolver.com/ when running pip install
# Lastly, it’s important to understand that install_requires is a listing of “Abstract” requirements, i.e just names
# and version restrictions that don’t determine where the dependencies will be fulfilled from (i.e. from what index or
# source). The where (i.e. how they are to be made “Concrete”) is to be determined at install time using pip options.

# IMPORTANT: Version will be overwritten from Azure Pipeline

setuptools.setup(
    name='opti-suite-opti-app',
    version='OVERWRITTEN',
    author='Jose Angel Velasco',
    author_email='joseangel.velasco@yahoo.es',
    description='Dummy project for optimization with AutoDoc',
    packages=setuptools.find_packages("src", exclude=["test"]),  # include all packages under src
    package_dir={"": "src"},   # tell distutils packages are under src
    package_data={"opti_suite.opti_app.context": ["locale/*.json", "*json"]},
    include_package_data=True,
    python_requires=">=3.9",
    url='',
    license='',
    install_requires=[
        'Pyomo==6.2',
        'pandas==1.3.3',
        'numpy==1.20.3',
        'flake8==3.8.4',
        'pytest==7.1.1',
        'ipykernel==6.4.1',
        'openpyxl==3.0.7',
        'xlsxwriter==3.0.1'
    ]
)
