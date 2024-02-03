import os
import traceback

from decouple import config
from pathlib import Path
from subprocess import run as bashrun

try:
    print("Default var for upstream repo & branch will used if none were given!")
    ALWAYS_DEPLOY_LATEST = config(
        "ALWAYS_DEPLOY_LATEST",
        default=False,
        cast=bool)
    AUPR = config("ALWAYS_UPDATE_PY_REQ", default=False, cast=bool)
    UPSTREAM_REPO = config(
        "UPSTREAM_REPO",
        default="https://github.com/N-SUDY/Tg-encoder")
    UPSTREAM_BRANCH = config("UPSTREAM_BRANCH", default="main")

except Exception:
    print("Environment vars Missing")
    traceback.print_exc()


def varsgetter(files):
    evars = ""
    if files.is_file():
        with open(files, "r") as file:
            evars = file.read().rstrip()
            file.close()
    return evars


def varssaver(evars, files):
    if evars:
        file = open(files, "w")
        file.write(str(evars) + "\n")
        file.close()


r_filep = Path("Auto-rename.txt")
rvars = varsgetter(r_filep)
update_check = Path("update")

try:
    if ALWAYS_DEPLOY_LATEST is True or update_check.is_file():
        if os.path.exists('.git'):
            bashrun(["rm", "-rf", ".git"])
        update = bashrun([f"git init -q \
                       && git config --global user.email 117080364+Niffy-the-conqueror@users.noreply.github.com \
                       && git config --global user.name Niffy-the-conqueror \
                       && git add . \
                       && git commit -sm update -q \
                       && git remote add origin {UPSTREAM_REPO} \
                       && git fetch origin -q \
                       && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)
        if AUPR:
            bashrun(["pip3", "install", "-r", "requirements.txt"])
        if update.returncode == 0:
            print('Successfully updated with latest commit from UPSTREAM_REPO')
        else:
            print('Something went wrong while updating,maybe invalid upstream repo?')
        if update_check.is_file():
            os.remove("update")
        varssaver(rvars, r_filep)
    else:
        print("Auto-update is disabled.")
except Exception:
    traceback.print_exc()
