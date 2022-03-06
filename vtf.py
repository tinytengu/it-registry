import re
import os
import shutil
import argparse
import subprocess

PYTHON_PREFIX = "python" if os.name == "nt" else "python3"

FLASK_MAIN_TEMPLATE = """from flask import Flask, render_template

app = Flask(__name__)


@app.route(\"/\")
def index():
    return render_template(\"index.html\")


if __name__ == \"__main__\":
    app.run(host=\"0.0.0.0\", port=8080)
"""

PYTHON_GITIGNORE_TEMPLATE = """
env/
__pycache__/
.env
.pyc
"""


def init_out_dir(dir_path: str):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)

    os.mkdir(dir_path)
    os.mkdir(os.path.join(dir_path, "static"))
    os.mkdir(os.path.join(dir_path, "static", "assets"))
    os.mkdir(os.path.join(dir_path, "templates"))

    with open(os.path.join(dir_path, "main.py"), "w") as file:
        file.write(FLASK_MAIN_TEMPLATE)


def init_virtualenv(dest: str):
    subprocess.run([PYTHON_PREFIX, "-m", "venv", os.path.join(dest, "env")])


def init_git(dest: str):
    subprocess.run(["git", "init", "-q", "-b", "main", dest])


def get_files(source: str):
    return [
        os.path.abspath(os.path.join(dp, f))
        for dp, _, filenames in os.walk(source)
        for f in filenames
    ]


def copy_files(files: list, dest: str):
    for file in files:
        try:
            if file.endswith("index.html"):
                shutil.copy(file, os.path.join(dest, "templates"))
                continue

            if "favicon" in file:
                shutil.copy(file, os.path.join(dest, "static"))
                continue

            shutil.copy(file, os.path.join(dest, "static", "assets"))
        except shutil.SameFileError:
            continue


def format_index(filepath: str):
    with open(filepath, encoding="utf-8") as file:
        text = file.read()

    for match in re.finditer(r"(?:href|src)=\"(.+?)\"", text):
        uri = match.group(0).replace(
            match.group(1),
            "{{{{ url_for('static', filename='{}') }}}}".format(
                match.group(1).strip("/")
            ),
        )
        text = text.replace(match.group(0), uri)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(text)


def write_requirements(dest: str):
    result = subprocess.run(
        [
            os.path.join(dest, "env", "Scripts" if os.name == "nt" else "bin", "pip"),
            "freeze",
        ],
        stdout=subprocess.PIPE,
    )
    with open(os.path.join(dest, "requirements.txt"), "wb") as file:
        file.write(result.stdout)


def install_flask(dest: str):
    subprocess.run(
        [
            os.path.join(dest, "env", "Scripts" if os.name == "nt" else "bin", "pip"),
            "install",
            "flask",
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="VueJS to Flask app converter.")
    parser.add_argument(
        "--dist",
        "-d",
        dest="dist",
        type=str,
        help="dist folder path ('dist' by default)",
        default="dist",
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        type=str,
        help="output folder path ('flask' by default)",
        default="flask",
    )

    args = parser.parse_args()

    if not args.dist or not args.output:
        parser.print_help()
        return

    if not os.path.isdir(args.dist):
        print("[Error] Invalid dist folder path")
        return

    files = get_files(args.dist)
    print("Initializing folder structure...")
    init_out_dir(args.output)

    print("Copying and formatting files...")
    copy_files(files, args.output)
    format_index(os.path.join(args.output, "templates", "index.html"))

    print("Initializing Python virtual environment...")
    init_virtualenv(args.output)

    print("Installing Flask...")
    install_flask(args.output)

    print("Writing requirements.txt")
    write_requirements(args.output)

    print("Initializing git...")
    init_git(args.output)

    print("Writing .gitignore")
    with open(os.path.join(args.output, ".gitignore"), "w") as file:
        file.write(PYTHON_GITIGNORE_TEMPLATE.strip())


if __name__ == "__main__":
    main()
