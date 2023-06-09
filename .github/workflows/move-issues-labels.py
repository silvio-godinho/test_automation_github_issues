import os
import requests
import json

def move_issues():
    access_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('REPO_NAME')

    if not access_token:
        raise ValueError('Variável de ambiente GITHUB_TOKEN não definida.')

    if not repo_name:
        raise ValueError('Variável de ambiente REPO_NAME não definida.')

    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    url = f'https://api.github.com/repos/{repo_name}/issues'

    params = {'state': 'open'}
    response = requests.get(url, headers=headers, params=params)
    issues = json.loads(response.text)

    for issue in issues:
        issue_number = issue['number']
        labels_url = f'https://api.github.com/repos/{repo_name}/issues/{issue_number}/labels'
        labels_response = requests.get(labels_url, headers=headers)
        labels = json.loads(labels_response.text)
        label_names = [label['name'] for label in labels]

        if 'marretada' in label_names:
            issue_data = {'state': 'closed'}
            update_url = f'https://api.github.com/repos/{repo_name}/issues/{issue_number}'
            response = requests.patch(update_url, headers=headers, data=json.dumps(issue_data))

            if response.status_code == 200:
                print(f"A issue #{issue_number} foi fechada com sucesso!")
            else:
                print(f"Ocorreu um erro ao fechar a issue #{issue_number}. Código de status: {response.status_code}")
        else:
            print(f"A issue #{issue_number} não possui a label 'bug'. Não será fechada.")

# Chamar a função para mover as issues
move_issues()