from tabulate import tabulate
import string

def input_table():
    input_array = []
    input_n = int(input("Введите коэффициент n: "))
    print()

    for i in range(2 ** input_n):
        input_array.append(list(map(int, input(f"Введите {i+1}-ю строку: ")))[:input_n+1])

    return input_n, input_array


def row_xor(row):
    temp_array = []
    for j in range(len(list(row)) - 1):
        temp_array.append(row[j] ^ row[j + 1])

    return temp_array


def make_triangle(t, n):
    if not t:
        return []

    triangle_array = list()
    triangle_array.append(list(a[n] for a in t))

    while len(list(triangle_array)) != 2 ** n:
        triangle_array.append(row_xor(list(triangle_array[-1])))

    return triangle_array


def make_polynomial(tr, n):
    variables = string.ascii_uppercase[:n]

    coeffs = [i[0] for i in list(tr)]
    terms = []

    for i in range(2 ** n):
        if coeffs[i] == 1:
            term = []
            for j in range(n):
                if (i & (1 << (n - 1 -j))) != 0:
                    term.append(f'{variables[j]}')
            terms.append(''.join(term) if term else '1')
    return coeffs, ' + '.join(terms)


def draw_triangle(tr):
    top_side = tr[0]
    left_side = [row[0] for row in tr]

    tr[0] = left_side
    for i in range(len(tr)):
        tr[i][0] = top_side[i]

    for i, row in enumerate(tr):
        indent = "  " * i
        print(f"{indent}{row}")


def main():
    vars_count, table = input_table()

    triangle = make_triangle(table, vars_count)

    coefficients, polynomial = make_polynomial(triangle, vars_count)

    print(f"Введенная таблица истинности:")

    headers = list(string.ascii_uppercase[:vars_count] + "F")
    print(tabulate(table, headers=headers, tablefmt="grid"))

    print(f"Треугольник:")
    draw_triangle(triangle)

    print(f"Коэффициенты: {list(coefficients)}")
    print(f"Полином Жегалкина: {polynomial}")


if __name__ == '__main__':
    main()

