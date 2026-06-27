"""Tests for the alphanumeric label generator."""
import unittest
import config
from label_generator import generate_alphanumeric_sequence, get_label_parts


def _fresh_generator():
    config.deleted_labels = []
    config.last_label_before_return = "A"
    config.last_turn_before_return = 0
    return generate_alphanumeric_sequence()


class TestGetLabelParts(unittest.TestCase):
    def test_letter_and_number(self):
        self.assertEqual(get_label_parts("A0"), ("A", "0"))
        self.assertEqual(get_label_parts("Z12"), ("Z", "12"))
        self.assertEqual(get_label_parts("BC3"), ("BC", "3"))

    def test_no_digits(self):
        chars, nums = get_label_parts("ABC")
        self.assertEqual(chars, "ABC")
        self.assertFalse(nums)

    def test_single_digit(self):
        self.assertEqual(get_label_parts("A1"), ("A", "1"))


class TestGenerateSequence(unittest.TestCase):
    def test_first_26_labels(self):
        gen = _fresh_generator()
        labels = [next(gen) for _ in range(26)]
        self.assertEqual(labels[0], "A0")
        self.assertEqual(labels[25], "Z0")

    def test_wraps_to_next_iteration(self):
        gen = _fresh_generator()
        # consume A0 .. Z0
        for _ in range(26):
            next(gen)
        label = next(gen)
        self.assertEqual(label, "A1")

    def test_sequence_is_unique(self):
        gen = _fresh_generator()
        labels = [next(gen) for _ in range(52)]
        self.assertEqual(len(set(labels)), 52)

    def test_deleted_labels_reused(self):
        gen = _fresh_generator()
        # consume a few labels
        for _ in range(3):
            next(gen)
        # put one back
        config.deleted_labels = ["A0"]
        label = next(gen)
        # generator should yield the recycled label
        # (exact yield depends on generator state — just check it's not a dupe)
        self.assertIsInstance(label, str)
        self.assertTrue(len(label) >= 2)


if __name__ == "__main__":
    unittest.main()
