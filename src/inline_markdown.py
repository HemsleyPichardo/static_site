import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            split_pieces = node.text.split(delimiter)
            if len(split_pieces) % 2 == 0:
                raise ValueError(
                    "Invalid Markdown syntax. Formatted section not closed"
                )
            else:
                for index, value in enumerate(split_pieces):
                    if value == "":
                        continue
                    if index % 2 == 0:
                        result.append(TextNode(value, TextType.TEXT))
                    else:
                        result.append(TextNode(value, text_type))
    return result


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        images = extract_markdown_images(node.text)
        # handle the "no imaes found" case
        if not images:
            result.append(node)
            continue
        # Remaining is the part of the text not processed yet
        remaining = node.text

        for alt, url in images:
            sections = remaining.split(f"![{alt}]({url})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(alt, TextType.IMAGE, url))
            remaining = sections[1]

        if remaining != "":
            result.append(TextNode(remaining, TextType.TEXT))

    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        links = extract_markdown_links(node.text)
        # handle the "no imaes found" case
        if not links:
            result.append(node)
            continue
        # Remaining is the part of the text not processed yet
        remaining = node.text

        for text, url in links:
            sections = remaining.split(f"[{text}]({url})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.TEXT))
            result.append(TextNode(text, TextType.LINK, url))
            remaining = sections[1]

        if remaining != "":
            result.append(TextNode(remaining, TextType.TEXT))

    return result


def text_to_textnodes(text):
    # result = []
    node = TextNode(text, TextType.TEXT)

    bolded_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bolded_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    result = split_nodes_link(image_nodes)
    return result
