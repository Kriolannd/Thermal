import random


def append_to_file(file_path, time_value, select_all=False):
    values = {
        'change_state_true': 1,
        'change_state_done': 1,
        'state_true': random.randint(0, 1),
        'temp_true': random.randint(500, 2000),
        'temp_seeming': random.randint(500, 2000)
    }

    with open(file_path, 'a') as file:
        variables = ['change_state_true', 'change_state_done', 'state_true', 'temp_true', 'temp_seeming']
        line = 'time=' + str(time_value) + ' '

        if select_all:
            selected_variables = variables
        else:
            selected_variables = random.sample(variables, random.randint(1, len(variables)))

        for variable in selected_variables:
            line += variable + '=' + str(values[variable]) + ' '

        file.write(line + '\n')

# append_to_file('F1_generated.txt')
