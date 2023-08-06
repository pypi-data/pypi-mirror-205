from datetime import datetime
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from urllib.request import urlopen
import glob
import importlib
import json
import nbformat
import os
import shutil
import sys

# default values
FOLDER = "datamachine_temp"
INDEX = "https://colab.research.google.com/drive/1QE92tEB94X0xLT5AfQf_Hcn1mVK1VkG5"
LIBRARY = "benevolent"
NUMBER = 100000

# set current values
_folder = FOLDER
_index = INDEX
_library = LIBRARY
_number = NUMBER

_notebooks = []


def cache_notebook(path, library=None, index=None, force_reload=False):

    global _notebooks, _number, _library, _index
    notebook = {}

    # check for a cached entry
    for n in _notebooks:
        if n["path"] == path:
            notebook = n
            if not force_reload:
                return notebook
            break 

    # determine how to access the notebook
    # TODO: add support for reading notebooks with credentials
    if path.startswith("https://colab"):
        file_id = path.split("/")[-1]  # get the file id
        file_id = file_id.split("?")[0]  # trim out any arguments
        url = "https://docs.google.com/uc?export=download&id="
        url = url + file_id
        notebook["pull"] = url
    elif path.startswith("https://github"):
        url = path.replace("github.com", "raw.githubusercontent.com")
        notebook["pull"] = url
    elif path.startswith("https:"):
        notebook["pull"] = path
    elif path.endswith(".ipynb"):
        notebook["pull"] = path
    else:  # assume we are left with a library and index to search

        if library is None:
            library = _library
        if ":" in library or "." in library:  # direct to library
            library_path = library
        else:  # lookup library in index
            if index is None:
                index = _index
            idx = import_module(index)
            library_path = idx.LIBRARIES[library]["path"]
        lib = import_module(library_path)
        return get_notebook(lib.NOTEBOOKS[notebook_path]["path"])

    # pull the notebook into temp
    if not os.path.exists(_folder):
        os.makedirs(_folder)
    if _number == NUMBER:  # clear temp files before first request
        for f in glob.glob(_folder + os.path.sep + "n*"):
            os.remove(f)

    number = _number = _number + 1
    tempbase = _folder + os.path.sep + "n" + str(number)
    notebook["temp"] = tempbase + ".ipynb"
    if notebook["pull"].lower().startswith("https:"):
        with urlopen(notebook["pull"]) as r:
            with open(notebook["temp"], "wb") as out_file:
                shutil.copyfileobj(r, out_file)
    else:  # it's a file!
        with open(notebook["pull"]) as in_file:
            with open(notebook["temp"], "w") as out_file:
                out_file.write(in_file.read())

    # add or update cache and return notebook
    if "path" in notebook:  
        notebook["cached"] = True # already imported
    else: # new entry
        notebook["cached"] = False # not yet imported 
        notebook["path"] = path
        _notebooks.append(notebook)
    return notebook


def execute(
    notebook=None,
    library=None,  # use current
    index=None,  # use current
    input_code=None,  # inject function or string
    output_html="output.html",
    params={},
    force_reload=False,
):
    nbo = cache_notebook(notebook, library, index, force_reload=force_reload)
    request = {  # pass to the executed notebook
        "notebook": notebook,
        "library": library,
        "index": index,
        "input_code": input_code,  # TODO extract code from function reference
        "output_html": output_html,
        "params": params,
    }
    with open(_folder + os.path.sep + "execute.json", "w") as f:
        json.dump(request, f, indent=4)
    with open(nbo["temp"]) as r:
        src = r.read()
        src = src.replace("'colab'", "'notebook'")
        src = src.replace("%pip install datamachine", "")
        nb = nbformat.reads(src, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        ep.preprocess(nb)
        html_exporter = HTMLExporter()
        html_exporter.exclude_input = True
        html_data, resources = html_exporter.from_notebook_node(nb)
        html_data = execute_stylings(html_data)
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_data)


def execute_params():
    req = None
    path = _folder + os.path.sep + "execute.json"
    if os.path.exists(path):
        with open(path) as f:
            request = f.read()
            req = json.loads(request)
    return req


def execute_stylings(html_data):
    html_data = html_data.replace(
        "</head>",
        """
        <style>
            .container { width: 100% } 
            .prompt { min-width: 0 } 
            div.output_subarea { max-width: 100% }
            body { margin: 0; padding: 0; }
            div#notebook { padding-top: 0; }
        </style>
        </head>
    """,
    )
    html_data = html_data.replace(
        """
<div class="cell border-box-sizing code_cell rendered">

</div>""",
        "",
    )
    return html_data


def import_module(
    notebook=None, library=None, index=None, force_reload=False,
):
    nbo = cache_notebook(notebook, library, index, force_reload=force_reload)

    nbo["code"] = nbo["temp"].replace("ipynb", "py")
    with open(nbo["temp"]) as f:
        nbj = json.load(f)
        with open(nbo["code"], "w") as code_file:
            code_file.write(import_module_code(nbj))
    nbo["module"] = nbo["code"].replace(".py","").replace(os.path.sep, ".")

    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())
    importlib.invalidate_caches()
    module = importlib.import_module(nbo["module"])
    if force_reload:
        importlib.reload(module)

    return module


def import_module_code(nb):
    code = """
##############################################################################
# Module file generated by datamachine. Any changes here will be lost.       #
##############################################################################
"""
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            # transform the input to executable Python
            src = cell["source"]
            if src[0].startswith("#run"):
                code += "\n# " + "# ".join(cell["source"])
            elif src[0].startswith("#test"):
                code += "\n# " + "# ".join(cell["source"])
            else:
                code += "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            code += "\n# " + "# ".join(cell["source"])
        code += "\n\n"
    return code


def info():
    print(_index, _library)

def params(dict):
    return dict


def set_index(index=None):
    global _index
    # put test here
    if index is None:  # reset to default
        _index = INDEX
    else:
        _index = index


def set_library(library=None):
    global _library
    # put test here
    if library is None:
        _library = LIBRARY
    else:
        _library = library


def show_index(index=None):
    global _index
    if index is None:
        index = _index
    print(index)


def show_library(library=None):
    global _library
    if library is None:
        library = _library
    print(library)


def trace(line):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S  ")
    with open("request.txt", "a") as f:
        f.write(ts + line + "\n")

