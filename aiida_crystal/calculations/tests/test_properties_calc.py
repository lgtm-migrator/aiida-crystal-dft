#   Copyright (c)  Andrey Sobolev, 2019. Distributed under MIT license, see LICENSE file.

# noinspection PyUnresolvedReferences
from aiida_crystal.tests.fixtures import *


def test_store_calc(properties_calc):
    calc = properties_calc
    calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})
    calc.store_all()
    assert calc.pk is not None
    assert calc.inp.code.pk is not None
    assert calc.inp.parameters.pk is not None
    assert calc.inp.wavefunction.pk is not None


def test_validate_input(test_properties_code, properties_calc_parameters, test_wavefunction):
    from aiida.common.exceptions import InputValidationError
    from aiida_crystal.calculations.properties import PropertiesCalculation
    calc = PropertiesCalculation()
    with pytest.raises(InputValidationError):
        calc._validate_input(calc.get_inputs_dict())
    calc.use_code(test_properties_code)
    with pytest.raises(InputValidationError):
        calc._validate_input(calc.get_inputs_dict())
    calc.use_parameters(properties_calc_parameters)
    with pytest.raises(InputValidationError):
        calc._validate_input(calc.get_inputs_dict())
    calc.use_wavefunction(test_wavefunction)
    assert calc._validate_input(calc.get_inputs_dict())


def test_submit(properties_calc):
    from aiida.common.folders import Folder
    temp_dir = tempfile.mkdtemp()
    properties_calc.store_all()
    properties_calc.submit_test(folder=Folder(temp_dir), subfolder_name='test')
    files = os.listdir(os.path.join(temp_dir, 'test-00001'))
    assert '_aiidasubmit.sh' in files
    assert properties_calc._WAVEFUNCTION_FILE in files
    assert properties_calc._DEFAULT_INPUT_FILE in files
    shutil.rmtree(temp_dir)
