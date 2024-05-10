from urllib.parse import urlparse #module của thư viện urllib, được sử dụng để phân tích các thành phần của URL như scheme, netloc, path, params, query, và fragment
import tldextract #trích xuất các thành phần của một URL, bao gồm tên miền, tên miền cấp cao nhất (TLD), và tên miền phụ
import re #hỗ trợ cho các biểu thức chính quy (regular expressions)
from tld import get_tld # lấy top level domain (com, xyz, ...)
import string
import pandas as pd

class FeatureExtraction:
  def __init__(self):
    self.alexa_domains = pd.read_csv("top-1m.csv", header=None).iloc[:, 1].values

  def haveIP(self, url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        return 1
    else:
        return 0

  def lenURL(self, url):
    return len(url)

  def lenHostname(self, url):
    try:
      return len(urlparse(url).hostname)
    except:
      return 0

  def tinyURL(self, url):
    #listing shortening services
    shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                          r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                          r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                          r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                          r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                          r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                          r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                          r"tr\.im|link\.zip\.net"

    return 1 if re.search(shortening_services,url) else 0

  def abnormal_url(self, url):
    hostname = urlparse(url).hostname
    hostname = str(hostname).lower()
    try:
      match = re.search(hostname, url.lower())
      return 0 if match else 1
    except:
      return 1

  def suspicious_tlds(self, url):
    suspicious_tlds = [
      'tk', 'pw', 'info', 'biz', 'xyz', 'top', 'club', 'work', 'online',
      'site', 'website', 'space', 'click', 'link', 'download', 'trade', 'cn'
      'review', 'party', 'win', 'stream', 'gdn', 'racing', 'science', 'net'
      'gq', 'icu', 'ooo', 'mobi', 'fun', 'buzz', 'kim', 'ga', 'cf', 'org', 'ml', 'co', 'ru'
    ]
    try:
      tld = get_tld(url)
      if tld in suspicious_tlds: return 1
      else: return 0
    except:
      return 1

  def digit_count(self, url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits


  def letter_count(self, url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters

  def special_chars_count(self, url):
    special_chars = set(string.punctuation)
    num_special_chars = sum(char in special_chars for char in url)
    return num_special_chars

  def haveAtSign(self, url):
    return 1 if "@" in url else 0

  def haveDash(self, url):
    return 1 if '-' in urlparse(url).netloc else 0

  def redirection(self, url):
    pos = url.rfind('//')
    if pos > 6:
      return 1 if pos > 7 else 0
    return 0

  def subDomains(self, url):
    url = str(url)
    url = url.replace("www.", "")
    url = url.replace("." + tldextract.extract(url).suffix, "")
    count = url.count(".")
    return 1 if count > 1 else 0
  
  def rank_host(self, url):
    try:
        domain = tldextract.extract(url).registered_domain
        return 1 if domain in self.alexa_domains else 0
    except Exception:
        return 0