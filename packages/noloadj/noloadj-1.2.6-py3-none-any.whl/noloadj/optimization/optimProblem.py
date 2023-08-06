# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from typing import Dict, Callable
import scipy.optimize as scipyOpt
from noloadj.optimization.specifications import Spec
from noloadj.optimization.wrapper import Wrapper
from noloadj.optimization.iterationHandler import Iterations
from noloadj.optimization.multiobjective import EpsilonConstraint
from noloadj.optimization.Tools import *

class OptimProblem:
    # TODO : standardiser les results d'optim entre 1D : SLSQP Result et
    #  2D : Pareto...
    def __init__(self, model: Callable[..., Dict], specifications: Spec,
                 parameters: Dict = {}, resultsHandler=True):
        self.specifications = specifications
        self.wrapper = Wrapper(model,specifications, parameters,resultsHandler)

    def run(self, ftol=1e-5, disp=True, maxiter=500, nbParetoPts=5,
            method='SLSQP',method2d='epsconstr'):
        """
        Solves the optimization problem.
        :param ftol: float Precision goal for the value of f in the stopping
        criterion.
        :param disp: bool  Set to True to print convergence messages. If False,
         verbosity is ignored and set to 0.
        :param maxiter: int  Maximum number of iterations.
        :param nbParetoPts: int Number of Pareto points wished
        :param method: SLSQP or IPOPT or LeastSquare according problems
        :param method2d: algorithm for solving bi objective problems
        :return: results of optimization under class Wrapper (in Wrapper.py)
        """
        # utilisation de SLSQP
        options = {'ftol': ftol, 'disp': disp, 'maxiter': maxiter,}
        pbSize = len(self.wrapper.spec.objectives)

        # TODO si pas de contraintes, lancer un BFGS

        if pbSize == 1:  # Cas mono-objectif
            if (method == 'SLSQP'):
                result = SLSQP(self.wrapper, self.specifications.xinit, options,
                               disp)  # TODO : modifier results
            elif (method=='IPOPT'):
                result = IPOPT(self.wrapper,self.specifications.xinit,options)
            elif (method == 'LeastSquare'):
                result = LSSQ(self.wrapper, self.specifications.xinit, options)
                # TODO : modifier results
            else:
                print("SLSQP or LeastSquare or IPOPT")

        elif pbSize == 2:  # Cas bi-objectif
            p = EpsilonConstraint(self.wrapper,method,disp)
            if method2d=='epsconstr':
                result = p.optim2D(self.specifications.xinit, nbParetoPts,
                                   options)
            elif method2d=='ponderation':
                result = p.optim2D_weighting(self.specifications.xinit,
                                             nbParetoPts, options)
            else:
                print('ponderation or epsconstr')
            # TODO : modifier results
            # result = p.optim2D_basic(self.specifications.xinit, nbParetoPts,
            # options)
        else:
            print("Only mono or bi objective function.")

        return self.wrapper  # result  #TODO : modifier results


