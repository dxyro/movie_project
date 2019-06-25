import unittest


# palindrome
def palindrome(string: str) -> bool:
    string = ''.join(c for c in string if c.isalnum())
    return string.lower().replace(' ', '')[::-1] == string.lower().replace(' ', '')

class A:
    pass

class PalindromesTestCase(unittest.TestCase):

    def test_palindrome_function_should_return_true_for_anna(self):
        assert palindrome('anna')

    def test_palindrome_function_should_return_false_for_peter(self):
        assert not palindrome('peter')

    def test_palindrome_function_should_return_true_for_anna_capital_case(self):
        assert palindrome('Anna')

    def test_palindrome_function_should_return_true_if_is_valid_palindrome_even_if_it_has_spaces(self):
        assert palindrome('anita lava la tina')

    def test_palindrome_function_with_special_character_is_valid_palindrome_should_return_true(self):
        assert palindrome('Don\'t nod')

    def test_palindrome_should_raise_error_if_param_is_not_a_string(self):
        with self.assertRaises(TypeError):
            palindrome(2)

if __name__ == '__main__':
    unittest.main()