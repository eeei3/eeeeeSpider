import os

def create_data_dir(directory):
        if not os.path.exists(directory):
            print("Creating project " + directory)
            os.makedirs(directory)
        
def create_data_files(project_name, base_url):
        parsed = project_name+'/parsed.txt'
        if not os.path.isfile(parsed):
            write_file(parsed, '')

def write_file(path, data):
        f = open(path, 'w')
        f.write(data)
        f.close()

def append_to_file(path, data):
        with open(path, 'a') as file:
            file.write(data + '\n')

def delete_file_contents(path):
        with open(path, 'w'):
            pass

def file_to_set(file_name):
        results = set()
        with open(file_name, 'rt') as f:
            for line in f:
                results.add(line.replace('\n', ''))
        return results

def set_to_file(content, file):
        delete_file_contents(file)
        for link in content:
            append_to_file(file, content)
