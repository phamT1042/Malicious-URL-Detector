from urllib.parse import urlparse #module của thư viện urllib, được sử dụng để phân tích các thành phần của URL như scheme, netloc, path, params, query, và fragment
import tldextract #trích xuất các thành phần của một URL, bao gồm tên miền, tên miền cấp cao nhất (TLD), và tên miền phụ
import re #hỗ trợ cho các biểu thức chính quy (regular expressions)
from tld import get_tld # lấy top level domain (com, xyz, ...)
import string
import pandas as pd
import math
from collections import Counter

class FeatureExtraction:
  def __init__(self):
    self.alexa_domains = pd.read_csv("top-1m.csv", header=None).iloc[:, 1].values

  def IpAddress(self, url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        return 1
    else:
        return 0

  def UrlLength(self, url):
    return len(url)

  def HostnameLength(self, url):
    try:
      return len(urlparse(url).hostname)
    except:
      return 0

  def PathLength(self, url):
    try:
        parsed_url = urlparse(url)
        return len(parsed_url.path)
    except:
        return 0

  def QueryLength(self, url):
    try:
        parsed_url = urlparse(url)
        return len(parsed_url.query)
    except:
        return 0

  def UseShortService(self, url):
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

  def SusTlds(self, url):
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

  def NumSensitiveWords(self, url):
    words = ['number', 'update', 'fraud', 'spoof', 'bank', 'banking', 'paypal', 'spoofing', 'credit', 'confirm', 
            'free', 'webscr', 'payment', 'secure', 'PayPal', 'password', 'bonus', 'identity', 'lucky', 'social', 'money', 'account', 
            'transfer', 'ebayisapi', 'keylogger', 'card', 'verify', 'sign in', 'ssn', 'service', 'signin', 'login']
    word_count = sum(url.count(word) for word in words)
    return word_count

  def NumNumericChars(self, url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits += 1
    return digits

  def NumDots(self, url):
    return url.count('.')

  def NumDash(self, url):
    return url.count('-')

  def NumDashInHostname(self, url):
    try:
        url_info = tldextract.extract(url)
        hostname = url_info.domain
        return hostname.count('-')
    except:
        return 0
    
  def NumUnderscore(self, url):
    return url.count('_')

  def NumPercent(self, url):
    return url.count("%")

  def NumAmpersand(self, url):
    return url.count("&")

  def NumHash(self, url):
    return url.count("#")

  def NumQueryComponents(self, url):
    try:
        parsed_url = urlparse(url)
        return len(parsed_url.query.split('&')) if parsed_url.query else 0
    except:
        return 0
    
  def AtSymbol(self, url):
    return 1 if "@" in url else 0

  def TildeSymbol(self, url):
    return 1 if "~" in url else 0

  def DoubleSlashInPath(self, url):
    pos = url.rfind('//')
    if pos > 6:
      return 1 if pos > 7 else 0
    return 0

  def SubDomainLevel(self, url):
    try:
        url_info = tldextract.extract(url)
        subdomain = url_info.subdomain
        if subdomain:
            return subdomain.count('.') + 1
        else:
            return 0
    except:
        return 0

  def PathLevel(self, url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.path:
            return parsed_url.path.count('/') + 1
        else:
            return 0
    except:
        return 0

  def DomainInSubdomains(self, url):
    try:
        url_info = tldextract.extract(url)
        tld = get_tld(url, fail_silently=True)
        if tld:
            return 1 if tld in url_info.subdomain else 0
        else:
            return 1
    except:
        return 1

  def DomainInPaths(self, url):
    try:
        parsed_url = urlparse(url)
        tld = get_tld(url, fail_silently=True)
        if tld:
            return 1 if tld in parsed_url.path else 0
        else:
            return 1
    except:
        return 1

  def EntropyDomainName(self, url):
    try:
        hostname = urlparse(url).netloc
        counter = Counter(hostname)
        probabilities = [count / len(hostname) for count in counter.values()]
        return -sum(p * math.log2(p) for p in probabilities)
    except:
        return 0
    
  def rank_host(self, url):
    try:
        domain = tldextract.extract(url).registered_domain
        return 0 if domain in self.alexa_domains else 1
    except Exception:
        return 1
  