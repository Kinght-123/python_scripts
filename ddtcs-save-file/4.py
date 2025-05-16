def Selection_Sort(ls):
    for i in range(len(ls)):
        min_index = i
        for j in range(i + 1, len(ls)):
            if ls[j] < ls[min_index]:
                min_index = j
        ls[i], ls[min_index] = ls[min_index], ls[i]
    return ls


if __name__ == '__main__':
    ls = [6, 7, 8, 10, 3, 2, 1, 0]
    print(Selection_Sort(ls))
