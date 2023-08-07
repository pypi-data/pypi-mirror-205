import os
import shutil
from configparser import ConfigParser
from pip._internal.cli.main import main as pipmain

CONFIG_FILE = ".aws_lambda_mess"
REQUIREMENTS_FILE = "requirements.txt"
GITIGNORE_FILE = ".gitignore"
APP_FILE = "app.py"

def new(dirname):
    print('Running new', dirname)

    if os.path.isdir(dirname):
        print(f"[{dirname}] already exists.")
        exit(1)

    os.mkdir(dirname)
    os.chdir(dirname)
    try:
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'init_files', CONFIG_FILE), CONFIG_FILE)
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'init_files', REQUIREMENTS_FILE), REQUIREMENTS_FILE)
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'init_files', GITIGNORE_FILE), GITIGNORE_FILE)
        os.mkdir("src")
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'init_files', APP_FILE), os.path.join("src", APP_FILE))
        os.mkdir("package")
        os.mkdir("dist")
        os.mkdir("tests")
    except Exception as e:
        print(e)
        os.chdir("..")
        exit(1)


    #framework_dir = os.path.join(os.path.dirname(__file__), "framework")
    #files = [file_name for file_name in os.listdir(framework_dir) if file_name not in ["__pycache__"]]
    #for file in files:
    #    print(f"{os.path.join(framework_dir,file)}")

def build():
    print('Running build', __file__ )
    if not os.path.isfile(CONFIG_FILE):
        print("Project not initialised. Please run init")
        exit(1)

    if not os.path.isdir("./build"):
        os.mkdir("./build")
    if not os.path.isdir("./build/aws_lambda_mess"):
        os.mkdir("./build/aws_lambda_mess")

    cfg = ConfigParser()
    cfg.read(CONFIG_FILE)
    cfg_source = cfg.get('main', 'source')
    cfg_package = cfg.get('main', 'package')

    shutil.copytree(cfg_source, "./build/aws_lambda_mess", dirs_exist_ok=True)

    shutil.make_archive("./dist/package", "zip", "./build/aws_lambda_mess")
    pipmain(['install',"--upgrade","--target=./build/aws_lambda_mess/package","pymysql"])


def run():
    import argparse

    parser = argparse.ArgumentParser(description="aws lambda mess")
    subparsers = parser.add_subparsers(dest='subparser')

    new_parser = subparsers.add_parser('new')
    new_parser.add_argument('dirname')
    build_parser = subparsers.add_parser('build')

    kwargs = vars(parser.parse_args())
    globals()[kwargs.pop('subparser')](**kwargs)


if __name__ == "__main__":
    run()
