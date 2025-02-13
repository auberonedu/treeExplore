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
    Build and return a sample unbalanced binary tree with:
    - One duplicate value (5 appears twice)
    - One negative value (-3)

              10
           /      \
          9        15
         / \       / \
        5   2    -3   5
                       \
                       22
    """
    root = Node(10)
    root.left = Node(9)
    root.right = Node(15)

    root.left.left = Node(5)
    root.left.right = Node(2)

    root.right.left = Node(-3)
    root.right.right = Node(5)
    root.right.right.right = Node(22)

    return root


def get_css_path(depth):
    """
    Return a relative path to the 'styles.css' file based on the node's depth.
    - The root is at depth 0 (where 'index.html' and 'styles.css' live side by side).
    - A child is depth 1, so it references "../styles.css".
    - A grandchild is depth 2, so it references "../../styles.css", etc.
    """
    return "../" * depth + "styles.css"

def generate_node_page(node, parent_path, output_dir, depth):
    """
    Generate the HTML for a single node's 'index.html' file.
    
    :param node: Current Node
    :param parent_path: The relative link to the parent's index.html (e.g., "../index.html")
    :param output_dir: Folder path to place this node's 'index.html'
    :param depth: How many levels deep this node is from the root
    """
    css_rel_path = get_css_path(depth)

    # Determine child links (either to actual child or null page)
    left_link_html = f'<a class="circle-link" href="left/index.html">Left</a>'
    right_link_html = f'<a class="circle-link" href="right/index.html">Right</a>'

    parent_link_html = (f'<a class="circle-link" href="{parent_path}">Return to Parent</a>'
                        if parent_path else '')

    # Build the HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Node {node.value}</title>
    <link rel="stylesheet" href="{css_rel_path}">
</head>
<body>
    <h1 class="node-value">{node.value}</h1>
    <nav>
        {left_link_html}
        {parent_link_html}
        {right_link_html}
    </nav>
</body>
</html>
"""

    # Write out the HTML to index.html
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)


def generate_null_page(output_dir, parent_path):
    """
    Generate an 'index.html' page for a null node.
    
    :param output_dir: The folder where this node's page is stored
    :param parent_path: Relative path to this node's parent index.html
    """
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Null</title>
    <link rel="stylesheet" href="{get_css_path(output_dir.count(os.sep))}">
</head>
<body>
    <h1 class="node-value">null</h1>
    <nav>
        <a class="circle-link" href="{parent_path}">Return to Parent</a>
    </nav>
</body>
</html>
"""

    # Write out the HTML to index.html
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_tree_pages(node, output_dir, parent_path=None, depth=0):
    """
    Recursively create directories for the node, generate its index.html,
    and do the same for the left and right children. Generates 'null' pages
    where children are missing.
    
    :param node: The current Node (or None for null nodes)
    :param output_dir: The folder where this node's page is stored
    :param parent_path: Relative path to this node's parent's index.html
    :param depth: Depth of this node from the root (root=0, child=1, grandchild=2, etc.)
    """
    if node is None:
        # If the node is null, just make a placeholder page with a "Return to Parent" link
        os.makedirs(output_dir, exist_ok=True)
        generate_null_page(output_dir, parent_path)
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate this node's HTML page
    generate_node_page(node, parent_path, output_dir, depth)

    # Generate left subtree (or null page)
    left_child_path = os.path.join(output_dir, "left")
    left_parent_link = "../index.html"
    if node.left:
        generate_tree_pages(node.left, left_child_path, left_parent_link, depth+1)
    else:
        generate_tree_pages(None, left_child_path, left_parent_link, depth+1)

    # Generate right subtree (or null page)
    right_child_path = os.path.join(output_dir, "right")
    right_parent_link = "../index.html"
    if node.right:
        generate_tree_pages(node.right, right_child_path, right_parent_link, depth+1)
    else:
        generate_tree_pages(None, right_child_path, right_parent_link, depth+1)


def create_css_file(output_folder):
    """
    Creates a single 'styles.css' file at the root output folder.
    """
    css_content = """
/* Simple styling with a cream background and some circle links */
body {
  font-family: Arial, sans-serif;
  margin: 1em;
  padding: 0;
  text-align: center;
  background-color: #fdf8ee; /* a light cream color */
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
"""
    with open(os.path.join(output_folder, "styles.css"), "w", encoding="utf-8") as f:
        f.write(css_content)

def main():
    """
    Main entry point:
    - Build the tree
    - Wipe/create an output folder
    - Generate all pages
    - Write a single CSS file in the root
    """
    # Build the sample tree
    root = build_example_tree()

    # Define the output folder
    output_folder = "tree_site"

    # Remove old site folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Create the main output folder again
    os.makedirs(output_folder, exist_ok=True)

    # Create the CSS file in the root
    create_css_file(output_folder)

    # Generate the pages for the entire tree
    # The root node has no parent, so parent_path=None, depth=0
    generate_tree_pages(root, output_folder, parent_path=None, depth=0)

    print(f"Website generated in folder: {output_folder}")
    print("Open 'index.html' inside that folder in your browser to explore the tree!")

if __name__ == "__main__":
    main()
