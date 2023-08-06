from itertools import product, permutations
import random
import vthread


def get_all_operation_combine(cards):
    c1, c2, c3, c4 = cards
    operators = ['+', '-', '*', '/']

    expressions = []

    for p in product(operators, repeat=len(cards) - 1):  # 运算符是注入在数字之间，所以用数字的长度  -1
        op1, op2, op3 = p  # 循环运算符 (3)

        expressions.append('{} {} {} {} {} {} {}'.format(c1, op1, c2, op2, c3, op3, c4))

    return expressions  # 得出不同的数字和运算符组合的列表


def rand_card():
    return random.randint(1, 14)  # 从十四张牌中随意抽取一张


def get_all_operation_combine_with_number_exchange(cards):
    all_result = []
    for p in permutations(cards):  # 将随机抽取的列表的四个数进行全排列，然后循环调用 get_all_operation_combine() 获得数学运算式，未加括号，放入列表中
        all_result += get_all_operation_combine(p)

    return all_result


# 利用递归思想进行括号添加
def add_brace(numbers):
    if len(numbers) < 2:
        return [numbers]
    if len(numbers) == 2:
        return [['(' + str(numbers[0])] + [str(numbers[1]) + ')']]

    results = []

    for i in range(1, len(numbers)):
        prefix = numbers[:i]
        prefix1 = add_brace(prefix)

        tail = numbers[i:]

        tails = add_brace(tail)

        for p, t in product(prefix1, tails):
            # 将列表中的组合列表先拆开，分别在头步和尾部添加括号在用列表组合
            brace_with_around = ['(' + p[0]] + p[1:] + t[:-1] + [t[-1] + ')']

            results.append(brace_with_around)

    return results


# 不固定长读输出数学运算式
def join_op_with_brace_number(operators, with_brace):
    finally_exp = with_brace[0]

    for i, op in enumerate(operators):
        finally_exp += (op + ' ' + with_brace[i + 1])

    return finally_exp


# 添加括号
def join_brace_to_expression(expression):
    numbers = expression.split()[::2]  # 数字拆分
    operators = expression.split()[1::2]  # 运算符拆分

    with_braces = add_brace(numbers)  # 添加括号

    with_operator_and_brace = []

    for brace in with_braces:
        with_operator_and_brace.append(join_op_with_brace_number(operators, brace))

    return with_operator_and_brace


def simple_but_may_not_answer(cards):
    target = 24

    for exp in get_all_operation_combine(cards):
        if eval(exp) == target:
            print(exp)


def a_little_complicate_but_may_not_answer(cards):
    target = 24

    for exp in get_all_operation_combine_with_number_exchange(cards):
        if eval(exp) == target:
            print(exp)


# 不固定长度
def complicate_but_useful_with_brace(cards):
    targe = 24

    for exp in get_all_operation_combine_with_number_exchange(cards):
        for b in join_brace_to_expression(exp):  # 添加括号不固定长度，数学运算式组合
            try:
                if eval(b) == targe:
                    print(b)
            except ZeroDivisionError:
                continue


new_cards = [rand_card() for _ in range(4)]

# print('我抽到的牌是: {}'.format(new_cards))
#
# print('-- 不带交换位置找到的答案')
# simple_but_may_not_answer(new_cards)
#
# print('-- 带了交换位置找到的答案')
# a_little_complicate_but_may_not_answer(new_cards)
if __name__ == '__main__':
    print('-- 带了括号的答案是')
    complicate_but_useful_with_brace([12, 2, 7, 2])
