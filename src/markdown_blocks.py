from enum import Enum
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    temp_blocks = markdown.split("\n\n")

    for block in temp_blocks:
        block = block.strip()
        if block != "":
            blocks.append(block)

    return blocks


def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    elif block.startswith(("```\n")) and block.endswith(("```")):
        return BlockType.CODE

    elif block.startswith((">")):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    elif block.startswith(("- ")):
        lines = block.split("\n")
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    elif block.startswith(("1. ")):
        lines = block.split("\n")
        for i, line in enumerate(lines, start=1):
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    children = []

    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                paragraph_node = ParentNode("p", text_to_children(block))
                children.append(paragraph_node)
            case BlockType.HEADING:
                hashes, text = block.split(" ", 1)
                level = len(hashes)
                heading_node = ParentNode(f"h{level}", text_to_children(text))
                children.append(heading_node)
            case BlockType.CODE:
                stripped_text = (
                    block.removeprefix("```").removesuffix("```").removeprefix("\n")
                )
                code_text_node = TextNode(stripped_text, TextType.TEXT)
                code_node = ParentNode(
                    "pre",
                    [ParentNode("code", [text_node_to_html_node(code_text_node)])],
                )
                children.append(code_node)
            case BlockType.QUOTE:
                lines = [line.lstrip(">").strip() for line in block.split("\n")]
                text = " ".join(lines)
                quote_node = ParentNode("blockquote", text_to_children(text))
                children.append(quote_node)
            case BlockType.UNORDERED_LIST:
                lines = [line.removeprefix("- ") for line in block.split("\n")]
                li_nodes = [ParentNode("li", text_to_children(line)) for line in lines]
                unordered_list_node = ParentNode("ul", li_nodes)
                children.append(unordered_list_node)
            case BlockType.ORDERED_LIST:
                lines = [line.split(". ", 1)[1] for line in block.split("\n")]
                li_nodes = [ParentNode("li", text_to_children(line)) for line in lines]
                ordered_list_node = ParentNode("ol", li_nodes)
                children.append(ordered_list_node)

    return ParentNode("div", children)
