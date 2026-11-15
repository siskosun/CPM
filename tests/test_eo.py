import random
import unittest

from cpm.eo import CubeEdges, all_face_moves, eo_preserving_moves, move_effect


class EdgeOrientationTests(unittest.TestCase):
    def test_solved_cube_has_no_bad_edges(self):
        self.assertEqual(CubeEdges.solved().eo_count(), 0)

    def test_zz_natural_moves_preserve_eo(self):
        for move in eo_preserving_moves():
            with self.subTest(move=move):
                self.assertEqual(CubeEdges.solved().apply(move).eo_count(), 0)

    def test_f_and_b_quarter_turns_flip_four_edges(self):
        for move in ("F", "F'", "B", "B'"):
            with self.subTest(move=move):
                self.assertEqual(CubeEdges.solved().apply(move).eo_count(), 4)

    def test_f2_b2_preserve_eo(self):
        for move in ("F2", "B2"):
            self.assertEqual(CubeEdges.solved().apply(move).eo_count(), 0)

    def test_m_slice_quarter_turn_changes_eo(self):
        for move in ("M", "M'"):
            with self.subTest(move=move):
                self.assertEqual(CubeEdges.solved().apply_slice(move).eo_count(), 4)

    def test_even_eo_parity_after_arbitrary_face_turns(self):
        seqs = [
            ("R", "U", "F", "L'", "B2", "D", "R2"),
            ("F", "F", "B'", "U2", "R2"),
            ("R'", "D2", "B", "L", "F'", "U", "B2"),
        ]
        for seq in seqs:
            state = CubeEdges.solved().apply_sequence(seq)
            self.assertEqual(state.eo_count() % 2, 0, (seq, state.bad_edges()))

    def test_all_face_moves_preserve_even_eo_parity(self):
        for move in all_face_moves():
            self.assertEqual(CubeEdges.solved().apply(move).eo_count() % 2, 0)

    def test_each_face_turn_has_inverse(self):
        for face in "RLUDFB":
            for suffix, inverse in (("", "'"), ("'", ""), ("2", "2")):
                state = CubeEdges.solved().apply(face + suffix).apply(face + inverse)
                self.assertEqual(state, CubeEdges.solved())

    def test_four_quarter_turns_restore_all_edges(self):
        for face in "RLUDFB":
            state = CubeEdges.solved().apply_sequence((face, face, face, face))
            self.assertEqual(state, CubeEdges.solved())

    def test_eo_generators_preserve_after_composition(self):
        seqs = [
            ("R", "U", "L'", "D2", "F2", "B2", "R2", "U'"),
            ("L2", "D", "R'", "U2", "B2", "F2", "D'", "L"),
            ("U", "R2", "D'", "L", "F2", "U2", "B2", "R'"),
        ]
        for seq in seqs:
            self.assertEqual(CubeEdges.solved().apply_sequence(seq).eo_count(), 0)

    def test_each_eo_generator_preserves_random_eo_states(self):
        rng = random.Random(20261115)
        generators = eo_preserving_moves()
        for _ in range(40):
            scramble = tuple(rng.choice(generators) for _ in range(20))
            state = CubeEdges.solved().apply_sequence(scramble)
            self.assertTrue(state.is_fully_oriented())
            for move in generators:
                with self.subTest(scramble=scramble, move=move):
                    self.assertTrue(state.apply(move).is_fully_oriented())

    def test_move_effect_counts(self):
        self.assertEqual(move_effect("R")["bad_count"], 0)
        self.assertEqual(move_effect("F")["bad_count"], 4)
        self.assertEqual(move_effect("F2")["bad_count"], 0)


if __name__ == "__main__":
    unittest.main()
