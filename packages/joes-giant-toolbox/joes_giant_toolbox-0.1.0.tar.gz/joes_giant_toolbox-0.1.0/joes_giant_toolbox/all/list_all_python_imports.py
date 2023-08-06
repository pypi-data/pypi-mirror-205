import os
import re
import warnings


def list_all_python_imports(dir_path: str) -> dict:
    """Searches every python script in a given folder and lists all python modules imported within those scripts

    (see "Example Usage")

    Parameters
    ----------
    dir_path: str
        Folder in which to find the python scripts

    Notes
    -----
    Package import statements are only searched for in files ending with .py or .ipynb
    Lines starting with a hash (i.e. commented lines) are ignored
    Any line of a script on which no modules were found although the line contains the word "import" raises a warning

    Example Usage
    -------------
    >>> from pprint import pprint
    >>> imports_found_dict = list_all_python_imports( os.getcwd() )
    >>> pprint(imports_found_dict)
    ...

    Returns
    -------
    dict
        {file_name: tuple_of_module_names}
        Dictionary, with key=filename and values=(tuple containing list of modules found)
    """
    results_dict = {
        filename: f"{dir_path}/{filename}"
        for filename in os.listdir(dir_path)
        if filename != "list_all_python_imports.py"
        and (filename[-3:] == r".py" or filename[-6:] == r".ipynb")
    }

    for script in results_dict:
        with open(results_dict[script], "r") as f:
            temp_readlines = f.readlines()

        imports_found = []
        for line in temp_readlines:
            words_in_line = line.strip().split()
            if len(words_in_line) > 0:
                if words_in_line[0] == "#":
                    # ignore lines starting with a comment
                    pass
                elif words_in_line[0] == "import":
                    imports_found.append(words_in_line[1])
                elif words_in_line[0] == "from" and words_in_line[2] == "import":
                    imports_found.append(words_in_line[1])
                elif re.search(r"\bimport\b", line):
                    if ">>>" not in line:
                        warnings.warn(
                            f"possible import missed due to unexpected import pattern: {script} {line}"
                        )

        results_dict[script] = tuple(set(imports_found))
        del imports_found, temp_readlines

    return results_dict
