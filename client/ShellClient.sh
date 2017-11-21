#!/bin/bash
#
# Shell Client
#

params=$1
# 格式 'key1=value, key2=value,...'

function make_url() {
    python -c "
import hashlib, datetime, time, re
version='v1'
accesskey_id='demo_id'
accesskey_secret='demo_secret'
md5 = lambda pwd: hashlib.md5(pwd).hexdigest()
comma_pat = re.compile(r'\s*,\s*')
get_current_timestamp = lambda: int(time.mktime(datetime.datetime.now().timetuple()))
def _sign(parameters):
    cqs, _my_sorted = '',sorted(parameters.items(), key=lambda parameters: parameters[0])
    for (k, v) in _my_sorted:cqs += '{}={}&'.format(k,v)
    cqs += accesskey_secret
    return md5(cqs).upper()
def make_url(params=''):
    uri, params = '', dict([i.split('=') for i in re.split(comma_pat, params.strip()) if i])
    for k,v in dict(accesskey_id=accesskey_id, version=version, timestamp=get_current_timestamp()-5).iteritems(): params[k] = v
    for k,v in params.iteritems():uri += '{}={}&'.format(k,v)
    uri += 'signature=' + _sign(params)
    print uri
make_url('${params}')
"
}

curl -sL "http://127.0.0.1:1798/?$(make_url)"
echo