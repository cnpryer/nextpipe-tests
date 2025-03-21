import copy
import json
import os

import nextmv
import nextmv.cloud

from nextpipe import FlowSpec, foreach, join, needs, step


class Flow(FlowSpec):
    @foreach()  # Run the successor step for each item in the result list of this step
    @step
    def prepare(data: dict):
        """
        Creates 3 copies of the input and configures them for 3 different app parameters.
        """
        inputs = [copy.deepcopy(data) for _ in range(3)]
        return inputs

    @needs(predecessors=[prepare])
    @step
    def solve():
        """
        Runs the model.
        """
        pass

    @needs(predecessors=[solve])
    @join()  # Collect the results from the previous 'foreach' step and combine them into a list passed as the arg
    @step
    def merge(results: list[dict]):
        """Merges the results."""
        return results[0]


def main():
    # Load input data
    input = nextmv.load_local()

    # Run workflow
    flow = Flow("DecisionFlow", input.data)
    flow.run()

    # Write out the result
    print(json.dumps(flow.get_result(flow.merge)))


if __name__ == "__main__":
    main()
