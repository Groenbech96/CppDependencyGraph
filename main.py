import os
import re
from graphviz import Digraph

BASE_DIR_PATHS = ["C:/Users/Groenbech/Development/Cpp/SokoAI/src/SokoAI/"]
EXLUDED_FOLDERS = ["absl", "entt"]

file_types = [".h", ".hpp"]

pattern_local_includes = re.compile("#include \"[\w.\\/]*\"")
pattern_system_includes = re.compile("#include <[\w.\\/]*>")

include_map = dict()


def process_local_include(file_with_includes, include_list):

    for include in include_list:
        
        # find the path of the include, as it is in the middle of two " signs
                
        parts = include.split("\"")
        included_file = parts[1]

        
        if included_file.split("/")[0] in EXLUDED_FOLDERS:
            continue

        file_with_includes = file_with_includes.replace("\\", "/")

        if not file_with_includes in include_map:
            include_map[file_with_includes] = [included_file]
        else:
            if not included_file in include_map[file_with_includes]:
                include_map[file_with_includes].append(included_file)

    

def process_system_include(file_with_includes, include_list):    
    return 0

def process_file(base_dir, path_to_a_file):
    
    # Remove basepath from file 
    base_file = path_to_a_file.replace(base_dir, "")
    
    for type in file_types:
        if path_to_a_file.endswith(type):
            with open(path_to_a_file, "rt") as file:
                content = file.read()
                file.close()

                local_includes = pattern_local_includes.findall(content)
                process_local_include(base_file, local_includes)

                system_includes = pattern_system_includes.findall(content)
                process_system_include(base_file, system_includes)


def call_recursive_on(directory, recursive_dir=""):

    recursive_dir = directory if recursive_dir == "" else  recursive_dir

    for entry in os.listdir(recursive_dir):
        # See if entry is subdirectory
        new_thing = os.path.join(recursive_dir, entry)
        if os.path.isdir(new_thing):
            call_recursive_on(directory, new_thing)
        # Else must be file
        elif os.path.isfile(new_thing):
            process_file(directory, new_thing)
            
            
# program run from here

for path in BASE_DIR_PATHS:
    call_recursive_on(os.path.normcase(path))

f = Digraph('unix', filename='unix.gv',
            node_attr={'color': 'lightblue2', 'style': 'filled'})
f.attr(size='6,6')

for key, value in include_map.items():
    f.node(key)

    for v in value:
        f.edge(key, v)

f.view()