def SLSQP(wrapper: Wrapper, x0, options,disp):
    """
    Solves the optimization problem with SLSQP method
    from scipy.optimize.minimize
    :param wrapper: Class giving information to scipy.minimize (fgrad, bounds,
    constraints)
    :param x0: Initial inputs vector
    :param options: options = {'func': None, 'maxiter': 100, 'ftol': 1e-06,
    'iprint': 1, 'disp': False, 'eps': 1.4901161193847656e-08}
     ftol : float Precision goal for the value of f in the stopping criterion.
     eps : float  Step size used for numerical approximation of the Jacobian.
     disp : bool  Set to True to print convergence messages. If False,
     verbosity is ignored and set to 0.
     maxiter : int  Maximum number of iterations.
     :param disp : set to True to print convergence messages.
    :return: class Result including the optimal inputs vector
    """
    # Equality constraint means that the constraint function result is to
    # be zero
    # Inequality means that it is to be non-negative.
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
    wrapper.init()  # init doit être appelé avant l'optim pour bien prendre en
    # compte les nouvelles contraintes.
    options['disp']=False
    x0=normalize(x0,wrapper.spec.bounds) # normalization of values
    bounds=normalize_bounds(wrapper.spec.bounds)
    result = scipyOpt.minimize(wrapper.f_val_grad, x0=x0, jac=True,
                               method='SLSQP', bounds=bounds,
                               constraints=wrapper.constraints, options=options)
    while (not result.success) and (result.status!=9):
        if (result.status != 9): # not if maxiteration# TODO gérer une exception
            #  Iteration limit exceeded    (Exit mode 9)
            # TRY Random initial point !
            print("WARNING : Optimization doesn't converge... "
                  "Trying random inital guess")
            import numpy
            x0 = numpy.random.rand(len(x0))
            print('new initial point: ',denormalize(x0,wrapper.spec.bounds))
            import jax.numpy as jnp
            x0=jnp.array(x0)
            result = scipyOpt.minimize(wrapper.f_val_grad, x0=x0, jac=True,
                            method='SLSQP', bounds=bounds,
                            constraints=wrapper.constraints, options=options)
    if (not result.success):
        print("ERROR : Optimization doesn't converge.")  # TODO donner plus
        # de détails sur les spec de cette optim
        print(result.message)
        # TODO faire afficher les specifications
        print('objectif : ' + str(wrapper.spec.objectives))
        print('contraintes : ' + str(wrapper.spec.eq_cstr)+
              str(wrapper.spec.ineq_cstr))
    result.fun=result.fun*(wrapper.spec.objectives_val[1]-
        wrapper.spec.objectives_val[0])+wrapper.spec.objectives_val[0]
    if (result.success) and disp:
        print(result.message,'\t(Exit mode 0)')
        print('\t\t\tCurrent function value:',result.fun)
        print('\t\t\tIterations:',result.nit)
        print('\t\t\tFunction evaluations:', result.nfev)
        print('\t\t\tGradient evaluations:', result.njev)
    result.x = denormalize(result.x, wrapper.spec.bounds)
    return result

def IPOPT(wrapper: Wrapper, x0,options):
    """
    Solves the optimization problem with IPOPT method
    from scipy.optimize.minimize
    :param wrapper: Class giving information to scipy.minimize (fgrad, bounds,
    constraints)
    :param x0: Initial inputs vector
    :param options: options = {'func': None, 'maxiter': 100, 'ftol': 1e-06,
    'iprint': 1, 'disp': False, 'eps': 1.4901161193847656e-08}
     ftol : float Precision goal for the value of f in the stopping criterion.
     eps : float  Step size used for numerical approximation of the Jacobian.
     disp : bool  Set to True to print convergence messages. If False,
     verbosity is ignored and set to 0.
     maxiter : int  Maximum number of iterations.
    :return: class Result including the optimal inputs vector
    """
    # Equality constraint means that the constraint function result is to
    # be zero
    # Inequality means that it is to be non-negative.
    # https://cyipopt.readthedocs.io/en/stable/tutorial.html
    wrapper.init()  # init doit être appelé avant l'optim pour bien prendre en
    # compte les nouvelles contraintes.
    x0=normalize(x0,wrapper.spec.bounds) # normalization of values
    bounds=normalize_bounds(wrapper.spec.bounds)
    from cyipopt import minimize_ipopt
    result = minimize_ipopt(wrapper.f_val_grad, x0=x0, jac=True,
                            bounds=bounds,constraints=wrapper.constraints)
    while (not result.success) and (result.status!=9):
        if (result.status != 9): # not if maxiteration# TODO gérer une exception
            #  Iteration limit exceeded    (Exit mode 9)
            # TRY Random initial point !
            print("WARNING : Optimization doesn't converge... "
                  "Trying random inital guess")
            import numpy
            x0 = numpy.random.rand(len(x0))
            print('new initial point: ',denormalize(x0,wrapper.spec.bounds))
            import jax.numpy as jnp
            x0=jnp.array(x0)
            result = minimize_ipopt(wrapper.f_val_grad, x0=x0, jac=True,
                             bounds=bounds,constraints=wrapper.constraints)
    if (not result.success):
        print("ERROR : Optimization doesn't converge.")  # TODO donner plus
        # de détails sur les spec de cette optim
        print(result.message)
        # TODO faire afficher les specifications
        print('objectif : ' + str(wrapper.spec.objectives))
        print('contraintes : ' + str(wrapper.spec.eq_cstr)+
              str(wrapper.spec.ineq_cstr))
    result.fun=result.fun*(wrapper.spec.objectives_val[1]-
        wrapper.spec.objectives_val[0])+wrapper.spec.objectives_val[0]
    if (result.success)and options['disp']:
        print('Algorithm IPOPT terminated successfully')
        print('\t\t\tCurrent function value:',result.fun)
        print('\t\t\tIterations:',result.nit)
        print('\t\t\tFunction evaluations:', result.nfev)
        print('\t\t\tGradient evaluations:', result.njev)
    result.x=denormalize(result.x,wrapper.spec.bounds)
    return result


