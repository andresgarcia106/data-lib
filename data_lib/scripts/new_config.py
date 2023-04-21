import os
import glob
import shutil

def main():
    """
    It copies a file from a directory that is two levels above the current working directory to the
    current working directory
    """
    cwd = os.getcwd() + "\\"
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_template = glob.glob(
        root_path + "/**/config_template.cfg", recursive=True
    )[0]

    shutil.copy2(config_template, cwd + "/config.cfg")


if __name__ == "__main__":
    main()
