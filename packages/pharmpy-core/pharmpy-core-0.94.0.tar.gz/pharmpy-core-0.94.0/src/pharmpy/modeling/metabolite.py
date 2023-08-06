"""
:meta private:
"""
from pharmpy.deps import sympy
from pharmpy.model import (
    Assignment,
    Compartment,
    CompartmentalSystem,
    CompartmentalSystemBuilder,
    Model,
    output,
)

from .odes import add_individual_parameter


def add_metabolite(model: Model, drug_dvid: int = 1):
    """Adds a metabolite compartment to a model

    The flow from the central compartment to the metabolite compartment
    will be unidirectional.

    Parameters
    ----------
    model : Model
        Pharmpy model
    drug_dvid : int
        DVID for drug (assuming all other DVIDs being for metabolites)

    Return
    ------
    Model
        Pharmpy model object

    Examples
    --------
    >>> from pharmpy.modeling import *
    >>> model = load_example_model("pheno")
    >>> model = add_metabolite(model)

    """
    qm1 = sympy.Symbol('QM1')
    model = add_individual_parameter(model, qm1.name)
    clm1 = sympy.Symbol('CLM1')
    model = add_individual_parameter(model, clm1.name)
    vm1 = sympy.Symbol('VM1')
    model = add_individual_parameter(model, vm1.name)

    odes = model.statements.ode_system
    central = odes.central_compartment
    ke = odes.get_flow(central, output)
    cl, vc = ke.as_numer_denom()
    cb = CompartmentalSystemBuilder(odes)
    metacomp = Compartment.create(name="METABOLITE")
    cb.add_compartment(metacomp)
    cb.add_flow(central, metacomp, qm1 / vc)
    cb.add_flow(metacomp, output, clm1 / vm1)
    cs = CompartmentalSystem(cb)

    # dvid_col = model.datainfo.typeix['dvid'][0]
    # dvids = dvid_col.categories

    conc = Assignment(sympy.Symbol('CONC_M1'), metacomp.amount / vm1)
    y_m1 = sympy.Symbol('Y_M1')
    y = Assignment(y_m1, conc.symbol + sympy.Symbol(model.random_variables.epsilons.names[0]))
    original_y = next(iter(model.dependent_variables))
    ind = model.statements.after_odes.find_assignment_index(original_y)
    old_after = model.statements.after_odes
    new_after = old_after[: ind + 1] + y + old_after[ind + 1 :]
    error = conc + new_after

    dvs = model.dependent_variables.copy()
    dvs[y_m1] = 2  # FIXME: Should be next DVID in categories
    statements = model.statements.before_odes + cs + error
    model = model.replace(statements=statements, dependent_variables=dvs)
    return model.update_source()
