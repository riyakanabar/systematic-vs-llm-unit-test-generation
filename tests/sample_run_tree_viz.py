from utils import TreeNode, tree_to_code, visualize_tree

root_binary_search = TreeNode("while", "low <= high",
            left_child=TreeNode("action", "mid = low + (high - low) // 2",
                next_sibling=TreeNode("condition", "arr[mid] == x",
                    left_child=TreeNode("action", "return mid"),
                    right_child=TreeNode("condition", "arr[mid] < x",
                        left_child=TreeNode("action", "low = mid + 1"),
                        right_child=TreeNode("action", "high = mid - 1")
                    )
                )
            ),
        next_sibling=TreeNode("action","return -1")
        )
print("Binary Search Algorithm")

#Tree to Code
print("Tree to Code testing:")
binarySearch = tree_to_code(root_binary_search)
print("\n".join(binarySearch))

# Visualize Tree
dot = visualize_tree(root_binary_search)
dot.render('tree_viz_binary_search', format='png', cleanup=False)
