import requests as r,re
def gw(t1,t2,s):
    try:
        regexPattern = t1 + '(.+?)' + t2
        str_found = re.search(regexPattern,s).group(1)
        return str_found.strip()
    except AttributeError:
        return 'Null'
def getname():
    s = r.post("https://api.name-fake.com/indonesia/female/",headers={'Content-Type':'application/x-www-form-urlencoded','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'},data='con%5B%5D=id_ID&perc=100&miny=19&maxy=57')
    if s.text:
        return gw('<h2 style="text-align:center;padding: 1rem;">','</h2>',s.text)
    else: getname()

