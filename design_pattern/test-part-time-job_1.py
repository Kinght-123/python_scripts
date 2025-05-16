from itertools import permutations


def main():
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
    permutation_pairs = permutations(test_fields, 2)

    # 批量生成输入公式
    lines = [
        f'ts_regression(ts_zscore({d1},{WINDOW_SIZE}), ts_zscore({d2},{WINDOW_SIZE}), {WINDOW_SIZE})'
        for d1, d2 in permutation_pairs
    ]

    print('\n'.join(lines))
    print(len(lines))


if __name__ == "__main__":
    main()
