import os, shutil

from markdown import extract_title

def main():
    create_from_static("static/", "public/")
    generate_page("content/index.md", "template.html", "public/index.html")


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

    #TODO:create missing directories if not present
    with open(dest_path, "w") as file:
        file.write(out)



if __name__ == "__main__":
    main()
