def add(x, y):
    """计算两个数的和。

    支持整数和浮点数相加，返回两数之和。

    调用示例:
        >>> add(1, 2)
        3
        >>> add(3.5, 2.5)
        6.0

    返回示例:
        int | float: x 与 y 的和，类型与输入参数一致。
    """
    return x + y


def subtract(x, y):
    """计算两个数的差。

    返回 x 减去 y 的结果，支持整数和浮点数。

    调用示例:
        >>> subtract(5, 3)
        2
        >>> subtract(10.0, 3.5)
        6.5

    返回示例:
        int | float: x - y 的差值，类型与输入参数一致。
    """
    return x - y