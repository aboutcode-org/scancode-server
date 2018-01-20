import subprocess
import os
import virtualenv

req_path = os.path.abspath(os.path.join(os.pardir, 'scancode-server'))


def install_requirements():
    commands = ['pip', 'install', '-r', req_path + '/requirements.txt']
    subprocess.call(commands)


def create_venv():
    venv_dir = os.path.join(req_path, ".scancode-server")
    virtualenv.create_environment(venv_dir)
    activate_venv(venv_dir)


def activate_venv(venv_dir):
    bin_dir = os.path.join(venv_dir, "bin")
    activate_this = os.path.join(bin_dir, 'activate_this.py')
    with open(activate_this) as f:
        code = compile(f.read(), activate_this, 'exec')
        exec (code, dict(__file__=activate_this))
    install_requirements()


if __name__ == '__main__':
    create_venv()
