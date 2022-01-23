# pylint: disable=C0116
"""
/***************************************************************************************
Module that is responsible for universal file i/o
***************************************************************************************\
"""


# Writes data to file
def write_file(path, data):

    # Opening the file in write mode and writing
    # the data
    with open(path, 'w', encoding='utf8') as file:
        file.write(data)
        file.close()


# Appends data to file
def append_to_file(path, data):

    # Opening the file in append mode and appending
    # the data
    with open(path, 'a', encoding='utf8') as file:
        file.write(data + '\n')


# Empty a file of data
def delete_file_contents(path):

    # Opening the file in write mode and closing it
    with open(path, 'w', encoding='utf8'):
        pass


# Read contents of file and return the data
def file_to_set(file_name):

    # Set for links retrieved from file
    results = set()

    # Opening the file in read text mode
    # and compiling each line into the set
    with open(file_name, 'rt', encoding='utf8') as file:
        for line in file:

            results.add(line.replace('\n', ''))

    return results


# Read data and dump it into file
def set_to_file(links, file):

    delete_file_contents(file)

    # Appending each link to the end of the file
    for link in sorted(links):

        append_to_file(file, link)
