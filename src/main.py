import os, shutil

from markdown import extract_title

def main():
    create_from_static("static/", "public/")
    generate_pages_recursive("content", "template.html", "public")


def create_from_static(src, dest):
    print(f"Copying from [{src}] to [{dest}]")

    if os.path.exists(dest):
        print("Removing all contents of destination")
        shutil.rmtree(dest)
    os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(src_path):
            print(f"Copying [{src_path}] to [{dest_path}]")
            shutil.copy(src_path, dest_path)
        else:
            create_from_static(src_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    from markdown import markdown_to_html_node
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown = file.read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    with open(template_path, "r") as file:
        template = file.read()
    out = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(dest_path, "w") as file:
        file.write(out)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, item)
        dest = os.path.join(dest_dir_path, item.replace(".md", ".html"))
        if os.path.isfile(src) and src[-2:] == "md":
            generate_page(src, template_path, dest)
        elif not os.path.isfile(src):
            os.mkdir(dest)
            generate_pages_recursive(src, template_path, dest)
        else:
            raise Exception("invalid file in content")


if __name__ == "__main__":
    main()
