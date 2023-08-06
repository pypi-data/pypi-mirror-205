import os

import requests
from jinja2 import Environment, FileSystemLoader


class SetUp:
    def __init__(self):
        self.__dir = os.getcwd()
        self.__create_github_dir()
        self.__create_workflows_dir()
        self.__create_gitignore()
        self.__create_license()
        self.__create_readme()
        self.__create_git_hook()

    def __create_github_dir(self):
        github_dir = os.path.join(self.__dir, '.github')
        if not os.path.exists(github_dir):
            os.mkdir(github_dir)

    def __create_workflows_dir(self):
        workflows_dir = os.path.join(self.__dir, '.github', 'workflows')
        if not os.path.exists(workflows_dir):
            os.mkdir(workflows_dir)

    def __create_gitignore(self):
        file_path = os.path.join(self.__dir, '.gitignore')
        if not os.path.exists(file_path):
            with open(file_path, 'a+', encoding='utf-8') as f:
                f.write('.idea\n')

    def __create_license(self):
        file_path = os.path.join(self.__dir, 'LICENSE')
        if not os.path.exists(file_path):
            with open(file_path, 'a+', encoding='utf-8') as f:
                f.write('MIT License\n')

    def __create_readme(self):
        file_path = os.path.join(self.__dir, 'README.md')
        if not os.path.exists(file_path):
            with open(file_path, 'a+', encoding='utf-8') as f:
                f.write('# {name}\n'.format(name=os.path.basename(self.__dir)))

    def __create_git_hook(self):
        git_dir = os.path.join(self.__dir, '.git')
        if not os.path.exists(git_dir):
            os.system('git init')
        hook_dir = os.path.join(self.__dir, '.git', 'hooks')
        if not os.path.exists(hook_dir):
            os.mkdir(hook_dir)
        file_path = os.path.join(hook_dir, 'pre-commit')
        if not os.path.exists(file_path):
            res = requests.get(
                'https://gist.githubusercontent.com/wgnpj2cg/bc4ffb641cebfc76eb90dfdef2929427/raw/fa69f61dac913c932676049d00807e55f45c29d1/pre-commit').text
            with open(file_path, 'a+', encoding='utf-8') as f:
                f.write(res)

    def create_python(self):
        env = Environment(loader=FileSystemLoader(searchpath='templates'))
        tmpl = env.get_template('python_docker_build_publish.tpl')
        with open(os.path.join(self.__dir, '.github', 'workflows', 'python_docker_build_publish.yaml'), 'a+') as f:
            f.write(tmpl.render())


# if __name__ == '__main__':
#     su = SetUp()
#     type = {
#         '1': 'python',
#         '2': 'java',
#     }
#     for k, v in type.items():
#         print(k, v)
#     t = input('please input type:')
#     if t == '1':
#         su.create_python()
