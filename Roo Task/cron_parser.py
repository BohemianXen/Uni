import sys


def str_to_cron(string, field_range):
    """Converts a string Cron field into a parsed list of elements.

    Args:
        string (str): The Cron string.
        field_range (Range): All possible valid entries the converted output can contain.

    Returns:
        list: cron formatted list of the string input.
      """
    cron = []
    flatten = False  # Flag to to signal recursion added a dimension to the output list
    step_index = string.find('/')
    step_required = False if step_index is -1 else True  # Flag to signal that step filtering is required after parsing

    if ',' in string:
        vals = string.split(',')
        for val in vals:
            cron.append(str_to_cron(val, field_range))  # Recursively call function for each comma separated entry
        flatten = True
    elif '*' in string:
        cron = [x for x in field_range]  # Extract all values, they will be filtered later if necessary
    elif '-' in string:
        if step_required:
            # Only interested in sub-range so take 1st el. and recursively call function
            cron.append(str_to_cron(string.split('/')[0], field_range))
            flatten = True
        else:
            cron = get_sub_ranges(string.split('-'), field_range)
    else:
        return [int(string)] if int(string) in field_range else []

    if flatten:
        cron = [y for x in range(0, len(cron)) for y in cron[x]]  # Concatenates all values in a 2D list

    if step_required and ',' not in string:
        # Filter outputs to only contain values within the steps
        step = int(string[step_index+1:])
        cron = list(filter(lambda x: (x % step) == 0, cron))

    return cron


def get_sub_ranges(start_stops, field_range):
    """Extracts each discrete value within a fully inclusive start/stop band.

       Args:
           start_stops (list): A list containing each start/stop pair
           field_range (Range): All possible valid entries the converted output can contain.

       Returns:
           list: A concatenated list of all values in the sub-range (that conform to the field_range limit).
         """
    sub_ranges = []
    for i in range(0, len(start_stops), 2):  # Loop in steps of 2 to get each pair
        start = int(start_stops[i])
        stop = int(start_stops[i + 1]) + 1  # Account for inclusive stop band

        sub_ranges.append([x for x in range(start, stop) if x in field_range])

    return [y for x in range(0, len(sub_ranges)) for y in sub_ranges[x]]


def list_to_string(cron_list):
    cron_string = ''
    for val in cron_list:
        cron_string += str(val) + ' '

    return cron_string


def str_date_to_int(string, mapping, index_offset):
    for item in mapping:
        if item in string:
            string = string.replace(item, str(mapping.index(item)+index_offset))

    return string


if __name__ == '__main__':
    ranges = {
        'minute': range(0, 60),
        'hour': range(0, 24),
        'day of month': range(1, 32),
        'month': range(1, 13),  # TODO: string months
        'day of week': range(0, 8),
    }
    months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec')
    days = ('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')

    total_args = len(sys.argv)
    if total_args != 7:
        print('Error: Received %d args, expected 7\nExiting...' % total_args)
        exit(-1)

    args = sys.argv[1:]
    count = 0
    for field_name, field_range in ranges.items():
        arg = args[count].lower()
        try:
            if field_name is 'month':
                arg = str_date_to_int(arg, months, 1)
            elif field_name == 'day of week':
                arg = str_date_to_int(arg, days, 0)
            else:
                pass

            line = list_to_string(sorted(str_to_cron(arg, field_range)))
            print('%14s\t%s\n' % (field_name, line))
        except Exception as e:
            print('Error: Failed to process arg no. %d (\'%s\')\nExiting...' % (count+1, arg))
            exit(-1)

        count += 1

    print('%13s\t%s\n' % ('command', args[-1]))
    exit(0)
