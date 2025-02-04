import os
import shutil

class Node:
    """
    A simple binary tree node.
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def build_example_tree():
    """
    Build and return a sample binary tree.
    
            10
           /  \
          5    15
         / \     \
        2   7     20
    """
    root = Node(10)
    root.left = Node(5)
    root.right = Node(15)
    root.left.left = Node(2)
    root.left.right = Node(7)
    root.right.right = Node(20)
    
    return root

def generate_node_page(node, parent_path, output_dir):
    """
    Generate the HTML for a single node's 'index.html' file.
    """
    # We'll store an inline CSS block here for simplicity.
    # You could also write this out to a separate CSS file if you prefer.
    css_block = """
    <style>
    body {
      font-family: Arial, sans-serif;
      margin: 1em;
      padding: 0;
      text-align: center;
    }
    .node-value {
      font-size: 3em;
      margin: 0.5em 0;
    }
    nav {
      margin-top: 1em;
      display: flex;
      justify-content: center;
      gap: 1em;
      flex-wrap: wrap;
    }
    .circle-link {
      display: inline-block;
      text-decoration: none;
      color: #333;
      border: 2px solid #333;
      border-radius: 999px; /* big number for a circle */
      padding: 0.5em 1em;
      min-width: 3em;
      text-align: center;
      transition: background-color 0.2s, color 0.2s;
    }
    .circle-link:hover {
      background-color: #333;
      color: #fff;
    }
    </style>
    """

    # Links: We'll create an anchor only if there's a valid target.
    # Parent link:
    if parent_path:
        parent_link = f'<a class="circle-link" href="{parent_path}">Back to parent</a>'
    else:
        parent_link = ''

    # Left link:
    if node.left:
        left_link = '<a class="circle-link" href="left/index.html">Left</a>'
    else:
        left_link = ''

    # Right link:
    if node.right:
        right_link = '<a class="circle-link" href="right/index.html">Right</a>'
    else:
        right_link = ''

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Node {node.value}</title>
    {css_block}
</head>
<body>
    <h1 class="node-value">{node.value}</h1>
    <nav>
        {parent_link}
        {left_link}
        {right_link}
    </nav>
</body>
</html>
"""
    # Write out the HTML to index.html in the output_dir
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_tree_pages(node, output_dir, parent_path=None):
    """
    Recursively create directories for the node, generate its index.html,
    and do the same for the left and right children.
    
    :param node: The current Node
    :param output_dir: The folder where this node's page is stored
    :param parent_path: Relative path to this node's parent index.html (for the "back to parent" link)
    """
    if not node:
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate this node's HTML page
    generate_node_page(node, parent_path, output_dir)

    # Generate left subtree if present
    if node.left:
        # The parent link from the child's perspective is "../index.html"
        child_parent_link = "../index.html"
        generate_tree_pages(node.left, os.path.join(output_dir, "left"), child_parent_link)

    # Generate right subtree if present
    if node.right:
        # The parent link from the child's perspective is "../index.html"
        child_parent_link = "../index.html"
        generate_tree_pages(node.right, os.path.join(output_dir, "right"), child_parent_link)

def main():
    """
    Main entry point. Builds a sample tree, wipes/creates an output folder, and
    generates all pages for the entire tree.
    """
    # Build or define the tree here:
    root = build_example_tree()

    # Define where to place the output.
    # This will create a folder "tree_site" with subfolders for each node.
    output_folder = "tree_site"

    # Remove old site folder if it exists, so we start fresh.
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Generate the site
    # The root node has no parent, so parent_path=None
    generate_tree_pages(root, output_folder, parent_path=None)
    print(f"Website generated in folder: {output_folder}")
    print("Open 'index.html' inside that folder in your browser to explore the tree!")

if __name__ == "__main__":
    main()
