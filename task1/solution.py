def strict(func):
    def wrapper(*args, **kwargs):
        # Определяем метаданные для функции-обертки вручную, не пользуясь itertools (по ТЗ)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        wrapper.__annotations__ = func.__annotations__
        func_annotations = func.__annotations__

        annotations = func.__annotations__   # Получаем аннотации типов

        for arg, (param_name, expected_type) in zip(args, annotations.items()):
            '''Проходим по всем переданным аргументам и проверяем их тип'''
            if not isinstance(arg, expected_type):
                raise TypeError(
                    f"Argument '{param_name}' must have type {expected_type.__name__}, "
                    f"but got {type(arg).__name__}."
                )

            if param_name == 'return':   # Пропускаем проверку для результата
                continue

        result = func(*args, **kwargs)   # Выполняем функцию

        if 'return' in annotations:
            expected_return_type = annotations['return']

            if not isinstance(result, expected_return_type):   # Проверяем тип возвращаемого значения
                raise TypeError(
                    f"Return value must have {expected_return_type.__name__}, "
                    f"but got {type(result).__name__}."
                )

        return result   # Если исключений не возникло -> возвращаем результат выполнения функции
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


# Тесты
print(sum_two(1, 2))      # >>> 3
print(sum_two(1, 2.4))    # >>> TypeError: Argument 'b' must be of type int, but got float.

@strict
def multiply(a: int, b: int) -> int:
    return a * b

try:
    print(multiply(3, 2.5))  # >>> TypeError: Return value must have int, but got float.
except TypeError as e:
    print(e)

@strict
def concat_strings(a: str, b: str) -> str:
    return a + b

try:
    print(concat_strings("hello", 5))  # >>> TypeError: Argument 'b' must be of type str, but got int.
except TypeError as e:
    print(e)

try:
    print(concat_strings("hello", "world"))  # >>> "helloworld"
except TypeError as e:
    print(e)