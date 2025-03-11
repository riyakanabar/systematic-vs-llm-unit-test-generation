from graphviz import Digraph
import inspect

class TreeNode:
    def __init__(self, node_type, value, left_child=None, right_child=None, next_sibling=None):
        self.node_type = node_type  # "while", "for", "condition", "action"
        self.value = value
        self.left_child = left_child
        self.right_child = right_child
        self.next_sibling = next_sibling #to maintain the flow of statements

def tree_to_code(node, indent=0):
    if node is None:
        return []

    indent_str = " " * 4 * indent
    code = []

    if node.node_type == "while":
        code.append(f"{indent_str}while {node.value}:") # node.value is the condition
        body = tree_to_code(node.left_child, indent + 1)  # left child is the body
        code += body

    elif node.node_type == "for":
        code.append(f"{indent_str}for {node.value}:")  # node.value is the condition
        body = tree_to_code(node.left_child, indent + 1)  # left child is the body
        code += body

    # Handle If condition structure
    elif node.node_type == "condition":
        condition = node.value  # node.value is the condition
        code.append(f"{indent_str}if {condition}:")
        code += tree_to_code(node.left_child, indent + 1)  #if
        if node.right_child: #else
            code.append(f"{indent_str}else:")
            code += tree_to_code(node.right_child, indent + 1)

    # Handle basic action (e.g., return, assignment)
    elif node.node_type == "action":
        code.append(f"{indent_str}{node.value}")

    if node.next_sibling:
        code += tree_to_code(node.next_sibling, indent)

    return code

def code_to_tree(code_lines):
    if not code_lines:
        return None

    root = None
    stack = []
    current_indent = 0

    for line in code_lines:
        stripped_line = line.strip()
        current_indent = len(line) - len(stripped_line)

        if stripped_line.startswith("for"):
            node = TreeNode("for", stripped_line.split("for")[1].strip(":").strip())
        elif stripped_line.startswith("if"):
            node = TreeNode("condition", stripped_line.split("if")[1].strip(":").strip())
        elif stripped_line.startswith("while"):
            node = TreeNode("while", stripped_line.split("while")[1].strip(":").strip())
        elif stripped_line.startswith("else"):
            node = TreeNode("condition", None)  # Use "condition" node type for else
        else:
            node = TreeNode("action", stripped_line)

        # Handle indentation and construct the tree structure
        while stack and stack[-1][0] >= current_indent:
            stack.pop()  # Pop nodes from the stack until the correct parent is found

        if stack:
            parent = stack[-1][1]
            if parent.node_type in {"while", "for", "condition"}:
                if parent.left_child is None:
                    parent.left_child = node
                else:
                    sibling = parent.left_child
                    while sibling.next_sibling:
                        sibling = sibling.next_sibling
                    sibling.next_sibling = node
            elif parent.node_type == "condition" and stripped_line.startswith("else"):
                # Attach else to the last condition
                parent.right_child = node
        else:
            if not root:
                root = node

        if stripped_line.startswith("else"):
            # If it's an else statement, it needs to be processed specially
            if stack:
                last_node = stack[-1][1]
                if last_node.node_type == "condition" and last_node.right_child is None:
                    last_node.right_child = node
                else:
                    # Handle unexpected else position
                    if parent:
                        parent.next_sibling = node

        stack.append((current_indent, node))  # Push current node onto stack with its indentation level

    return root

def visualize_tree(node):
    dot = Digraph()

    def add_nodes_edges(node, parent_id=None, edge_type=None):
        if node is None:
            return
        node_id = str(id(node))

        # Set the label for the node based on its type
        if node.node_type == "condition":
            label = f"condition: if {node.value}"
        elif node.node_type == "action" and edge_type == "right_child":
            label = f"action: else {node.value}"
        else:
            label = f"{node.node_type}: {node.value}" if node.value else node.node_type

        dot.node(node_id, label)

        # Connect to parent if there's a parent
        if parent_id is not None:
            edge_label = ""
            if edge_type == "left_child":
                edge_label = "left (body)" if node.node_type != "condition" else "if"
            elif edge_type == "right_child":
                # If right child is condition, it means it's an 'else if'
                if node.node_type == "condition":
                    edge_label = "right (else)"
                else: #right child is 'else'
                    edge_label = "right"
            elif edge_type == "next_sibling":
                edge_label = "next"

            edge_color = "blue" if edge_type == "left_child" else "green" if edge_type == "right_child" else "orange"
            dot.edge(parent_id, node_id, label=edge_label, color=edge_color)

        # Recursively add children
        if node.left_child:
            add_nodes_edges(node.left_child, node_id, edge_type="left_child")
        if node.right_child:
            add_nodes_edges(node.right_child, node_id, edge_type="right_child")

        # Handle next sibling connections
        if node.next_sibling:
            add_nodes_edges(node.next_sibling, node_id, edge_type="next_sibling")

    add_nodes_edges(node)

    return dot


def middle_to_end_alternating_traversal(pc_fx):
    if not pc_fx:
        return []

    mid = len(pc_fx) // 2

    # Initialize the result list with the middle element
    result = [pc_fx[mid]]

    # Alternate between left and right indices, starting with left
    left, right = mid - 1, mid + 1
    while left >= 0 or right < len(pc_fx):
        if left >= 0:  # Check if left index is within bounds
            result.append(pc_fx[left])
            left -= 1
        if right < len(pc_fx):  # Check if right index is within bounds
            result.append(pc_fx[right])
            right += 1

    return result


def middle_divide_conquer_traversal(pc_fx):
    if not pc_fx:
        return []

    mid = len(pc_fx) // 2

    # First, process the middle element, then recursively traverse the left and right subarrays
    middle = [pc_fx[mid]]
    left = middle_divide_conquer_traversal(pc_fx[:mid])
    right = middle_divide_conquer_traversal(pc_fx[mid + 1:])
    return middle + left + right
















