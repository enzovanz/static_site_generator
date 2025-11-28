import os
import shutil

def copy_files(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    recursive_copy(src, dest)

def recursive_copy(src, dest):
    for item in os.listdir(src):   
        file_path_source = os.path.join(src, item)
        file_path_destination = os.path.join(dest, item)
        if os.path.isfile(file_path_source):
            shutil.copy(file_path_source, file_path_destination)
        else:
            os.mkdir(file_path_destination)
            recursive_copy(file_path_source, file_path_destination)

def main():
    copy_files("static/", "public/")


if __name__ == "__main__":
    main()
