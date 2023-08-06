# Tresto

Tresto is a Python library that integrates with Trello to provide advanced
functionality for unit testing.  With Tresto, you can create Trello cards
for each test automatically, and these cards will be moved to the
appropriate list based on the test results.  This makes Tresto an ideal tool
for test-driven development, as it provides a convenient and visual way to
monitor the progress of your tests.

## Installation

You can install Tresto using pip:

```shell
pip3 install tresto
```

## Usage

Using Tresto is easy.  Simply create a TrestoTestCase and write your tests
as you normally would.  However, you will need to set up your Trello API key
and token as environment variables TRELLO_API_KEY and TRELLO_API_TOKEN.

```python
import unittest
from tresto import TrestoTestCase
# FIX: arithmetic.py is in examples/ folder
from arithmetic import add, subtract, multiply, divide

class TestArithmetic(TrestoTestCase):
    auto_create_board = True
    auto_create_lists = True

    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(1, 0)

if __name__ == '__main__':
    unittest.main()
```

You can then run your tests using the standard Python unittest framework.
See the tests/ subdirectory for test_hello_world.py, test_arithmetic.py and test_tresto.py -
Yes, that's Tresto testing itself:

```python
import os
import unittest
from tresto import TrestoTestCase
from trello.exceptions import ResourceUnavailable

class TestTresto(TrestoTestCase):

    def setUp(self):
        self.card_failed = None
        self.card_passed = None

    def test_1_board_setup(self):
        self.assertIsNotNone(self.board)
        self.assertEqual(self.board.name, self.board_name)

    def test_2_list_setup(self):
        self.assertIsNotNone(self.passed_list)
        self.assertIsNotNone(self.failed_list)
        self.assertEqual(self.passed_list.name, self.test_passed_list)
        self.assertEqual(self.failed_list.name, self.test_failed_list)

    def test_3_add_and_delete_cards(self):
        # Test add_card and delete_card for FAILED List
        card_name_failed = "Test Card for FAILED List"
        self.card_failed = self.add_card(self.failed_list, card_name_failed)
        self.assertEqual(self.card_failed.name, card_name_failed, self.failed_list)
        self.card_failed.delete()
        try:
            deleted_card_failed = self.board.get_card(self.card_failed.id)
            self.fail("Card was not deleted")
        except ResourceUnavailable:
            pass

        # Test add_card and delete_card for PASSED List
        card_name_passed = "Test Card for PASSED List"
        self.card_passed = self.add_card(self.passed_list, card_name_passed)
        self.assertEqual(self.card_passed.name, card_name_passed, self.passed_list)
        self.card_passed.delete()
        try:
            deleted_card_passed = self.board.get_card(self.card_passed.id)
            self.fail("Card was not deleted")
        except ResourceUnavailable:
            pass

    def test_4_add_and_move_card_between_lists(self):
        card_name = "Test Card for Moving Between Lists"
        card = self.add_card(self.passed_list, card_name)
        self.move_card(card, self.failed_list)

        # Refresh card data
        card.fetch()

        self.assertEqual(card.list_id, self.failed_list.id, self.failed_list)
        card.delete()

if __name__ == '__main__':
    unittest.main()
```


## Acknowledgements

Tresto is built using the [py-trello](https://github.com/sarumont/py-trello) library. Thank you to the py-trello developers for their great work!

## Contributing

Contributions are always welcome!  If you find a bug or have a suggestion
for how to improve Tresto, please open an issue [here](https://github.com/buanzo/tresto/issues).
