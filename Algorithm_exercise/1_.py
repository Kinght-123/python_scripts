ls, target = [1, 3, 7], 10


def main(ls, target):
    dic = {}
    for i, num in enumerate(ls):
        if (y := target - num) in dic:
            return [dic[y], i]
        dic[num] = i


if __name__ == "__main__":
    print(main(ls, target))
