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

def create_directories(prj_dir, prj_sub_dir):
    
    # custom project name
    if get_args(sys.argv) != "":   
        # create project directories     
        project_name = get_args(sys.argv)
        os.mkdir(project_name)
        for prt_dir in prj_dir:
            os.mkdir(project_name + "\\" + prt_dir)
        # create project subdirectories
        if os.path.isdir(project_name + "\\" + "02_data"):
            for prt_sub_dir in prj_sub_dir:
                os.mkdir(project_name + "\\" + "02_data" + "\\" + prt_sub_dir)

    else:
        # create project directories
        project_name = "python_data_project"
        os.mkdir(project_name)
        for prt_dir in prj_dir:
            os.mkdir(project_name + "\\" + prt_dir)
        # create project subdirectories
        if os.path.isdir(project_name + "\\" + "02_data"):
            for prt_sub_dir in prj_sub_dir:
                os.mkdir(project_name + "\\" + "02_data" + "\\" + prt_sub_dir) 
    return project_name

def generate_cfg(path):
    """
    It copies a file from a directory that is two levels above the current working directory to the
    current working directory
    """
    cwd = os.getcwd() + "\\"
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_template = glob.glob(
        root_path + "/**/config_template.cfg", recursive=True
    )[0]

    shutil.copy2(config_template, cwd + f"{path}/config.cfg")
    
def generate_nb(path):
    """
    It takes the name of the notebook template, copies it to the current working directory, and renames
    it to the name specified by the user
    """
    cwd = os.getcwd() + "\\"
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    notebook_template = glob.glob(
        root_path + "/**/notebook_template.ipynb", recursive=True
    )[0]

    
    notebook = "jupyter_notebook_sample"
    shutil.copy2(notebook_template, cwd +  f"{path}/01_notebooks/{notebook}.ipynb")

def main():
    """
    It takes the name of the notebook template, copies it to the current working directory, and renames
    it to the name specified by the user
    """
    cwd = os.getcwd() + "\\"
    
    project_directories = ["01_notebooks","02_data","03_src","04_data_models"]
    project_subdirectories = ["01_input_files","02_input_query","03_stage_files","04_output_files","04_archived_files"]
    
    # create directories    
    root_path = create_directories(project_directories, project_subdirectories)     
    
    # place initial files
    generate_cfg(root_path)
    generate_nb(root_path)
    


if __name__ == "__main__":
    main()
