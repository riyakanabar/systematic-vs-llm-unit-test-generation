import unittest
from utils import TreeNode, tree_to_code, visualize_tree

class TestTreeToCode(unittest.TestCase):
    def setUp(self):
        self.root_binary_search = TreeNode("while", "low <= high",
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

        self.root_insertion_sort = TreeNode("for", "i in range(1, len(arr))",
            left_child=TreeNode("action", "key = arr[i]",
                next_sibling=TreeNode("action", "j = i - 1",
                    next_sibling=TreeNode("while", "j >= 0 and key < arr[j]",
                        left_child=TreeNode("action", "arr[j + 1] = arr[j]",
                            next_sibling=TreeNode("action", "j -= 1")
                        ),
                        next_sibling=TreeNode("action", "arr[j + 1] = key")
                    )
                )
            )
        )

        self.root_sum = TreeNode("action", "total = 0",
            next_sibling=TreeNode("for", "i in arr",
                left_child=TreeNode("action", "total += i"),
                next_sibling=TreeNode("action", "return total")
            )
        )

    def test_binary_search_tree_to_code(self):
        expected_code = [
            "while low <= high:",
            "    mid = low + (high - low) // 2",
            "    if arr[mid] == x:",
            "        return mid",
            "    else:",
            "        if arr[mid] < x:",
            "            low = mid + 1",
            "        else:",
            "            high = mid - 1",
            "return -1"
        ]
        self.assertEqual(tree_to_code(self.root_binary_search), expected_code)

    def test_insertion_sort_tree_to_code(self):
        expected_code = [
            "for i in range(1, len(arr)):",
            "    key = arr[i]",
            "    j = i - 1",
            "    while j >= 0 and key < arr[j]:",
            "        arr[j + 1] = arr[j]",
            "        j -= 1",
            "    arr[j + 1] = key"
        ]
        self.assertEqual(tree_to_code(self.root_insertion_sort), expected_code)

    def test_sum_tree_to_code(self):
        expected_code = [
            "total = 0",
            "for i in arr:",
            "    total += i",
            "return total"
        ]
        self.assertEqual(tree_to_code(self.root_sum), expected_code)

if __name__ == "__main__":
    unittest.main()

