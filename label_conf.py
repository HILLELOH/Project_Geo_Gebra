import config


def generate_alphanumeric_sequence():
    current_char = 'A'
    num_iteration = 0
    while True:
        if len(config.deleted_labels) > 0:
            current_char = config.deleted_labels.pop()
        else:
            if num_iteration != 0:
                yield current_char + str(num_iteration)
            else:
                pass
            if current_char == 'Z':
                current_char = 'A'
                num_iteration += 1

            else:
                current_char = chr(ord(current_char) + 1)
