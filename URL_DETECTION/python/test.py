import math
from urllib.parse import urlparse #module của thư viện urllib, được sử dụng để phân tích các thành phần của URL như scheme, netloc, path, params, query, và fragment
import tldextract #trích xuất các thành phần của một URL, bao gồm tên miền, tên miền cấp cao nhất (TLD), và tên miền phụ
import re #hỗ trợ cho các biểu thức chính quy (regular expressions)
from tld import get_tld
import string
import textwrap
from collections import Counter
def EntropyHostName(url):
    try:
        hostname = urlparse(url).netloc
        counter = Counter(hostname)
        probabilities = [count / len(hostname) for count in counter.values()]
        return -sum(p * math.log2(p) for p in probabilities)
    except:
        return 0

print(type(EntropyHostName("https://www.youtube.com/results?search_query=c%E1%BA%A5u+tr%C3%BAc+url")))