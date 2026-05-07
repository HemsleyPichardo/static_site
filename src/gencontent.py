import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            # return line.split(" ", 1)[1].strip()
            return line[2:].strip()

    raise ValueError("no h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as from_file:
        markdown_contents = from_file.read()

    with open(template_path) as template_file:
        template_contents = template_file.read()

    html_string = markdown_to_html_node(markdown_contents).to_html()
    title = extract_title(markdown_contents)
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_string)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as destination_file:
        destination_file.write(template_contents)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(full_path):
            generate_page(
                full_path, template_path, Path(dest_path).with_suffix(".html")
            )
        else:
            generate_pages_recursive(full_path, template_path, dest_path)
