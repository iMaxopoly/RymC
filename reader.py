import io

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


def read(filename):
    with io.open(filename, "r", encoding="utf8") as f:
        string_list = []
        for line in f:
            if line != "" and line not in string_list:
                string_list.append(line.strip("\t\r\n '\""))
        return string_list
