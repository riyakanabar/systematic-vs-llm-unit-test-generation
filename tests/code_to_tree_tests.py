from utils import code_to_tree, tree_to_code

print("Code to Tree test:")
sum_lines = [
    "total = 0",
    "for i in arr:",
    "    total += i",
    "return total"
]
nested_lines = [
    "for i in range(5):",
    "    for j in range(3):",
    "        print(i, j)",
    "    print(i)"
]
condition_lines = [
    "if x > 0:",
    "    print('Positive')",
    "else:",
    "    print('Non-positive')"
]

print("Test1: Nested Lines")
root_nested = code_to_tree(nested_lines)
nested_code = tree_to_code(root_nested)
print("\n".join(nested_code))

print("Test2: Sum")
root_sum = code_to_tree(sum_lines)
sum_code = tree_to_code(root_sum)
print("\n".join(sum_code))

print("Test3: Condition Lines")
root_condition = code_to_tree(condition_lines)
condition_code = tree_to_code(root_condition)
print("\n".join(condition_code))