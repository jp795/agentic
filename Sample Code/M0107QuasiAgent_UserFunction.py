def check_palindrome():
    """
    Function to determine if a given word is a palindrome.
    
    A palindrome is a word that is the same when read forwards and backwards.
    This function prompts the user to input a word and checks if it is a palindrome.
    
    Parameters:
    None
    
    Returns:
    This function does not return any value. It prints a message indicating whether the entered word is a palindrome.
    
    Example Usage:
    >>> check_palindrome()  
    Please enter a word: radar
    'radar' is a palindrome.
    
    Edge Cases:
    - An empty string will be considered a palindrome since reversing it results in another empty string.
    - Whitespace around the word is disregarded due to the use of `strip()`.
    - Case sensitivity is not handled, so inputs with different cases (e.g., "Anna") will be considered non-palindrome unless converted to the same case before comparison.
    """
    # Prompt the user to enter a word
    word = input('Please enter a word: ').strip()
    
    # Reverse the word using slicing
    reversed_word = word[::-1]
    
    # Check if the word is the same as its reverse
    if word == reversed_word:
        print(f"'{word}' is a palindrome.")
    else:
        print(f"'{word}' is not a palindrome.")

import unittest
from io import StringIO
import sys

class TestPalindromeChecker(unittest.TestCase):
    
    def test_basic_functionality(self):
        # Redirect input and output flows
        sys.stdin = StringIO('radar')
        sys.stdout = StringIO()
        check_palindrome()
        # Check if output is as expected
        self.assertIn("'radar' is a palindrome.", sys.stdout.getvalue())

    def test_empty_string(self):
        sys.stdin = StringIO('')
        sys.stdout = StringIO()
        check_palindrome()
        self.assertIn("'' is a palindrome.", sys.stdout.getvalue())

    def test_single_character(self):
        sys.stdin = StringIO('a')
        sys.stdout = StringIO()
        check_palindrome()
        self.assertIn("'a' is a palindrome.", sys.stdout.getvalue())

    def test_whitespace_string(self):
        sys.stdin = StringIO(' ')
        sys.stdout = StringIO()
        check_palindrome()
        self.assertIn("' ' is a palindrome.", sys.stdout.getvalue())

    def test_non_palindrome(self):
        sys.stdin = StringIO('python')
        sys.stdout = StringIO()
        check_palindrome()
        self.assertIn("'python' is not a palindrome.", sys.stdout.getvalue())

    def test_case_sensitivity(self):
        sys.stdin = StringIO('Radar')
        sys.stdout = StringIO()
        check_palindrome()
        self.assertIn("'Radar' is not a palindrome.", sys.stdout.getvalue())

    def test_with_numbers(self):
        sys.stdin = StringIO('12321')
        sys.stdout = StringIO()
        check_palindrome()
        self.assertIn("'12321' is a palindrome.", sys.stdout.getvalue())

    def test_with_symbols(self):
        sys.stdin = StringIO('A man, a plan, a canal, Panama')
        sys.stdout = StringIO()
        check_palindrome()
        self.assertIn("'A man, a plan, a canal, Panama' is not a palindrome.", sys.stdout.getvalue())
    
    def tearDown(self):
        # Reset stdin and stdout to its original state
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()