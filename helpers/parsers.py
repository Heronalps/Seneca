import re, os

def parse_path(current_path, keyword):
    return re.search('.*'+ keyword, current_path).group(0)