import subprocess
import sys


def check_vacuum():
    try:
        subprocess.check_call(["which", "vacuum"])
        return True
    except subprocess.CalledProcessError:
        return False


def install_vacuum():
    try:
        subprocess.check_call(["/bin/sh", "-c", "curl -fsSL https://quobix.com/scripts/install_vacuum.sh | sh "])
    except subprocess.CalledProcessError:
        sys.exit("Failed to install vacuum")


def vacuum(args):
    try:
        subprocess.check_call(["vacuum"] + args)
    except subprocess.CalledProcessError as e:
        sys.exit("Error running vacuum: " + str(e))


if not check_vacuum():
    install_vacuum()


def main():
    vacuum(["help"])


if __name__ == "__main__":
    main()
