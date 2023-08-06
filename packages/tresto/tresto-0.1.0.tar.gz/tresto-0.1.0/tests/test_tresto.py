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
        self.assertEqual(self.card_failed.name, card_name_failed)
        self.card_failed.delete()
        try:
            deleted_card_failed = self.board.get_card(self.card_failed.id)
            self.fail("Card was not deleted")
        except ResourceUnavailable:
            pass

        # Test add_card and delete_card for PASSED List
        card_name_passed = "Test Card for PASSED List"
        self.card_passed = self.add_card(self.passed_list, card_name_passed)
        self.assertEqual(self.card_passed.name, card_name_passed)
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

        self.assertEqual(card.list_id, self.failed_list.id)
        card.delete()

if __name__ == '__main__':
    unittest.main()
