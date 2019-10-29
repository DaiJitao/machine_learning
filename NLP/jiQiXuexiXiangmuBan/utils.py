
def load_data(in_file):
    cn = []
    en = []
    with open(in_file, mode='r', encoding='utf-8') as file:
        for line in file.readlines():
            line = line.strip().split("\t")
            en.append(line[0])
            cn.append(line[1])

    return cn, en