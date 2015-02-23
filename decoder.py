import unicodedata


def decode(input_str):
     input_str = input_str.decode('latin-1')
     nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
     return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])