import re, os

def parse_path(current_path, keyword):
    return re.search('.*'+ keyword, current_path).group(0)

def split_path(path):
    # This regex captures filename after the last backslash
    filename = re.search("(?!\/)(?:.(?!\/))*(?=\.\w*$)", path).group(0)
    path_prefix = re.search("(.*\/)(?!.*\/)", path).group(0)
    
    return path_prefix, filename