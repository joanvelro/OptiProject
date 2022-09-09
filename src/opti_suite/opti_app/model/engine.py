"""
.. module:: opti_suite.opti_app.model.engine
   :synopsis: Engine

.. moduleauthor:: (C) Jose Angel Velasco - 2022
"""
import time
import logging
import traceback
import pyomo.environ as pyo

from abc import ABC
from pyomo.util.infeasible import log_infeasible_constraints

from opti_suite.opti_app.constants import ColName
from opti_suite.opti_app.context.model_data import ModelData
from opti_suite.opti_app.factory.data_converter import DataConverter
from opti_suite.opti_app.factory.model_response_factory import ModelResponseFactory
from opti_suite.opti_app.context.exception import OptiSuiteException, OptiSuiteDataException

logger = logging.getLogger(__name__)


class Engine(ABC):
    """
    ``This class defines the optimization engine for build and solve the optimization problem``

            *Attributes*:

                *status* :
                ``Status of the optimization execution.``

                *model* :
                ``Instance of the optimization model.``

                *data* :
                ``A ModelData data instance.``

                *response* :
                ``A ModelResponse data instance.``

                *results* :
                ``Optimization model results``


            *Methods*:

                *execute* :
                ``Run DataAnalyzer with the instance DataModel, build the model, solve the model and build
                model response.``

                *get_response* :
                ``Get the ModelResponse instance generated with the ModelResponseFactory with solution of saved in
                ModelData.``

                *generate_json_response* :
                ``Get the json response with the solution.``

                *generate_excel_response* :
                ``Get the excel response with the solution.``

                *generate_solver_factory*
                ``Generate solver factory based on the solver choose``

                *has_solution*
                ``Check if the solver founded a solution and the quality of the solution``
            """

    def __init__(self, data: ModelData) -> None:
        self.results = None
        self.status = None
        self.data = data
        self.response = None
        self.model = None

    def execute(self, verbosity: bool = False, solver: str = 'cbc', opt_parameters: dict = None):
        """
        ``This method trigger the engine optimization module.``
            *Arguments* :

                *verbosity* :
                ``Verbosity of engine (by default True).``

                *solver* :
                ``Solver to be used (string).``

                *opt_parameters* :
                ``Dictionary with the solver parameters.``
        """
        try:
            self.__build_model()
            self.__solve(verbosity, solver, opt_parameters)
            self.__build_solution()

        except (OptiSuiteException, OptiSuiteDataException):
            raise

        except Exception as err:
            logger.exception('There was an unexpected error running the optimization engine')
            raise OptiSuiteException('There was an unexpected error running the optimization engine') from err

    def __build_model(self):
        logger.info('Building optimization model...')

        self.model = pyo.ConcreteModel()

        start = time.time()

        try:
            self.__build_sets()
            self.__build_parameters()
            self.__build_variables()
            self.__build_constraints()
            self.__build_objective()

        except Exception as err:
            logger.exception(f'Error building model: {err}\n{traceback.format_exc()}')
            self.model = None
            raise OptiSuiteException('Error building model') from err

        end = time.time()
        logger.info(f'done! It took {round(end - start, 3)} seconds\n')

    def __build_sets(self):
        # Planning info
        self.model.workers = self.data.get_workers()[ColName.WORKER].to_list()
        self.model.periods = self.data.get_periods()[ColName.PERIOD].to_list()
        self.model.shifts_ids = self.data.get_shifts_ids()
        self.model.shifts_map = self.data.get_shifts()

    def __build_parameters(self):

        self.hours_per_shift = self.data.get_config_parameter(ColName.HOURS_PER_SHIFT)
        self.daily_hours_limit = self.data.get_config_parameter(ColName.DAILY_HOURS_LIMIT)
        self.work_load = self.data.get_config_parameter(ColName.WORK_LOAD)
        self.unitary_cost = self.data.get_config_parameter(ColName.UNITARY_COST)

    def __build_variables(self):
        # Decision variables

        # binary variables representing if a worker is scheduled somewhere
        self.model.worker_scheduled = pyo.Var(((worker, period, shift)
                                               for worker in self.model.workers
                                               for shift in self.model.shifts_ids
                                               for period in self.model.shifts_map[shift]
                                               ),
                                              within=pyo.Binary, initialize=0)

        # binary variables representing if a worker is necessary
        self.model.worker_needed = pyo.Var(self.model.workers, within=pyo.Binary, initialize=0)

    def __build_constraints(self):

        # Constraint: Each worker can not work more than the limit of hours
        self.model.constraint_limit_hours = pyo.Constraint(self.model.workers,
                                                           rule=self.__build_constraint_limit_hours)

        # Constraint: in each period the workload required has to be done
        self.model.constraint_work_done = pyo.Constraint(rule=self.__build_constraint_work_done)

        # Constraint: workers needed
        self.model.constraint_workers_needed = pyo.Constraint(self.model.workers,
                                                              rule=self.__build_constraint_workers_needed)

    def __build_constraint_limit_hours(self, model, worker):
        return sum(self.hours_per_shift*self.model.worker_scheduled[worker, period, shift]
                   for shift in self.model.shifts_ids
                   for period in self.model.shifts_map[shift]) <= self.daily_hours_limit

    def __build_constraint_work_done(self, model):
        return sum(self.hours_per_shift*self.model.worker_scheduled[worker, period, shift]
                   for worker in self.model.workers
                   for shift in self.model.shifts_ids
                   for period in self.model.shifts_map[shift]) >= self.work_load

    def __build_constraint_workers_needed(self, model, worker):
        return self.model.worker_needed[worker] >= sum(
            self.model.worker_scheduled[worker, period, shift]
            for shift in self.model.shifts_ids
            for period in self.model.shifts_map[shift]
            )

    def __build_objective(self):

        self.workforce_cost = sum(self.unitary_cost*self.model.worker_needed[worker] for worker in self.model.workers)
        self.model.objective = pyo.Objective(rule=self.workforce_cost, sense=pyo.minimize)

    def __solve(self, verbosity, solver, opt_parameters):

        try:
            opt = self.generate_solver_factory(solver, opt_parameters)

            start = time.time()
            logger.info('Solving full problem...')
            self.results = opt.solve(self.model, tee=verbosity)
            logger.info(f'done! It took {round(time.time() - start, 3)} seconds\n')

            if self.has_solution():
                logger.info('Optimal Solution Founded')
            else:
                logger.info('No Solution Founded')

        except OptiSuiteException:
            raise

        except Exception as err:
            logger.exception(f'Error solving model: {err}\n{traceback.format_exc()}')
            raise OptiSuiteException('Error solving optimization problem') from err

    def __build_solution(self):

        if self.has_solution():

            logger.info('Workforce minimum cost: {} $'.format(pyo.value(self.workforce_cost)))
            try:
                [self.data.add_solution_scheduled_worker(worker, period, shift, pyo.value(var))
                 for ((worker, period, shift), var) in self.model.worker_scheduled.items()]

                [self.data.add_solution_needed_worker(worker, pyo.value(var))
                 for (worker, var) in self.model.worker_needed.items()]

                self.response = ModelResponseFactory.create(self.data) if self.has_solution() else None

            except Exception as err:
                logger.exception(f'Error building solution: {err}\n{traceback.format_exc()}')
                raise OptiSuiteException('Error building solution') from err

    def has_solution(self) -> bool:
        """
        ``Check whether the optimization problem has been solved.``

        *Returns*:
            *bool*:
            ``If true, the problem has been solved. Otherwise, false.``
        """
        self.status = self.results.solver.status
        condition = self.results.solver.termination_condition

        max_time_limit = condition == pyo.TerminationCondition.maxTimeLimit
        feasible = condition == pyo.TerminationCondition.optimal or condition == pyo.TerminationCondition.feasible
        solution = (self.status == pyo.SolverStatus.ok and feasible) or \
                   (self.status == pyo.SolverStatus.aborted and max_time_limit)

        if not solution:
            logger.error(self.results)
            logger.error(f'(!) Something is wrong -> status: [{self.status}] and condition: [{condition}]')
            if (condition == pyo.TerminationCondition.infeasible) and (logger.getEffectiveLevel() <= logging.DEBUG):
                log_infeasible_constraints(self.model, logger=logger, log_expression=True, log_variables=True)
            raise OptiSuiteException('No solution found!')

        return solution

    def generate_solver_factory(self, solver: str, opt_parameters: dict) -> pyo.SolverFactory:
        """
        ``Configure the internal solver and its parameters.``

        *Arguments*:
            *solver* :
             ``(str): Name of the internal solver.``
            *opt_parameters*:
            ``(dict): Parameters for the internal solver.``

        *Returns*:
            *opt*:
            ``pyo.SolverFactory: A pyo.SolverFactory class instance with the configuration of the internal solver.``
        """
        # Define solver: glpk, cbc, cplex, gurobi
        opt_parameters = dict() if opt_parameters is None else opt_parameters
        opt = pyo.SolverFactory(solver)
        opt.options.update(opt_parameters)

        if solver == 'glpk':
            opt.options['mipgap'] = opt_parameters.get('mipgap', 0.001)

        elif solver == 'cbc':
            opt.options['integertolerance'] = opt_parameters.get('integertolerance', 1e-11)
            opt.options['ratioGAP'] = opt_parameters.get('ratioGAP', 0.0005)  # (0.05 %)
            opt.options['timeMode'] = opt_parameters.get('timeMode', 'elapsed')
            opt.options['seconds'] = opt_parameters.get('seconds', 300)

        elif solver == 'cplex':
            opt.options['mipgap'] = opt_parameters.get('mipgap', 0.001)

        elif solver == 'gurobi':
            opt.options['TimeLimit'] = opt_parameters.get('TimeLimit', 300)

        return opt

    def get_response(self):
        """
        ``Returns the ModelResponse instance with the solution of the optimization problem``
        """
        return self.response

    def generate_json_response(self, output_filename: str = None, rounded: bool = True) -> dict:
        """
        ``Generate the response of the planning engine for the logistic problem in json format``

        *Arguments*:
            *output_filename*:
             ``(str, optional): Path of the response file.``

            *rounded*:
            ``(bool, optional): If True, all the values will be rounded.``

        *Returns*:

            *json_response*:
            ``dict: Response of the planning engine for the logistic problem in json format if the output_filename param
            is not provided. Otherwise, None.``
        """
        if self.has_solution():
            json_response = DataConverter.scheduling_response_to_json(self.get_response(), output_filename)
        else:
            logger.error('json response could not be generated because there is no solution')
            json_response = None

        return json_response

    def generate_excel_report(self, filename: str) -> None:
        """
            ``Generate the response of the planning engine for the logistic problem in Excel format``

            *Arguments*:
                *output_filename*:
                 ``(str, optional): Path of the response file.``

        """
        if self.has_solution():
            DataConverter.scheduling_response_to_excel(self.get_response(), data=self.data,
                                                       with_request=True, output_path=filename)
        else:
            logger.error('Excel report could not be generated because there is no solution')
