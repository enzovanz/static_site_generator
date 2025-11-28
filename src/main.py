from functions import copy_files, generate_pages_recursive

def main():
    copy_files("static/", "public/")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
