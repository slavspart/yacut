from .models import URLMap


def is_unique(short):
    if short != '' and short is not None:
        if URLMap.query.filter_by(short=short).first() is None:
            return True
        return False
    return True


def latin_and_digits_length(short):
    if short != '' and short is not None:
        if (short.isalnum() and short.isascii() and len(short) < 16):
            return True
        return False
    return True
