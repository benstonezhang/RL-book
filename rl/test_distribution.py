import numpy as np
import unittest

from rl.distribution import Bernoulli, Categorical, Choose, Constant


def assert_almost_equal(dist_a, dist_b):
    '''Check that two distributions are "almost" equal (ie ignore small
    differences in floating point numbers when comparing them).

    '''
    list_a = list(dist_a.table())
    list_a.sort()

    list_b = list(dist_b.table())
    list_b.sort()

    np.testing.assert_almost_equal(list_a, list_b)


class TestFiniteDistribution(unittest.TestCase):
    def setUp(self):
        self.die = Choose({1, 2, 3, 4, 5, 6})

    def test_map(self):
        plusOne = self.die.map(lambda x: x + 1)
        assert_almost_equal(plusOne, Choose({2, 3, 4, 5, 6, 7}))

        evenOdd = self.die.map(lambda x: x % 2 == 0)
        assert_almost_equal(evenOdd, Choose({True, False}))

        greaterThan4 = self.die.map(lambda x: x > 4)
        assert_almost_equal(greaterThan4, Categorical({True: 1/3, False: 2/3}))


class TestConstant(unittest.TestCase):
    def test_constant(self):
        assert_almost_equal(Constant(42), Categorical({42: 1.}))
        self.assertAlmostEqual(Constant(42).probability(42), 1.)
        self.assertAlmostEqual(Constant(42).probability(37), 0.)


class TestBernoulli(unittest.TestCase):
    def setUp(self):
        self.fair = Bernoulli(0.5)
        self.unfair = Bernoulli(0.3)

    def test_constant(self):
        assert_almost_equal(self.fair, Categorical({True: 0.5, False: 0.5}))
        self.assertAlmostEqual(self.fair.probability(True), 0.5)
        self.assertAlmostEqual(self.fair.probability(False), 0.5)

        assert_almost_equal(self.unfair, Categorical({True: 0.3, False: 0.7}))
        self.assertAlmostEqual(self.unfair.probability(True), 0.3)
        self.assertAlmostEqual(self.unfair.probability(False), 0.7)


class TestChoose(unittest.TestCase):
    def setUp(self):
        self.one = Choose({1})
        self.six = Choose({1, 2, 3, 4, 5, 6})

    def test_choose(self):
        assert_almost_equal(self.one, Constant(1))
        self.assertAlmostEqual(self.one.probability(1), 1.)
        self.assertAlmostEqual(self.one.probability(0), 0.)

        categorical_six = Categorical({x: 1/6 for x in range(1, 7)})
        assert_almost_equal(self.six, categorical_six)
        self.assertAlmostEqual(self.six.probability(1), 1/6)
        self.assertAlmostEqual(self.six.probability(0), 0.)


class TestCategorical(unittest.TestCase):
    def setUp(self):
        self.normalized = Categorical({True: 0.3, False: 0.7})
        self.unnormalized = Categorical({True: 3., False: 7.})

    def test_categorical(self):
        assert_almost_equal(self.normalized, Bernoulli(0.3))
        self.assertAlmostEqual(self.normalized.probability(True), 0.3)
        self.assertAlmostEqual(self.normalized.probability(False), 0.7)
        self.assertAlmostEqual(self.normalized.probability(None), 0.)

    def test_normalization(self):
        assert_almost_equal(self.unnormalized, self.normalized)
        self.assertAlmostEqual(self.unnormalized.probability(True), 0.3)
        self.assertAlmostEqual(self.unnormalized.probability(False), 0.7)
        self.assertAlmostEqual(self.unnormalized.probability(None), 0.)