import os

def get_relative_path_a2b(abs_path_a, abs_path_b):
    # 计算从 a 到 b 的相对路径
    relative_path = os.path.relpath(abs_path_b, abs_path_a)

    return relative_path
def get_current_pyfileabspath():
    return os.path.dirname(__file__)
def abs_path2relative_path(abspath,relpath):

    head = relpath
    relpaths = [] 
    tail =  True
    while tail != '':
        head,tail = os.path.split(head)
        if tail == "..":
            abspath = os.path.dirname(abspath)
            continue
        relpaths.append(tail)
    relpath = ""
    for _ in reversed(relpaths):
        relpath = os.path.join(relpath,_)
    return os.path.normcase(os.path.join(abspath,relpath))



if __name__ == "__main__":

    # 示例使用
    
    a = 'C:\\home\\shared\\any_chat\\modules\\customer\\config.py'
    b = 'C:\\home\\shared\\any_chat\\web_assets\\manifest.json'

    # 计算从 a 到 b 的通用规则函数
    relative_path = get_relative_path_a2b(a, b)
    print(relative_path)

    # # 给定新的 a 的绝对路径
    # new_a = 'c:/home/user/documents/reports/report1.txt'

    # # # 应用规则计算出新的 b 的绝对路径
    # new_b = abs_path2relative_path(new_a,"..\\..\\projects\\a\\b\\c")
    # print('New b:', new_b)