import os

def generate_file_tree(root_dir, indent='', ignore=None):
    if ignore is None:
        ignore = {'venv', '__pycache__','.git'}  # 默认忽略的目录和文件
    
    # 获取当前目录下的所有文件和子目录
    entries = [entry for entry in os.listdir(root_dir) if entry not in ignore]
    entries.sort()  # 按字母顺序排序
    
    for i, entry in enumerate(entries):
        path = os.path.join(root_dir, entry)
        is_last = (i == len(entries) - 1)  # 判断是否为当前目录的最后一个条目
        branch = '└── ' if is_last else '├── '
        
        # 打印目录或文件的名称
        print(f"{indent}{branch}{entry}")
        
        # 如果是目录，递归遍历其内容
        if os.path.isdir(path):
            sub_indent = '    ' if is_last else '│   '
            generate_file_tree(path, indent + sub_indent, ignore)
# 设置根目录路径
root_directory = '/Users/markyangkp/Desktop/Projects/InvertedIndexAndRAGAI'

# 打印文件树
print('/')
generate_file_tree(root_directory)