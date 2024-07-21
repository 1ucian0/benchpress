# This code is part of Qiskit.
#
# (C) Copyright IBM 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""Test summit benchmarks"""

from bqskit import compile
from bqskit.compiler import Compiler

from benchpress.bqskit_gym.circuits import (
    bqskit_bv_all_ones,
    bqskit_circSU2,
    trivial_bvlike_circuit,
)
from benchpress.config import Configuration
from benchpress.utilities.io import qasm_circuit_loader
from benchpress.workouts.validation import benchpress_test_validation
from benchpress.workouts.device_transpile import WorkoutDeviceTranspile100Q


BACKEND = Configuration.backend()
TWO_Q_GATE = BACKEND.two_q_gate_type
OPTIMIZATION_LEVEL = Configuration.options["bqskit"]["optimization_level"]
compiler = Compiler()


@benchpress_test_validation
class TestWorkoutDeviceTranspile100Q(WorkoutDeviceTranspile100Q):
    def test_QFT_100_transpile(self, benchmark):
        """Compile 100Q QFT circuit against target backend"""
        circuit = qasm_circuit_loader(
            Configuration.get_qasm_dir("qft") + "qft_N100.qasm", benchmark
        )

        @benchmark
        def result():
            new_circ = compile(
                circuit,
                model=BACKEND,
                optimization_level=OPTIMIZATION_LEVEL,
                compiler=compiler,
            )
            return new_circ

        benchmark.extra_info["gate_count_2q"] = result.gate_counts[TWO_Q_GATE]
        benchmark.extra_info["depth_2q"] = result.multi_qudit_depth
        assert result

    def test_QV_100_transpile(self, benchmark):
        """Compile 10Q QV circuit against target backend"""
        circuit = qasm_circuit_loader(
            Configuration.get_qasm_dir("qv") + "qv_N100_12345.qasm"
        )

        @benchmark
        def result():
            new_circ = compile(
                circuit,
                model=BACKEND,
                optimization_level=OPTIMIZATION_LEVEL,
                compiler=compiler,
            )
            return new_circ

        benchmark.extra_info["gate_count_2q"] = result.gate_counts[TWO_Q_GATE]
        benchmark.extra_info["depth_2q"] = result.multi_qudit_depth
        assert result

    def test_circSU2_100_transpile(self, benchmark):
        """Compile 100Q circSU2 circuit against target backend"""
        circuit = bqskit_circSU2(100, 3)

        @benchmark
        def result():
            new_circ = compile(
                circuit,
                model=BACKEND,
                optimization_level=OPTIMIZATION_LEVEL,
                compiler=compiler,
            )
            return new_circ

        benchmark.extra_info["gate_count_2q"] = result.gate_counts[TWO_Q_GATE]
        benchmark.extra_info["depth_2q"] = result.multi_qudit_depth
        assert result

    def test_BV_100_transpile(self, benchmark):
        """Compile 100Q BV circuit against target backend"""
        circuit = bqskit_bv_all_ones(100)

        @benchmark
        def result():
            new_circ = compile(
                circuit,
                model=BACKEND,
                optimization_level=OPTIMIZATION_LEVEL,
                compiler=compiler,
            )
            return new_circ

        benchmark.extra_info["gate_count_2q"] = result.gate_counts[TWO_Q_GATE]
        benchmark.extra_info["depth_2q"] = result.multi_qudit_depth
        assert result

    def test_square_heisenberg_100_transpile(self, benchmark):
        """Compile 100Q square-Heisenberg circuit against target backend"""
        circuit = qasm_circuit_loader(
            Configuration.get_qasm_dir("square-heisenberg")
            + "square_heisenberg_N100.qasm",
            benchmark,
        )

        @benchmark
        def result():
            new_circ = compile(
                circuit,
                model=BACKEND,
                optimization_level=OPTIMIZATION_LEVEL,
                compiler=compiler,
            )
            return new_circ

        benchmark.extra_info["gate_count_2q"] = result.gate_counts[TWO_Q_GATE]
        benchmark.extra_info["depth_2q"] = result.multi_qudit_depth
        assert result

    def test_QAOA_100_transpile(self, benchmark):
        """Compile 100Q QAOA circuit against target backend"""
        circuit = qasm_circuit_loader(
            Configuration.get_qasm_dir("qaoa") + "qaoa_barabasi_albert_N100_3reps.qasm",
            benchmark,
        )

        @benchmark
        def result():
            new_circ = compile(
                circuit,
                model=BACKEND,
                optimization_level=OPTIMIZATION_LEVEL,
                compiler=compiler,
                seed=0,
            )
            return new_circ

        benchmark.extra_info["gate_count_2q"] = result.gate_counts[TWO_Q_GATE]
        benchmark.extra_info["depth_2q"] = result.multi_qudit_depth
        assert result

    def test_BVlike_simplification_transpile(self, benchmark):
        """Transpile a BV-like circuit that should collapse down
        into a single X and Z gate on a target device
        """
        circuit = trivial_bvlike_circuit(100)

        @benchmark
        def result():
            new_circ = compile(
                circuit,
                model=BACKEND,
                optimization_level=OPTIMIZATION_LEVEL,
                compiler=compiler,
                seed=0,
            )
            return new_circ

        benchmark.extra_info["gate_count_2q"] = result.gate_counts[TWO_Q_GATE]
        benchmark.extra_info["depth_2q"] = result.multi_qudit_depth
        assert result
