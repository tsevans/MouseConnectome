import csv


def read_adjacency_matrix():
    with open('data/Mouse_Matrix_Binned.csv', 'rb') as adj_file:
        reader = csv.reader(adj_file)
        for row in reader:
            print(str(row) + '\n')


if __name__ == '__main__':
    read_adjacency_matrix()
