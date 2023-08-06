import stripstats.hyp_test as hyp
import unittest
import math

class TestHypothesisTestingMethodS(unittest.TestCase):
    def test_ANOVA_ONEWAY(self):
        Cola=[88,90,92]
        ClubSoda=[83,95,87]
        Water=[80,82,84]
        self.assertEqual(hyp.ANOVA_ONEWAY((Cola, ClubSoda, Water)), )




if __name__ == '__main__':
    unittest.main()