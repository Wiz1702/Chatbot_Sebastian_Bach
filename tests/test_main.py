import os
import unittest
from unittest.mock import patch, MagicMock
from types import SimpleNamespace

import main


class TestMain(unittest.TestCase):
    def test_get_api_key_from_env(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "abc123"}, clear=False):
            self.assertEqual(main.get_api_key(), "abc123")

    def test_get_api_key_no_env_and_no_input(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch("builtins.input", side_effect=EOFError):
                with self.assertRaises(SystemExit):
                    main.get_api_key()

    def test_bach_chat_success(self):
        mock_client = MagicMock()
        mock_response = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="Hi"))])
        mock_client.chat.completions.create.return_value = mock_response
        with patch("main.get_client", return_value=mock_client):
            result = main.bach_chat("Hello")
            self.assertEqual(result, "Hi")

    def test_bach_chat_api_error(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("boom")
        with patch("main.get_client", return_value=mock_client):
            with self.assertRaises(RuntimeError):
                main.bach_chat("Hello")


if __name__ == "__main__":
    unittest.main()
