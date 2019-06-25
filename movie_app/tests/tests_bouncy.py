from django.test import TestCase
from movie_app.tests import bouncy_numbers


class BouncyTestCase(TestCase):

    def test_get_last_one_bouncy_should_return_int_type(self):
        assert isinstance(bouncy_numbers.get_last_one_bouncy(50.5), int)

    def test_bouncy_counter_should_return_int(self):
        assert isinstance(bouncy_numbers.bouncy_counter([1, 0, 0], 0), int)

    def test_non_increasing_should_return_true_if_is_decreasing_list(self):
        assert bouncy_numbers.non_increasing([5, 2, 1])

    def test_non_increasing_should_return_flase_if_is_increasing_list(self):
        assert not bouncy_numbers.non_increasing([1, 2, 5])

    def test_non_decreasing_should_return_true_if_is_increasing_list(self):
        assert bouncy_numbers.non_decreasing([1, 2, 5])

    def test_non_decreasing_should_return_flase_if_is_decreasing_list(self):
        assert not bouncy_numbers.non_decreasing([5, 2, 1])

    def test_is_bouncy_return_true_if_the_list_is_bouncy(self):
        assert bouncy_numbers.is_bouncy([1, 0, 5])

    def test_is_bouncy_return_false_if_the_list_is_not_bouncy(self):
        assert not bouncy_numbers.is_bouncy([2, 4, 5])

    def test_if_finish_return_true(self):
        ''' if the least number for which the proportion of
            bouncy numbers is to its percentage '''
        assert bouncy_numbers.if_finish(538, 269, 50)

    def test_if_finish_return_false(self):
        ''' if the least number for which the proportion of
            bouncy numbers less than to its percentage '''
        assert not bouncy_numbers.if_finish(538, 210, 50)
