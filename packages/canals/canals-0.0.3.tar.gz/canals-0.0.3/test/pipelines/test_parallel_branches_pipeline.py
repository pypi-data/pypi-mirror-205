from pathlib import Path
from pprint import pprint

from canals.pipeline import Pipeline
from test.components import AddValue, Repeat, Double

import logging

logging.basicConfig(level=logging.DEBUG)


def test_pipeline(tmp_path):
    add_one = AddValue(add=1, input="value")

    pipeline = Pipeline()
    pipeline.add_component("add_one", add_one)
    pipeline.add_component("enumerate", Repeat(input="value", outputs=["0", "1", "2"]))
    pipeline.add_component("add_ten", AddValue(add=10, input="0"))
    pipeline.add_component("double", Double(input="1", output="value"))
    pipeline.add_component("add_three", AddValue(add=3, input="2"))
    pipeline.add_component("add_one_again", add_one)

    pipeline.connect("add_one", "enumerate.1")
    pipeline.connect("enumerate.0", "add_ten")
    pipeline.connect("enumerate.1", "double")
    pipeline.connect("enumerate.2", "add_three")
    pipeline.connect("add_three", "add_one_again")

    try:
        pipeline.draw(tmp_path / "parallel_branches_pipeline.png")
    except ImportError:
        logging.warning("pygraphviz not found, pipeline is not being drawn.")

    results = pipeline.run({"value": 1})
    pprint(results)

    assert results == {
        "add_one_again": [{"value": 6}],
        "add_ten": [{"value": 12}],
        "double": [{"value": 4}],
    }


if __name__ == "__main__":
    test_pipeline(Path(__file__).parent)
