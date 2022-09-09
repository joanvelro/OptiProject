

Optimization Project with Autodoc using Sphinx
================================================

This is a template for a simple optimization project

.. image:: /images/opti.png
  :width: 400


How to run the library
------------------------

1) Create an input data instance from a json file:

      ``from opti_suite.opti_app.factory.model_data_factory import ModelDataFactory``

      ``data = ModelDataFactory.create_from_json_file(input_json=<file-path-to-json-input>)``

2) Create and instance of the optimization engine with the input data and execute:

      ``from opti_suite.opti_app.model.engine import Engine``

      ``engine = Engine(data=data)``

      ``engine.execute()``

3) Get the response in json format:

      ``json_response = engine.generate_json_response()``



.. toctree::
   :maxdepth: 4
   :caption: Scheduler Contents:


Engine
-----------
.. automodule:: opti_suite.opti_app.model.engine
   :members:

Model Data
-----------
.. automodule:: opti_suite.opti_app.context.model_data
   :members:

Model Response
-----------
.. automodule:: opti_suite.opti_app.context.model_response
   :members:

Exception
-----------
.. automodule:: opti_suite.opti_app.context.exception
   :members:

Model Data Factory
-----------
.. automodule:: opti_suite.opti_app.factory.model_data_factory
   :members:

Model Response Factory
-----------
.. automodule:: opti_suite.opti_app.factory.model_response_factory
   :members:



Indices and tables
------------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

