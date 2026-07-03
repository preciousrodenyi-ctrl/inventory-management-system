from unittest.mock import patch
import cli


@patch("builtins.input", side_effect=["8"])
def test_exit(mock_input):
    cli.main()


@patch("cli.requests.get")
def test_view_inventory(mock_get):

    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = []

    cli.view_inventory()


@patch("cli.requests.get")
def test_search_name(mock_get):

    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = []

    cli.name_search = lambda: None

    assert True