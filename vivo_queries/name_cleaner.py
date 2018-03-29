'''
Python2 doesn't play well with unusual unicode characters. Some VIVO instances may also have issues.
This tool cleans out those bad characters. If you come across a UnicodeEncodeError, add it to this list along with a replacement.
You can also add any other characters you don't want (for instance, Web of Science escapes &, which cause '/&' to appear after upload.)
The full_clean is used for string matching and so should be more strict.
'''

def clean_name(result):
    clean_result = result.replace(' \\&', ' &')
    clean_result = clean_result.replace('\n', ' ')
    clean_result = clean_result.replace('"', '\\"')
    return clean_result

def full_clean(result):
    clean_result = clean_name(result)
    clean_result = clean_result.replace(u'\xa9', '(c)')
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
    clean_result = clean_result.replace(u'\xf6', 'o')
    clean_result = clean_result.replace(u'\xfc', 'u')
    clean_result = clean_result.replace(u'\xe4', 'a')
    clean_result = clean_result.replace(u'\xfa', 'u')
    clean_result = clean_result.replace(u'\xd6', 'o')
    # clean_result = clean_result.replace(u'\xc1', 'A')
    clean_result = clean_result.replace(u'\xf2', 'o')
    clean_result = clean_result.replace(u'\xe3', 'a')
    clean_result = clean_result.replace(u'\xe7', 'c')
    clean_result = clean_result.replace(u'\xe0', 'a')
    clean_result = clean_result.replace(u'\xe8', 'e')

    return clean_result