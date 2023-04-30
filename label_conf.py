import re
import config


def get_label_parts(label):
    # print(label)
    match = re.search(r'\d', label)
    if match:
        index = match.start()
        chars = label[:index]
        numbers = label[index:]
        return chars, numbers
    else:
        return label, False


# def generate_alphanumeric_sequence():
#     current_char = 'A'
#     num_iteration = 0
#     config.last_label_before_return = 'A'
#     while True:
#         if len(config.deleted_labels) > 0:
#             current_char = config.deleted_labels.pop()
#
#         chars, numbers = get_label_parts(current_char)
#         if chars < config.last_label_before_return:
#             current_char = f'{config.last_label_before_return}'
#             current_char = chr(ord(current_char) + 1)
#             num_iteration = config.last_turn_before_return
#         else:
#
#
#             # if num_iteration != 0:
#             #     yield current_char + str(num_iteration)
#             # else:
#             #     pass
#             yield current_char + str(num_iteration)
#             if current_char == 'C':
#                 current_char = 'A'
#                 num_iteration += 1
#
#             else:
#                 current_char = chr(ord(current_char) + 1)
# def generate_alphanumeric_sequence():
#     current_char = 'A'
#     num_iteration = 0
#     config.last_label_before_return = 'A'
#     config.last_turn_before_return = 0
#     while True:
#         if len(config.deleted_labels) > 0:
#             # Use any previously deleted labels before generating new ones
#             tmp = config.deleted_labels.pop(0)
#             chars, numbers = get_label_parts(tmp)
#             if chars == config.last_label_before_return:
#                 num_iteration = int(numbers)
#             else:
#                 current_char = chars
#                 num_iteration = int(numbers)
#         else:
#             if current_char < config.last_label_before_return:
#                 current_char = chr(ord(config.last_label_before_return) + 1)
#                 num_iteration = config.last_turn_before_return
#             label = current_char + str(num_iteration)
#             while label in config.deleted_labels:
#                 num_iteration += 1
#                 label = current_char + str(num_iteration)
#             yield label
#             if current_char == 'Z':
#                 current_char = 'A'
#                 num_iteration += 1
#             else:
#                 current_char = chr(ord(current_char) + 1)
# def generate_alphanumeric_sequence():
#     current_char = 'A'
#     num_iteration = 0
#     config.last_label_before_return = 'A'
#     config.last_turn_before_return = 0
#     while True:
#         if len(config.deleted_labels) > 0:
#             # Use any previously deleted labels before generating new ones
#             tmp = config.deleted_labels.pop(0)
#             chars, numbers = get_label_parts(tmp)
#             if not chars == config.last_label_before_return:
#                 num_iteration = int(numbers)
#                 current_char = chars + str(num_iteration)
#                 print(current_char)
#
#         elif len(config.deleted_labels) == 0:
#             if current_char < config.last_label_before_return:
#                 current_char = chr(ord(config.last_label_before_return) + 1)
#                 num_iteration = config.last_turn_before_return
#             label = current_char + str(num_iteration)
#             while label in config.deleted_labels:
#                 config.deleted_labels.remove(label)
#                 num_iteration += 1
#                 label = current_char + str(num_iteration)
#             yield label
#             if current_char == 'Z':
#                 current_char = 'A'
#                 num_iteration += 1
#             else:
#                 current_char = chr(ord(current_char) + 1)
def generate_alphanumeric_sequence():
    current_char = 'A'
    num_iteration = 0
    config.last_label_before_return = 'A'
    config.last_turn_before_return = 0
    while True:
        if len(config.deleted_labels) > 0:
            # Use any previously deleted labels before generating new ones
            tmp = config.deleted_labels.pop(0)
            chars, numbers = get_label_parts(tmp)
            if not chars == config.last_label_before_return:
                current_char = chars
                num_iteration = int(numbers)
            label = current_char + str(num_iteration)
            while label in config.deleted_labels:
                config.deleted_labels.remove(label)
                num_iteration += 1
                label = current_char + str(num_iteration)
            yield label
        else:
            if current_char < config.last_label_before_return:
                current_char = chr(ord(config.last_label_before_return) + 1)
                num_iteration = config.last_turn_before_return
            label = current_char + str(num_iteration)
            while label in config.deleted_labels:
                config.deleted_labels.remove(label)
                num_iteration += 1
                label = current_char + str(num_iteration)
            yield label
            if current_char == 'Z':
                current_char = 'A'
                num_iteration += 1
            else:
                current_char = chr(ord(current_char) + 1)
