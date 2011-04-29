import re, urllib
import simplejson as json
from django.utils.encoding import force_unicode



class UrlOpener(urllib.FancyURLopener):
    version = "py-gtranslate/1.0"

base_uri = "http://ajax.googleapis.com/ajax/services/language/translate"

def translate(phrase, src="id", to="en"):
    if src == to:
        return phrase
    data = urllib.urlencode({'v': '1.0', 'langpair': '%s|%s' % (src, to), 'q': phrase.encode('utf-8')})
    resp = json.load(UrlOpener().open('%s?%s' % (base_uri, data)))
    try:
        return resp['responseData']['translatedText']
    except:
        return ""

def tr(kalimat, request):
    to = request.session.get('lang','id')
    return translate(kalimat, to=to)


########################################################
# Money format                                         # 
# Gubahan dari django/contrib/templatetags/humanize.py #
# dengan menambahkan pemisah ribuan.                   #
########################################################
"""
Converts an integer to a string containing commas every three digits.
For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
"""
def _money(value, separator):
    orig = force_unicode(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>%s\g<2>' % separator, orig)
    if orig == new:
        return new
    return _money(new, separator)

def money(value, separator="."):
    return _money(str(int(float(value))), separator)

