def process_dataset_two():
    fle = open('mouse.csv')
    new = open('mouse.txt', 'w')

    for ln in fle.readlines():
        p = ln.split(',')
        wline = p[0] + ' ' + p[1].rstrip() + ' 1\n'
        new.write(wline)

    fle.close()
    new.close()


def process_dataset_three():
    fle = open('processed.csv')
    new = open('mouse_info.txt', 'w')
    for line in fle.readlines():
        sp = line.split(',', 1)
        wline = sp[0] + "\t" + sp[1]
        new.write(wline)

    fle.close()
    new.close()


if __name__ == "__main__":
    process_dataset_three()