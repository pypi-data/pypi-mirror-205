#!/usr/bin/env python3
# encoding: utf-8

"""Define regression tests for RuNNer."""

from typing import List

import pytest

from ase.atoms import Atoms
from runnerase import Runner
from runnerase import generate_symmetryfunctions


class TestFunctional:
    """Define functional tests for the runner calculator.

    These tests pass if they complete without an error.
    """

    seed = 42

    @pytest.mark.parametrize('dataset', ['dataset_h2o'])
    def test_modes(
        self,
        dataset: List[Atoms],
        executable: str,
        request
    ) -> None:
        """Run RuNNer Modes 1 through 3 for a given test system."""
        # Load the test dataset.
        dataset = request.getfixturevalue(dataset)

        # Create a calculator object.
        command = f'{executable} > PREFIX.out'
        runnercalc = Runner(dataset=dataset, command=command)

        # Define the folder.
        runnercalc.label = 'test_results/mode1/mode1'

        # Define symmetry functions.
        radials = generate_symmetryfunctions(dataset, sftype=2,
                                             algorithm='half')
        angulars = generate_symmetryfunctions(dataset, sftype=3,
                                              algorithm='literature')

        runnercalc.symmetryfunctions += radials
        runnercalc.symmetryfunctions += angulars

        # Set a defined seed for reproducibility.
        runnercalc.set(random_seed=self.seed)

        # Run Mode 1.
        runnercalc.run(mode=1)

        # Run Mode 2.
        runnercalc.label = 'test_results/mode2/mode2'
        runnercalc.set(epochs=5)
        runnercalc.set(use_short_forces=False)
        runnercalc.run(mode=2)

        # Run Mode 3.
        runnercalc.label = 'test_results/mode3/mode3'
        runnercalc.run(mode=3)

    @pytest.mark.parametrize('dataset', ['dataset_h2o'])
    def test_restart(
        self,
        dataset: List[Atoms],
        executable: str,
        request
    ) -> None:
        """Test that the RuNNer calculator can restart without any changes."""
        # Load the test dataset.
        dataset = request.getfixturevalue(dataset)

        # Create a calculator object.
        command = f'{executable} > PREFIX.out'
        runnercalc = Runner(dataset=dataset, command=command)

        # Define symmetry functions.
        radials = generate_symmetryfunctions(dataset, sftype=2,
                                             algorithm='half')
        angulars = generate_symmetryfunctions(dataset, sftype=3,
                                              algorithm='literature')

        runnercalc.symmetryfunctions += radials
        runnercalc.symmetryfunctions += angulars

        # Set a defined seed for reproducibility.
        runnercalc.set(random_seed=self.seed)

        # Run Mode 1.
        runnercalc.label = 'test_results/mode1/mode1'
        runnercalc.run(mode=1)

        runnercalc_restarted = Runner(restart='test_results/mode1/mode1')

        assert len(runnercalc.results) == len(runnercalc_restarted.results)
        assert all(i is not None for i in runnercalc.results.values())
