import unittest
from unittest.mock import MagicMock

from your_module import create_hero, Hero

class TestCreateHero(unittest.TestCase):
    def test_create_hero(self):
        # Create a mock hero object
        hero = MagicMock(spec=Hero)

        # Mock the Session object and its methods
        session = MagicMock()
        session.add.return_value = None
        session.commit.return_value = None
        session.refresh.return_value = None

        # Mock the Session context manager
        engine = MagicMock()
        engine.return_value.__enter__.return_value = session

        # Call the create_hero function
        result = create_hero(hero)

        # Assert that the session methods were called correctly
        session.add.assert_called_once_with(hero)
        session.commit.assert_called_once()
        session.refresh.assert_called_once_with(hero)

        # Assert that the result is the same as the input hero object
        self.assertEqual(result, hero)

if __name__ == '__main__':
    unittest.main()