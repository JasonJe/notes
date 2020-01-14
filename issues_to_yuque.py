import os
import re
import requests
import urllib
import argparse

def get_github_labels():
    '''
    获取 Github 对应仓库全部 labels 数据
    
    Returns:
        labels 数据 | dict
    '''
    headers = {
        'Authorization':github_token
    }
    response = requests.get(github_api + 'labels', headers = headers)
    return response.json()

def get_github_detail_by_label(label):
    '''
    获取对应 label 的全部数据

    Args:
        label: 标签名  | str
    Returns:
        label 详细数据 | dict
    '''
    headers = {
        'Authorization':github_token
    }
    response = requests.get(github_api + 'issues', headers = headers, params = {'state': 'all', 'labels': label})
    return response.json()

def get_github_latest_issue():
    '''
    获取最新的一笔 issue

    Returns:
        issue 详细数据 | dict
    '''
    headers = {
        'Authorization':github_token
    }
    response = requests.get(github_api + 'issues', headers = headers, params = {'state': 'all', 'sort': 'updated', 'direction': 'desc'})
    return response.json()[0]

def get_github_all_issue():
    '''
    获取 issue 列表

    Returns:
        issue 详细数据 | dict
    '''
    headers = {
        'Authorization':github_token
    }
    response = requests.get(github_api + 'issues', headers = headers, params = {'state': 'all'})
    return response.json()

def get_yuque_repos_by_user_name(user):
    '''
    获取对应 label 的全部数据

    Args:
        user: 用户名       | str
    Returns:
        用户全部的仓库列表 | dict
    '''
    url = yuque_api + '/users/' + user + '/repos'
    headers = {
        'x-auth-token': yuque_token
    }
    response = requests.request("GET", url, headers = headers)
    return response.json().get('data', [])

def get_yuque_repo_detail(id_or_namespace):
    '''
    获取对应仓库的详细信息

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
    Returns:
        仓库的详细信息                                          | dict
    '''
    url = yuque_api + '/repos/' + id_or_namespace
    headers = {
        'x-auth-token': yuque_token
    }
    response = requests.request("GET", url, headers=headers)
    return response.json().get('data', [])

def get_yuque_repo_docs_list(id_or_namespace):
    '''
    获取对应仓库文章列表

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
    Returns:
        仓库的文章列表                                          | dict
    '''
    url = yuque_api + '/repos/' + id_or_namespace + '/docs'
    headers = {
        'x-auth-token': yuque_token
    }
    response = requests.request("GET", url, headers = headers)
    return response.json().get('data', [])

