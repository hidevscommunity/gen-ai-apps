import pycode_similar
from pprint import pprint

def similarity_check(ref_code: str, actual_code: str):
    print(ref_code)
    print(actual_code)

    _, info = pycode_similar.detect([ref_code, actual_code],
                                 diff_method=pycode_similar.UnifiedDiff,
                                 keep_prints=False,
                                 module_level=False)[0]
    return info[0].plagiarism_percent

# if __name__ == "__main__":
#     sample_code = """class Solution:
#     def maxDepth(self, root: TreeNode) -> int:

#         if not root:
#             return 0

#         l = self.maxDepth(root.left)
#         r = self.maxDepth(root.right)

#         if l > r:
#             return l + 1
#         return r + 1
# """
#     sol_1_code = """class Solution:
#     def maxDepth(self, root: TreeNode) -> int:
#         if not root:
#             return 0
        
#         depth = 0
#         q = []
#         q.append(root)
        
#         while q:
#             depth += 1
#             temp = []
            
#             for node in q:
#                 if node.left:
#                     temp.append(node.left)
#                 if node.right:
#                     temp.append(node.right)
            
#             q = temp
        
#         return depth
# """
#     pprint(similarity_check(sample_code, sol_1_code))