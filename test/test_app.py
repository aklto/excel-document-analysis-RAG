import unittest
from unittest.mock import patch
from interface.streamlit_app import InsuranceRAGApp


class TestInsuranceRAGApp(unittest.TestCase):
    """Unit tests for the InsuranceRAGApp Streamlit interface."""

    @patch("streamlit.text_input", return_value="test query")
    @patch("streamlit.spinner")
    @patch("streamlit.write")
    @patch("streamlit.markdown")
    def test_run(self, mock_markdown, mock_write, mock_spinner, mock_text_input):
        app = InsuranceRAGApp()
        app.run()

        mock_text_input.assert_called_once_with("Введите вопрос по отчёту:")
        mock_spinner.assert_called_once()
        mock_write.assert_called_once()


if __name__ == "__main__":
    unittest.main()
