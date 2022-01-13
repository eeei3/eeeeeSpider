"""
# /***************************************************************************************
#  Module that is responsible for universal file i/o
# ***************************************************************************************\
"""


def write_file(path, data):
    # Writes data to file
    with open(path, 'w', encoding='utf8') as file:
        file.write(data)
        file.close()

def append_to_file(path, data):
    # Appends data to file
    with open(path, 'a', encoding='utf8') as file:
        file.write(data + '\n')

def delete_file_contents(path):
    # Empty a file of data
    with open(path, 'w', encoding='utf8'):
        pass

def file_to_set(file_name):
    # Read contents of file and return the data
    results = set()
    with open(file_name, 'rt', encoding='utf8') as file:
        for line in file:
            results.add(line.replace('\n', ''))
    return results

def set_to_file(links, file):
    # Read data and dump it into file
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)
