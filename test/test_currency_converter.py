import unittest
from unittest.mock import patch, MagicMock
import requests
from code.currency_converter import convert_currency, run


class TestCurrencyConverter(unittest.TestCase):
    @patch("requests.get")
    def test_convert_currency_success(self, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"EUR": 0.85}}
        mock_get.return_value = mock_response

        result = convert_currency(100, "USD", "EUR")
        self.assertEqual(result, "100 USD = 85.00 EUR")

    @patch("requests.get")
    def test_convert_currency_unsupported_currency(self, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"rates": {"EUR": 0.85}}
        mock_get.return_value = mock_response

        result = convert_currency(100, "USD", "XYZ")
        self.assertEqual(result, "Currency 'XYZ' is not supported.")

    @patch("requests.get")
    def test_convert_currency_api_error(self, mock_get):
        # Mock API response failure
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        result = convert_currency(100, "USD", "EUR")
        self.assertEqual(result, "API Error")

    def test_run_invalid_command(self):
        mock_message = MagicMock()
        mock_bot = MagicMock()
        mock_message.chat.id = 12345
        mock_message.text = "/convert 100"

        run(mock_message, mock_bot)
        mock_bot.send_message.assert_called_with(
            12345, "Usage: /convert <amount> <from_currency> <to_currency>"
        )

    @patch("your_module.convert_currency")
    def test_run_valid_command(self, mock_convert_currency):
        mock_message = MagicMock()
        mock_bot = MagicMock()
        mock_message.chat.id = 12345
        mock_message.text = "/convert 100 USD EUR"

        mock_convert_currency.return_value = "100 USD = 85.00 EUR"
        run(mock_message, mock_bot)
        mock_bot.send_message.assert_called_with(12345, "100 USD = 85.00 EUR")

    def test_run_exception_handling(self):
        mock_message = MagicMock()
        mock_bot = MagicMock()
        mock_message.chat.id = 12345
        mock_message.text = "/convert 100 USD EUR"

        with patch("your_module.convert_currency", side_effect=Exception("Some error")):
            run(mock_message, mock_bot)
            mock_bot.send_message.assert_called_with(12345, "Some error")


if __name__ == "__main__":
    unittest.main()
