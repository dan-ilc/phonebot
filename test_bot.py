from twilio_client import is_valid_message, is_valid_uk_phone_number

def test_valid_phone_number():
    """
    Can we check the length, extension, and country code
    """
    assert is_valid_uk_phone_number("+447840222943")
    assert is_valid_uk_phone_number("07840222964")
    assert is_valid_uk_phone_number("02078402222")
    assert is_valid_uk_phone_number("0207840AAA2222")
    assert not is_valid_uk_phone_number("0207840222222")
    assert not is_valid_uk_phone_number("+107840222222")

def test_valid_message():
    """
    Can we check the length of a message
    """
    assert is_valid_message("Hi there")
    assert not is_valid_message("Hi"*10000)
    assert not is_valid_message("my main man musk")


