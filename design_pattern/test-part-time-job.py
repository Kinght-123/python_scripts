from itertools import permutations


def main():
    # 数据字段列表
    test_fields = [
        "fnd17_oxlcxspebq",
        "fnd17_shsoutbs",
        "fnd28_value_05191q",
        "fnd28_value_05301q",
        "fnd28_value_05302q",
        "fnd17_pehigh",
        "fnd17_pelow",
        "fnd17_priceavg150day",
        "fnd17_priceavg200day",
        "fnd17_priceavg50day",
        "fnd17_pxedra",
        "fnd28_newa3_value_18191a",
        "fnd28_value_02300a",
        "mdl175_ebitda",
        "mdl175_pain"
    ]
    WINDOW_SIZE = 500
    combines = list(permutations(test_fields, 2))
    for i in range(len(combines)):
        # 如果输出函数执行的结果可以用eval()函数解析
        print(
            f'ts_regression(ts_zscore({combines[i][0]}, {WINDOW_SIZE}), ts_zscore({combines[i][1]}, {WINDOW_SIZE}), {WINDOW_SIZE})')
    print(len(combines))


if __name__ == "__main__":
    main()
