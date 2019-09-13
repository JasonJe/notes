import os 
import pickle
import requests
import urllib
from git import Repo

path = './'
head_hexsha_path = './head'
r = Repo(path)
api_url = "https://www.yuque.com/api/v2"

token = os.environ.get('_YUQUE_') 
github_token = os.environ.get('_GITHUB_')

def get_repos(route):
    url = api_url + route
    headers = {
        'x-auth-token': token
    }
    response = requests.request("GET", url, headers=headers)
    return response.json().get('data', [])

def get_repo_detail(id_or_namespace):
    url = api_url + '/repos/' + id_or_namespace
    headers = {
        'x-auth-token': token
    }
    response = requests.request("GET", url, headers=headers)
    return response.json().get('data', [])

def get_repo_docs_list(id_or_namespace):
    url = api_url + '/repos/' + id_or_namespace + '/docs'
    headers = {
        'x-auth-token': token
    }
    response = requests.request("GET", url, headers=headers)
    return response.json().get('data', [])

def get_doc_detail(id_or_namespace, slug_or_id):
    url = api_url + '/repos/' + id_or_namespace + '/docs/' + slug_or_id
    headers = {
        'x-auth-token': token
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def get_github_repo_doc(route):
    url = 'https://raw.githubusercontent.com/JasonJe/notes/master/机器学习/监督学习.md'
    headers = {
        'Authorization': 'token ' + github_token
    }
    response = requests.request("GET", url, headers=headers)
    return response.text

def create_new_doc(id_or_namespace, title, body, slug = "", public = 0, format_ = "markdown"):
    data = "title=%s&slug=%s&public=%s&format=%s&body=%s" % (urllib.parse.quote(title), slug, str(public), format_, urllib.parse.quote(body))
    url = api_url + '/repos/' + id_or_namespace + '/docs'
    headers = {
        'x-auth-token': token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("POST", url, headers=headers, data=data, timeout=5000)
    return response.json()

def get_toc_data(id_or_namespace):
    url = api_url + '/repos/' + id_or_namespace + '/toc'
    headers = {
        'x-auth-token': token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def list_mkdfiles():
    files = []
    for i in os.walk(path):
        if i[2] != []:
            files.extend([os.path.join(i[0], j) for j in i[2] if j.rsplit(r'.')[-1].lower() == 'md'])
    return files

def list_commit_hexsha():
    hexshas = []
    for i in r.iter_commits():
        hexshas.append(i.hexsha)
    return hexshas

def diff_commit_files(old_commit_hexsha):
    change_files = r.git.diff(old_commit_hexsha, name_only = True)
    return [os.path.join(path, i) for i in change_files.split('\n') if i.rsplit(r'.')[-1].lower() == 'md']

def dump_hexsha():
    with open(head_hexsha_path, 'wb') as f:
        pickle.dump(r.head.commit.hexsha, f)

def load_hexsha():
    head_hexsha = ''
    with open(head_hexsha_path, 'rb') as f:
        head_hexsha = pickle.load(f)
    return head_hexsha

if __name__ == "__main__":
    repos = get_repos("/users/jasonje/repos")
    for repo in repos:
        repo_detail = get_repo_detail(repo['namespace'])
        # pprint.pprint(repo_detail)
        docs_list = get_repo_docs_list(str(repo['id']))
        # pprint.pprint(docs_list)
        if repo['name'] == 'NOTES':
            pprint.pprint(repo_detail['toc'])
            pprint.pprint(docs_list)
            # pprint.pprint(get_toc_data(str(repo['id'])))
        # if repo['name'] == "测试":
        #     pprint.pprint(docs_list)
        #     if docs_list == []:
        #         for i in r.iter_commits():
        #             print(i.message) 