def LSSQ(wrapper: Wrapper, x0, options):
    """
    Solves the optimization problem with LeastSquare method from
    scipy.optimize.minimize
    :param wrapper: Class giving information to scipy.minimize
    (fgrad, bounds, constraints)
    :param x0: Initial inputs vector
    :param options: options = {'func': None, 'maxiter': 100, 'ftol': 1e-06,
    'iprint': 1, 'disp': False, 'eps': 1.4901161193847656e-08}
     ftol : float Precision goal for the value of f in the stopping criterion.
     eps : float  Step size used for numerical approximation of the Jacobian.
     disp : bool  Set to True to print convergence messages. If False,
     verbosity is ignored and set to 0.
     maxiter : int  Maximum number of iterations.
    :return: class Result including the optimal inputs vector
    """
    bounds = wrapper.spec.bounds.T

    # https: // docs.scipy.org / doc / scipy / reference / generated /
    # scipy.optimize.least_squares.html
    result = scipyOpt.least_squares(fun=wrapper.f_val, x0=x0, bounds=bounds,
                                    jac=wrapper.f_grad,
                             ftol=options['ftol'], max_nfev=options['maxiter'])

    if (not result.success or options['disp']):  # TODO gérer une exception
        print(result.message)
        print("Solution found: ", result.x)
        print("Value of the cost function at the solution: ", result.cost)
        print("Vector of residuals at the solution: ", result.fun)
        print("Gradient of the cost function at the solution: ", result.grad)

    return result

    '''
    is able to make several optimization changing one input parameter.
    returns the value of each elements of 'outputs' obtained for each optimization
    use iter.print() or noloadj.gui.plotIterations.plotXY(iter) to see the results
    '''


def optimizeParam(model: Callable[..., Dict], parameters: Dict,
                  specifications: Spec, variable, range, outputs,
                  ftol=0.001, disp=False, maxiter=50):
    """
    Solves all optimization problems for an input varying in a range of values,
    the other inputs remaining constant.
    :param model: model
    :param parameters: constant input parameters
    :param specifications: specifications of the problem
    :param variable: the varying input
    :param range: range of values of the varying input
    :param outputs: names of the outputs
    :param ftol: float Precision goal for the value of f in the stopping
    criterion.
    :param disp: bool Set to True to print convergence messages. If False,
     verbosity is ignored and set to 0.
    :param maxiter: int Maximum number of iterations.
    :return: list including all output vectors obtained at each optimization
    """
    iter = Iterations([variable], outputs)  # permet de sauvegarder les
    # résultats au fur et à mesure
    x = specifications.xinit
    for val in range:
        parameters[variable] = val
        optim = OptimProblem(model, specifications, parameters)
        res = optim.run(ftol=ftol, disp=disp, maxiter=maxiter)
        out = [res.rawResults[var] for var in outputs]
        iter.updateData([val], out)
    return iter
