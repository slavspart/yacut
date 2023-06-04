from .models import URLMap


def is_unique(short):
    if short !='' and short != None:
        if URLMap.query.filter_by(short=short).first() is None:
            return True
        return False    
    return True

def latin_and_digits_length(short):
    if short !='' and short != None:
        if (short.isalnum() and short.isascii() and len(short) < 16):
            return True
        return False
    return True 
