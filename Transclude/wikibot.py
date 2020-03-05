import requests
import json

def read_wiki(session, api_url, title):
    res = session.post(api_url, data={'format': 'json', 'action': 'query', 'assert': 'user', 'titles': title, 'prop': 'revisions', 'rvprop': 'content'})
    
    ret = json.loads(res.text)['query']['pages']
    for k in ret:
        ret = ret[k]
        break
    
    return ret["revisions"][0]["*"]
    
def read_wiki_sec(session, api_url, title, sec):
    res = session.post(api_url, data={'format': 'json', 'action': 'query', 'assert': 'user', 'titles': title, 'prop': 'revisions', 'rvprop': 'content', 'rvsection': sec})
    
    ret = json.loads(res.text)['query']['pages']
    for k in ret:
        ret = ret[k]
        break
    
    return ret["revisions"][0]["*"]

def write_wiki(session, api_url, title, text, summary, **others):
    token = session.get(api_url, params={'format': 'json', 'action': 'query', 'meta': 'tokens',})
    post_data = {'format': 'json', 'action': 'edit', 'assert': 'user', 'text': text, 'summary': summary, 'title': title, 'token': token.json()['query']['tokens']['csrftoken'], 'minor': 1}
    for k in others:
        post_data[k] = others[k]
    r = session.post(api_url, data=post_data)
    print(r.text)
    
def write_wiki_sec(session, api_url, title, sec, text, summary, **others):
    token = session.get(api_url, params={'format': 'json', 'action': 'query', 'meta': 'tokens',})
    post_data = {'format': 'json', 'action': 'edit', 'assert': 'user', 'text': text, 'summary': summary, 'title': title, 'section': sec, 'token': token.json()['query']['tokens']['csrftoken']}
    for k in others:
        post_data[k] = others[k]
    r = session.post(api_url, data=post_data)
    print(r.text)

def login_wiki(username, password, api_url):
    session = requests.Session()
    lgtoken = session.get(api_url, params={'format': 'json', 'action': 'query', 'meta': 'tokens', 'type': 'login',})
    
    lgtoken.raise_for_status()
    res = session.post(api_url, data={'format': 'json', 'action': 'login', 'lgname': username, 'lgpassword': password, 'lgtoken': lgtoken.json()['query']['tokens']['logintoken'],})
    if res.json()['login']['result'] != 'Success':
        raise RuntimeError(res.json()['login']['reason'])
        
    return session
    
def transcludedin(session, api_url, title, namespace):
	res = session.post(api_url, data={'format': 'json', 'action': 'query', 'assert': 'bot', 'titles': title, 'prop': 'transcludedin', 'tinamespace': namespace, "tilimit": "max"})
	ret = json.loads(res.text)['query']['pages']
	
	for k in ret:
		ret = ret[k].get('transcludedin')
		break
	
	if ret is not None:
		temp = list()
		for v in ret:
			temp.append(v['title'])
	else:
		temp = list()
		
	return temp