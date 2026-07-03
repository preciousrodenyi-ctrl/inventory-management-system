from unittest.mock import Mock, patch

from cli import main


def test_cli_list(capsys):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = [
        {"id": 1, "product_name": "Organic Almond Milk"}
    ]

    with patch("cli.requests.get", return_value=mock_response):
        main(["list"])

    captured = capsys.readouterr()
    assert "Organic Almond Milk" in captured.out


def test_cli_add(capsys):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"id": 4, "product_name": "Cashew Milk"}

    with patch("cli.requests.post", return_value=mock_response):
        main([
            "add",
            "--name", "Cashew Milk",
            "--brand", "Simple Truth",
            "--price", "4.25",
            "--stock", "12"
        ])

    captured = capsys.readouterr()
    assert "Cashew Milk" in captured.out


def test_cli_search(capsys):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "product_name": "Oat Milk",
        "brands": "Oatly"
    }

    with patch("cli.requests.get", return_value=mock_response):
        main(["search", "Oat Milk"])

    captured = capsys.readouterr()
    assert "Oat Milk" in captured.out