def get_yuque_doc_detail(id_or_namespace, slug_or_id):
    '''
    获取指定文档的详细数据

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
        slug_or_id:      文档 id 或 文档 slug                   | str
    Returns:
        文档的详细数据                                          | dict
    '''
    url = yuque_api + '/repos/' + id_or_namespace + '/docs/' + slug_or_id
    headers = {
        'x-auth-token': yuque_token
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def create_yuque_new_doc(id_or_namespace, title, body, slug = "", public = 0, format_ = "markdown"):
    '''
    创建新文档

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
        title:           文档标题                               | str
        body:            文档内容，markdown格式                 | str
        slug:            指定文档的 slug                        | str
        public:          是否公开，0 为不公开，1为公开           | int
        format_:         文档格式，默认为 markdown              | str
    Returns:
        文档的详细数据                                          | dict
    '''
    data = "title=%s&slug=%s&public=%s&format=%s&body=%s" % (urllib.parse.quote(title), urllib.parse.quote(slug), str(public), format_, urllib.parse.quote(body))

    url = yuque_api + '/repos/' + id_or_namespace + '/docs'

    headers = {
        'x-auth-token': yuque_token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("POST", url, headers=headers, data=data, timeout=5000)
    return response.json()

def update_yuque_doc(id_or_namespace, doc_id, title, body, slug = "", public = 0):
    '''
    更新文档

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
        doc_id:          文档 id                                | str
        title:           文档标题                               | str
        body:            文档内容，markdown格式                 | str
        slug:            指定文档的 slug                        | str
        public:          是否公开，0 为不公开，1为公开           | int
    Returns:
        文档的详细数据                                          | dict
    '''
    data = "title=%s&slug=%s&public=%s&body=%s&format=markdown" % (urllib.parse.quote(title), slug, str(public), urllib.parse.quote(body))
    url = yuque_api + '/repos/' + id_or_namespace + '/docs/' + doc_id
    headers = {
        'x-auth-token': yuque_token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("PUT", url, headers=headers, data=data, timeout=5000)
    return response.json()

def delete_yuque_doc(id_or_namespace, doc_id):
    '''
    删除文档

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
        doc_id:          文档 id                                | str
    Returns:
        文档的详细数据                                          | dict
    '''
    url = yuque_api + '/repos/' + id_or_namespace + '/docs/' + doc_id
    headers = {
        'x-auth-token': yuque_token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("DELETE", url, headers=headers, timeout=5000)
    return response.json()

def get_yuque_repo_toc_data(id_or_namespace):
    '''
    获取仓库目录

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
    Returns:
        目录的详细数据                                          | dict
    '''
    url = yuque_api + '/repos/' + id_or_namespace + '/toc'
    headers = {
        'x-auth-token': yuque_token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def generate_yuque_repo_toc_text(toc_data):
    '''
    生成仓库目录

    Args:
        toc_data: 文档的层级列表 | dict
    Returns:
        目录的详细数据           | dict
    '''
    template = '{}- [{}]({})\n'
    result = ''
    for i in toc_data:
        result += template.format(" " * (i['depth'] - 1) * 2, i['title'], i['slug'] if i['slug'] != "#" else "")
    return result

def update_yuque_repos_toc(id_or_namespace, toc_text):
    '''
    更新文档

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
        toc_text:        目录文案                               | str
    Returns:
        文档的详细数据                                          | dict
    '''
    data = "toc=%s" % (urllib.parse.quote(toc_text))
    url = yuque_api + '/repos/' + id_or_namespace
    headers = {
        'x-auth-token': yuque_token,
        'content-type': "application/x-www-form-urlencoded",
    }
    response = requests.request("PUT", url, headers=headers, data=data, timeout=5000)
    return response.json()

def generate_yuque_toc_data_by_issues_and_creste_doc(id_or_namespace):
    '''
    初始化使用，生成仓库目录数据和文章

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
    Returns:
        文档的详细数据                                          | dict
    '''
    labels = get_github_labels()
    issues_list = []
    for label in labels:
        issues_list.append({
            'title': label['description'],
            'slug': '#',
            'depth': 1
        })
        for detail in get_github_detail_by_label(label['name']):
            issues_list.append({
                'title': detail['title'],
                'slug' : str(detail['id']) + '_' + str(detail['number']),
                'depth': 2
            })
            resp = create_yuque_new_doc(id_or_namespace, detail['title'], detail['body'], slug = str(detail['id']) + '_' + str(detail['number']), public = is_public, format_ = "markdown")
            print(resp, str(detail['id']) + '_' + str(detail['number']))
    toc_text = generate_yuque_repo_toc_text(issues_list)
    update_yuque_repos_toc(id_or_namespace, toc_text)

def generate_yuque_toc_data_by_issues(id_or_namespace):
    '''
    结束更新使用，生成仓库目录数据

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
    Returns:
        文档的详细数据                                          | dict
    '''
    labels = get_github_labels()
    issues_list = []
    for label in labels:
        issues_list.append({
            'title': label['description'],
            'slug': '#',
            'depth': 1
        })
        for detail in get_github_detail_by_label(label['name']):
            issues_list.append({
                'title': detail['title'],
                'slug' : str(detail['id']) + '_' + str(detail['number']),
                'depth': 2
            })
    toc_text = generate_yuque_repo_toc_text(issues_list)
    print(toc_text)
    toc_result = update_yuque_repos_toc(id_or_namespace, toc_text)
    print(toc_result)

def create_yuque_doc_from_issue(id_or_namespace):
    '''
    新增 issue，同步更新到语雀
    issue 状态为 created

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
    Returns:
        更新结果，文档的详细数据                                | dict
    '''
    issue_data = get_github_latest_issue()
    create_result = create_yuque_new_doc(id_or_namespace, issue_data['title'], issue_data['body'], slug = str(issue_data['id']) + '_' + str(issue_data['number']), public = is_public, format_ = "markdown")
    print(create_result)

def delete_yuque_doc_from_issue(id_or_namespace):
    '''
    获取 issue 的更新，同步更新到语雀
    issue 状态为 edited

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
    Returns:
        更新结果，文档的详细数据                                | dict
    '''
    issue_data = get_github_all_issue()

    issue_id_list = []
    for issue in issue_data:
        issue_id_list.append(str(issue['id']) + '_' + str(issue['number']))
    
    docs_list  = get_yuque_repo_docs_list(id_or_namespace)
    need_to_delete_doc_id = []
    for doc in docs_list:
        if doc['slug'] not in issue_id_list:
            need_to_delete_doc_id.append(doc['id'])

    for doc_id in need_to_delete_doc_id:
        delete_result = delete_yuque_doc(id_or_namespace, str(doc_id))
        print(delete_result)

def create_yuque_doc_by_diff_issue(id_or_namespace):
    '''
    计算 issue 和语雀仓库的差别后，同步更新语雀仓库

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
    Returns:
        更新结果，文档的详细数据                                | dict
    '''
    issue_data = get_github_all_issue()
    docs_list  = get_yuque_repo_docs_list(id_or_namespace)
    docs_slug_list = [doc['slug'] for doc in docs_list]

    issue_id_list = []
    for issue in issue_data:
        issue_id = str(issue['id']) + '_' + str(issue['number'])
        if issue_id not in docs_slug_list:
            create_result = create_yuque_new_doc(id_or_namespace, issue['title'], issue['body'], slug = str(issue['id']) + '_' + str(issue['number']), public = is_public, format_ = "markdown")
            print(create_result)
        else:
            continue

def update_yuque_doc_from_issue(id_or_namespace):
    '''
    获取 issue 的更新，同步更新到语雀
    issue 状态为 edited

    Args:
        id_or_namespace: 仓库 id 或 用户名/仓库名 组合的命名空间 | str
    Returns:
        更新结果，文档的详细数据                                | dict
    '''
    issue_data = get_github_latest_issue()
    doc_detail = get_yuque_doc_detail(id_or_namespace, str(issue_data['id']) + '_' + str(issue_data['number']))
    update_result = update_yuque_doc(id_or_namespace, str(doc_detail['data']['id']), issue_data['title'], issue_data['body'], slug = str(issue_data['id']) + '_' + str(issue_data['number']), public = is_public)
    print(update_result)

if __name__ == "__main__":
    is_public = os.environ['ISPUBLIC']
    id_or_namespace = os.environ['YUQUE_REPO']
    yuque_api = os.environ['YUQUE_API']
    yuque_token = os.environ['YUQUE_TOKEN']

    github_api = os.environ['GITHUB_API']
    github_token = 'token ' + os.environ['GITHUB_TOKEN']

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--type", help="issue event type")
    args = parser.parse_args()

    if get_yuque_repo_docs_list(id_or_namespace) == []:
        print('init repo ...')
        generate_yuque_toc_data_by_issues_and_creste_doc(id_or_namespace)
    else:
        print('update repo diff between issues ...')
        create_yuque_doc_by_diff_issue(id_or_namespace)
    if args.type:
        latest_issue = get_github_latest_issue()
        if args.type == 'edited' or args.type == 'labeled':
            doc_detail = get_yuque_doc_detail(id_or_namespace, str(latest_issue['id']) + '_' + str(latest_issue['number']))
            print(doc_detail)
            if doc_detail.get('status', None) == 404:
                print('create doc ...')
                create_yuque_doc_from_issue(id_or_namespace)
            else:
                print('update doc ...')
                update_yuque_doc_from_issue(id_or_namespace)
        elif args.type == 'deleted':
            print('delete doc ...')
            delete_yuque_doc_from_issue(id_or_namespace)
        print('update repo toc ...')
        generate_yuque_toc_data_by_issues(id_or_namespace)