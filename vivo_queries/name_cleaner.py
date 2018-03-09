'''
The code, as well as VIVO, doesn't deal well with unusual characters. This cleans them.
If you come across a UnicodeEncodeError, add it to this list along with a replacement.
'''

def clean_name(result):
    clean_result = result.replace(u'\xa9', '(c)')
    clean_result = clean_result.replace(u'\xc2\x80\xc2\x93', '')
    clean_result = clean_result.replace(u"\xc3\xa2\xc2\x80\xc2\x98", "'")
    clean_result = clean_result.replace(u"\xc3\xa2\xc2\x80\xc2\x99", "'")
    clean_result = clean_result.replace(u'\xc3\x83\xc2\xaf', 'i')
    clean_result = clean_result.replace(u'\xc2\xa0', ' ')
    clean_result = clean_result.replace(u'\xc2\xae', '')
    clean_result = clean_result.replace(u'\xc3\xa2', '-')
    clean_result = clean_result.replace(u'\xe2\x80\x93', '-')
    clean_result = clean_result.replace(u'\xc3\x83\xc2\x83\xc3\x82\xc2\xb1', 'n')
    clean_result = clean_result.replace(u'\xed', 'i')
    clean_result = clean_result.replace(u'\xe1', 'a')
    clean_result = clean_result.replace(u'\xf1', 'n')
    clean_result = clean_result.replace(u'\xe9', 'e')
    clean_result = clean_result.replace(u'\xf3', 'o')
    clean_result = clean_result.replace(u'\xae', '(R)')
    clean_result = clean_result.replace(u'\u03b2', 'beta')
    clean_result = clean_result.replace(u'\xa0', ' ')
    return clean_result