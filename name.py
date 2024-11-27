def check_element_in_list(desired_element, ordered_list):
    """Проверяет наличие искомого элемента в отсортированном списке."""
    for item in ordered_list:
        if item == []:
            return f'Элемент {desired_element} не найден в массиве!'
        if item < desired_element:
            continue
        elif item == desired_element:
            return f'Элемент {desired_element} найден в массиве!'
        elif item > desired_element:
            return f'Элемент {desired_element} найден в массиве!'
        break


# Вызываем функцию с тестовыми данными.
# Первый аргумент - целое число.
# Второй аргумент - отсортированный по возрастанию список целых чисел.
result = check_element_in_list(5, [1, 2, 4, 5, 6])
# Распечатываем результат.
print(result)