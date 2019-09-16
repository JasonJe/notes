import os
import re
import requests
import urllib
from git import Repo

path = './'
r = Repo(path)
api_url = "https://www.yuque.com/api/v2"

repo_id = os.environ.get('_YUQUE_REPO_ID_')
token = os.environ.get('_YUQUE_TOKEN_') 
github_token = os.environ.get('_GITHUB_TOKEN_')

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

def create_new_doc(id_or_namespace, title, body, slug = "", public = 0, format_ = "markdown"):
    data = "title=%s&slug=%s&public=%s&format=%s&body=%s" % (urllib.parse.quote(title), slug, str(public), format_, urllib.parse.quote(body))
    url = api_url + '/repos/' + id_or_namespace + '/docs'
    headers = {
        'x-auth-token': token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("POST", url, headers=headers, data=data, timeout=5000)
    return response.json()

def update_doc(id_or_namespace, doc_id, title, body, slug = "", public = 0):
    data = "title=%s&slug=%s&public=%s&body=%s" % (urllib.parse.quote(title), slug, str(public), urllib.parse.quote(body))
    url = api_url + '/repos/' + id_or_namespace + '/docs/' + doc_id
    headers = {
        'x-auth-token': token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("PUT", url, headers=headers, data=data, timeout=5000)
    return response.json()

def get_repo_toc_data(id_or_namespace):
    url = api_url + '/repos/' + id_or_namespace + '/toc'
    headers = {
        'x-auth-token': token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def generate_toc_text(toc_data):
    template = '{}- [{}]({})\n'
    result = ''
    for i in toc_data:
        result += template.format(" " * (i['depth'] - 1) * 2, i['title'], i['slug'] if i['slug'] != "#" else "")
    return result

def update_repos_toc(id_or_namespace, toc_text):
    data = "toc=%s" % (urllib.parse.quote(toc_text))
    url = api_url + '/repos/' + id_or_namespace
    headers = {
        'x-auth-token': token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("PUT", url, headers=headers, data=data, timeout=5000)
    return response.json()

def generate_toc_data(index_file):
    with open(index_file, 'r') as f:
        index_body = f.read()
    doc_list = []
    for i in re.findall('(\d\..*<\/strong><\/summary>|#{4}.*)', index_body):
        if '</strong></summary>' in i:
            doc_list.append({
                'slug': '#',
                'depth': 1,
                'title': i.replace('</strong></summary>', ''),
                'file_path': ''
            })
        else:
            slug_repx = re.match('\d+\.\d+', i.replace('#### ', ''))
            if slug_repx is not None:
                file_path_repx = re.match('.*\.md', i)
                slug = i.replace('#### ', '')[slug_repx.span()[0] : slug_repx.span()[1]]
                doc_list.append({
                    'slug': slug,
                    'depth': 2,
                    'title': slug + ' ' + i.replace('#### ', '').split('[')[1].split(']')[0].replace('`', '') if '[' in i else i.replace('#### ', '').replace('`', ''),
                    'file_path': os.path.join(path, i[file_path_repx.span()[0]: file_path_repx.span()[1]].rsplit('(')[-1]) if file_path_repx is not None else ''
                })
    return doc_list[:-1]

def diff_repo_and_local(docs_list, toc_data):
    doc_set = set([i['title'] for i in docs_list])
    toc_set = set([i['title'] for i in toc_data if i['depth'] != 1])
    return toc_set - doc_set

def list_mkdfiles():
    files = []
    for i in os.walk(path):
        if i[2] != []:
            files.extend([os.path.join(i[0], j) for j in i[2] if j.rsplit(r'.')[-1].lower() == 'md' and 'README' not in j])
    return files

def list_commit_hexsha():
    hexshas = []
    for i in r.iter_commits():
        hexshas.append(i.hexsha)
    return hexshas

def diff_commit_files(old_commit_hexsha):
    change_files = r.git.diff(old_commit_hexsha, name_only = True)
    return [os.path.join(path, i) for i in change_files.split('\n') if i.rsplit(r'.')[-1].lower() == 'md']

if __name__ == "__main__":
    index_file = os.path.join(path, 'README.md')
    toc_data = generate_toc_data(index_file)
    toc_text = generate_toc_text(toc_data)
    resp = update_repos_toc(repo_id, toc_text)
    print('Update toc: ', resp)
    image_base_url = 'https://raw.githubusercontent.com/'
    for url in r.remote().urls:
        image_base_url = url.replace('.git', '').replace('https://github.com/', image_base_url)

    docs_list = get_repo_docs_list(repo_id)
    diff_docs = diff_repo_and_local(docs_list, toc_data)
    print('Diff doc between repo and local is: ', diff_docs) 
    
    for i in toc_data:
        if i['title'] in diff_docs and i['file_path'] != '':
            body = ''
            with open(i['file_path'], 'r') as f:
                body = f.read()
            body = body.replace('../assets/images/', image_base_url + '/master/assets/images/')
            resp = create_new_doc(repo_id, i['title'], body, slug = i['slug'], public = 0)
            print('Create new doc response: ', i['title'])

    hexshas = list_commit_hexsha()
    repo_hexsha = hexshas[1]
    update_files = diff_commit_files(repo_hexsha)

    update_files_slug = []
    for i in toc_data:
        if i['file_path'] in update_files:
            update_files_slug.append(i)

    for i in update_files_slug:
        doc_detail = get_doc_detail(repo_id, i['slug'])
        doc_id = str(doc_detail['data']['id'])
        body = ''
        with open(i['file_path'], 'r') as f:
            body = f.read()
        body = body.replace('../assets/images/', image_base_url + '/master/assets/images/')
        resp = update_doc(repo_id, doc_id, i['title'], body, slug = i['slug'], public = 0)
        print('Update doc: ', i['title'])
