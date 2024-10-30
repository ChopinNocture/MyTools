def update_value_in_file(filename, keyword, new_value):
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            parts = line.split('=')
            if len(parts) == 2:
                left = parts[0].strip()
                right = parts[1].strip()

                # 检查左侧是否为关键字，并且右侧为数字
                if left == keyword and (right.replace('.', '', 1).isdigit() or right.isdigit()):
                    # 修改右侧的值
                    line = f"{left} = {new_value}\n"
            file.write(line)

# 示例用法
update_value_in_file('data.txt', 'my_keyword', 42.0)
def update_value_in_file(filename, keyword, new_value):
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            parts = line.split('=')
            if len(parts) == 2:
                left = parts[0].strip()
                right = parts[1].strip()

                # 检查左侧是否为关键字，并且右侧为数字
                if left == keyword and (right.replace('.', '', 1).isdigit() or right.isdigit()):
                    # 修改右侧的值
                    line = f"{left} = {new_value}\n"
            file.write(line)

# 示例用法
update_value_in_file('data.txt', 'my_keyword', 42.0)
