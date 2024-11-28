import subprocess


def main():
    # 运行 isort
    subprocess.run(["isort", "."], check=True)
    # 运行 black
    subprocess.run(["black", "."], check=True)
    # 显示 git diff
    subprocess.run(["git", "diff", "origin/main"], check=True)
