import os
import unittest
from trello import TrelloClient
from trello.util import create_oauth_token

class TrestoTestCase(unittest.TestCase):
    board_name = 'Tresto'
    test_passed_list = 'PASSED'
    test_failed_list = 'FAILED'
    auto_create_board = False
    auto_create_lists = False

    @classmethod
    def setUpClass(cls):
        api_key = os.environ['TRELLO_API_KEY']
        api_token = os.environ['TRELLO_API_TOKEN']

        cls.trello_client = TrelloClient(api_key=api_key, api_secret=None, token=api_token)

        # Find or create the board
        if cls.auto_create_board:
            cls.board = cls._find_or_create_board(cls.board_name)
        else:
            cls.board = cls._find_board(cls.board_name)

        # Find or create lists
        if cls.auto_create_lists:
            cls.passed_list = cls._find_or_create_list(cls.test_passed_list)
            cls.failed_list = cls._find_or_create_list(cls.test_failed_list)
        else:
            cls.passed_list = cls._find_list(cls.test_passed_list)
            cls.failed_list = cls._find_list(cls.test_failed_list)

    @classmethod
    def _find_board(cls, name):
        for board in cls.trello_client.list_boards():
            if board.name == name:
                return board
        raise Exception(f'Board {name} not found.')

    @classmethod
    def _find_or_create_board(cls, name):
        try:
            board = cls._find_board(name)
        except Exception:
            board = cls.trello_client.add_board(name)
        return board

    @classmethod
    def _find_list(cls, name):
        for lst in cls.board.list_lists():
            if lst.name == name:
                return lst
        raise Exception(f'List {name} not found.')

    @classmethod
    def _find_or_create_list(cls, name):
        try:
            lst = cls._find_list(name)
        except Exception:
            lst = cls.board.add_list(name)
        return lst

    @classmethod
    def add_card(cls, lst, card_name, card_desc=''):
        return lst.add_card(name=card_name, desc=card_desc)

    @classmethod
    def move_card(cls, card, lst):
        card.change_list(lst.id)
