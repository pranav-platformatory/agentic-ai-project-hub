import os
from pathlib import Path

# Check if this folder is the _docs folder
pwd_name = Path.cwd().name
if pwd_name == "_docs":
    print("We are in the _docs directory; free to proceed!")
else:
    print(f"We are NOT in the _docs directory but rather in the {pwd_name} directory; aborting README creation/modification!")
    exit()

# Helper function definition:
def list_dir_recursive(parent:str) -> list[tuple[str]]:
    '''
    - Lists directories recursively
    - Returns a list of tuples, where:
        - Last element is the file name
        - Every preceding element is a parent directory of the succeeding element

    ---

    PARAMETERS:
    - `parent` (str): Parent directory

    RETURNS:
    - (list[tuple[str]]): List of tuples of strings representing the file (last element) and its parent director(y)(ies) (preceding elements)
    '''
    
    tracked_file_tuples = []
    files = os.listdir(parent)
    for file in files:
        full_file_path = os.path.join(parent, file)
        if os.path.isdir(full_file_path) and file[0] != '_':
            new_tracked_file_tuples = list_dir_recursive(full_file_path)
            for i in range(len(new_tracked_file_tuples)):
                new_tracked_file_tuples[i].insert(0, parent.split('/')[-1])
            tracked_file_tuples.extend(new_tracked_file_tuples)
        elif file.split('.')[-1] in ["md", "jpeg"] and not (parent == '.' and file == "README.md"):
            tracked_file_tuples.append([parent.split('/')[-1], file])
    
    return tracked_file_tuples

# Retrieving file tuples:
all_file_tuples = list_dir_recursive('.')

# Mapping directories to files and hierarchy levels to directories:
dir2file_map = {}
level2dir_map = {}
for file_tuple in all_file_tuples:
    dir = '/'.join(file_tuple[:-1])
    file = file_tuple[-1]
    level = len(file_tuple) - 1
    if dir2file_map.get(dir, None) is None:
        dir2file_map[dir] = []
    if level2dir_map.get(level, None) is None:
        level2dir_map[level] = set()
    dir2file_map[dir].append(file)
    level2dir_map[level].add(dir)

# Looping through hierarchy levels and the directories in each level and the files in each directory to obtain lines for the README:
lines = []
for level in range(1, max(level2dir_map.keys()) + 1):
    try:
        dirs = list(level2dir_map[level])
        dirs.sort() # To ensure alphabetic order
        for dir in dirs:
            lines.extend(['\n\n', '**Directory: `' + dir + '`**:', '\n'])
            files = dir2file_map[dir]
            files.sort() # To ensure alphabetic order
            # Ensuring any README's are at the top:
            if "README.md" in files:
                files.remove("README.md")
                files.insert(0, "README.md")

            # Adding the file name + link:
            lines.extend(["\n- [`" + file + f'`]({os.path.join(dir, file)})' for file in files])
    except KeyError as e:
        pass

# Writing to the README:
with open("README.md", 'w') as fp:
    fp.write('''<h1>DOCS</h1>

> **NOTE**: *Only the Markdown and image files are listed here.*

---''')
    fp.writelines(lines)
    print("README updated!")