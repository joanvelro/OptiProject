# Optimization Project Example with Auto-documentation using Sphinx
 


```
│
├── README.md                            # This file
│
├── data                                 # general data folder 
│                              
├── docs                                 # Auto-generated documentation        
│
├── notebooks                            # Notebooks folder
│
├── reports                              # output results and figures 
│    └── figures                         # figures folder 
│    └── logs                            # logs folder 
│    └── results                         # results folder 
│                                                            
├── src                                  # source code
│    └── opti_suite                             
│         └── opti_app   
│               └── constants.py   
│               └── analyzer                      
│                    └── data_analyzer.py            
│               └── context                    
│                    └── model_response.py
│                    └── exception.py
│                    └── model_data.py
│               └── model                   
│                    └── engine.py    
│               └── factory                          
│                    └── model_data_factory.py   
│                    └── model_response_factory.py 
│
│
├── test
│    └── data                            # input data files for unitary testing
│    └── reports                         # results from unitary testing
│    └── test_data.py                    # unitary test for test data
│    └── test_engine.py                  # unitary test for scheduler engine
│    └── test_converter.py               # unitary test for pconversion formats
│    └── test_python_version.py          # unitary test for python version
│
├── setup.py                             # python setup file to build the opti library
├── requirements.txt                     # python library dependencies 
└── 
```

## How to set up the Environment

#### Create  environment
```
# with conda
conda create --name OptiProject python=3.9

# with venv

# Windows
py -m venv OptiProject

# Linux/Mac
python -m venv OptiProject
```


#### Activate environment
```
# with conda
conda activate OptiProject

# with venv

# Windows
.\OptiProject\Scripts\activate

# Linux/Mac
source .OptiProject/bin/activate 
```

#### Or Create python environment with pip
```
python -m venv OptiProject
```

#### Activate the environment
```
OptiProject/Scripts/activate 
```

#### go to project path
```
cd <project-path>
```

#### Install requirements
```
pip install -r requirements.txt
```

#### Install pyomo independently
```
conda install pyomo -c conda-forge
```

#### Instalar extras: NEOS server
```
conda install pyomo.extras --channel conda-forge

conda install pyomo.extras  -c cachemeorg 
```

#### Instalar solver GLPK 
```
# windows
conda install glpk -c conda-forge

# linux
apt-get install -y -qq glpk-utils
SolverFactory('glpk', executable='/usr/bin/glpsol')
```

#### Instalar solver IPOPT
```
# Windows
conda install -c cachemeorg ipopt_bin

# Linux
wget -N -q "https://ampl.com/dl/open/ipopt/ipopt-linux64.zip"
unzip -o -q ipopt-linux64
SolverFactory('ipopt', executable='/content/ipopt').solve(model).write()
```

#### Instalar CBC 

Windows:
Download executable from:
https://ampl.com/products/solvers/open-source/
or
https://ampl.com/dl/open/cbc/cbc-win64.zip
or
https://github.com/coin-or/pulp/tree/master/pulp/solverdir/cbc/win/64
and add to the path (environment variable) the route of the .exe file

```
# Linux
apt-get install -y -qq coinor-cbc
SolverFactory('bonmin', executable=/usr/bin/cbc)
````

#### Instalar Couenne (MINLP) 

Windows
Download executable from:
https://ampl.com/dl/open/couenne/couenne-win64.zip
and finally add to the path (environment variable) the route of the .exe file

```
# Linux
wget -N -q "https://ampl.com/dl/open/couenne/couenne-linux64.zip"
unzip -o -q couenne-linux64
SolverFactory('couenne', executable=<path_to_exe>)
```

#### Instalar Bonmin (MINLP) 
Windows:
Download executable from:
https://ampl.com/dl/open/bonmin/bonmin-win64.zip

```
# Linux
wget -N -q "https://ampl.com/dl/open/bonmin/bonmin-linux64.zip"
unzip -o -q bonmin-linux64
SolverFactory('bonmin', executable=<path_to_exe>)
```

#### Detectar solver instalados
```
pyomo help -s
```

Ayuda sobre componentes
```
pyomo help --components
```

Ayuda sobre pyomo en general
```
pyomo help -a
```

## Create wheel of the library

first, execute all the unitary test and export results
```
python -m pytest test --junitxml=test-results.xml
```

Or execute tests with unittest
```
python -m unittest
```

then, check PEP 8 style before commit changes:
```
python  -m flake8 --max-line-length 120 --statistics
```

Finally, publish the wheel of the library in dist folder
```
python setup.py bdist_wheel
```



## How to generate Auto-documentation with Sphinx  

Install Sphinx and Rinohtype (if not installed)  in the virtual environment of the project you’re working on use the following commands below.

```
conda activate OptiProject
pip install Sphinx
pip install rinohtype
```
Create a docs directory and cd into this directory.
```
mkdir docs
cd docs
```

Setup Sphinx
```
sphinx-quickstart
```

Open source/conf.py and configure path to root directory, 
```
sys.path.insert(0, os.path.abspath('..\\src\\'))
```

Add extensions
```
extensions = ['sphinx.ext.viewcode', 'sphinx.ext.todo', 'sphinx.ext.autodoc']
```

Open the index.rst and change the content to the following. (Click the index.rst  link for full content)

```

===============================

Documentation - V.0.1
==============================

.. toctree::
   :maxdepth: 4
   :caption: Contents:

Model Data
***********
.. automodule:: product_name.app_name.context.model_data
   :members:
```

where automodule correspond with the name of the python file 
```
"""
.. module:: product_name.app_name.context.model_data
   :synopsis: Defines the model data class

.. moduleauthor:: (C) Jose Angel Velasco
"""
```

Still inside the docs directory run, Create the HTML documentation files.
```
make html
```

Create the latex documentation files
```
make latex
```

Create the PDF documentation files
```
sphinx-build -b rinoh source _build/rinoh
```

# check PEP 8 style
```
python  -m flake8 --max-line-length 120 --statistics
```

# publish the wheel of the library in dist folder
```
python setup.py bdist_wheel
```

# How to install the library from a whl
```
pip install dist/<name>.whl --extra-index-url <url>
```

(C) Jose Angel Velasco - 2022
