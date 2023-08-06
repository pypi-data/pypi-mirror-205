from typing import Dict, Any, List, Tuple

from canals import component


@component
class Double:
    def __init__(self, input: str = "value", output: str = "value"):
        """
        Doubles the value in input.

        Single input single output component. Doesn't take parameters.

        :param input: the name of the input.
        :param output: the name of the output.
        """
        self.inputs = [input]
        self.outputs = [output]

    def run(self, name: str, data: List[Tuple[str, Any]], parameters: Dict[str, Any]):
        for _, value in data:
            value *= 2

        return ({self.outputs[0]: value}, parameters)


def test_double_default():
    component = Double()
    results = component.run(name="test_component", data=[("value", 10)], parameters={})
    assert results == ({"value": 20}, {})
    assert component.init_parameters == {}


def test_double_init_params():
    component = Double(input="test_in", output="test_out")
    results = component.run(name="test_component", data=[("test_in", 10)], parameters={})
    assert results == ({"test_out": 20}, {})
    assert component.init_parameters == {"input": "test_in", "output": "test_out"}
