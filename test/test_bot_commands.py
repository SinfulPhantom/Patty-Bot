from bot_commands import valid_steam64id, valid_email


def test_valid_steam64id():
    test_id = "A" * 17
    assert valid_steam64id(test_id)


def test_invalid_steam64id():
    test_id = "B" * 16
    assert not valid_steam64id(test_id)
