import os
import glob
import shutil
import sys
import getopt


def get_args(argv):
    """
    It takes the command line arguments and returns the filename

    :param argv: This is the list of command-line arguments
    :return: The filename
    """
    arg_file_name = ""
    arg_help = "{0} -n <filename>".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "h:n:", ["help", "filename="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-n", "--filename"):
            arg_file_name = arg

    return arg_file_name


def main():
    """
    It takes the name of the notebook template, copies it to the current working directory, and renames
    it to the name specified by the user
    """
    cwd = os.getcwd() + "\\"
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    notebook_template = glob.glob(
        root_path + "/**/jupyter_notebook_sample.ipynb", recursive=True
    )[0]

    if get_args(sys.argv) != "":
        notebook_new_name = get_args(sys.argv)
        shutil.copy2(notebook_template, cwd + f"{notebook_new_name}.ipynb")
    else:
        shutil.copy2(notebook_template, cwd)


if __name__ == "__main__":
    main()
