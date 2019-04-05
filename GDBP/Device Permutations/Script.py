import Components
import csv
from datetime import datetime
from itertools import product


# Expected input file indexes
index = {
    'name': 0,
    'ID': 1,
    'cost': 2,
    'volume': 3,
    'quantity': 4
}


# Filenames
components_filename = 'components.csv'
permutations_filename = 'permutations'


# Constraints
constraints = {
    'cost': 125.00,  # GBP
    'volume': 80000  # mm^3
}


# Possible Permutations
id_headers = []
viable = []
non_viable = []


# Read components
def read_components(filename):
    with open(filename, 'r') as f_in:
        components = {}

        for line in f_in:
            if line is not '\n' and line.find('Component Name') == -1:  # Skip component name column
                fields = line.split(',')
                full_id = fields[index['ID']]
                header = full_id[:full_id.find('_')]  # Extract component type (header)

                # If header has not already been encountered, log it and make an empty list for its component variations
                if header not in id_headers:
                    id_headers.append(header)
                    components[header] = []

                # Log full component details to dictionary
                components[header].append(Components.Component(fields[index['ID']],
                                                               fields[index['cost']],
                                                               fields[index['volume']],
                                                               fields[index['quantity']]))

    okay = create_permutations(components)
    return okay


# Create permutations
def create_permutations(components):
    component_groupings = []

    # Split all components into their respective groupings by ID
    for header, component in components.items():
        component_groupings.append(component)

    # Cartesian product to determine all possible permutations
    component_groupings = tuple(component_groupings)
    all_permutations = list(product(*component_groupings))

    digits = len(str(len(all_permutations)))  # Max number of digits needed to uniquely identify all permutations
    ID = 0

    for permutation in list(all_permutations):
        ids = [comp.ID for comp in permutation]  # Extract ids of each component in the permutation
        [total_cost, total_volume] = sum_components(permutation)  # Add all costs and volumes of components in set

        # Log details of current permutation (constituents, total cost, and total volume)
        current_permutation = Components.Permutations('PER_' + format(ID, '0' + str(digits) + 'd'),
                                                      ids,
                                                      total_cost,
                                                      total_volume)

        # Check constraints to determine permutation viability
        if current_permutation.cost <= constraints['cost']: # and (current_permutation.volume <= constraints['volume']):
            viable.append(current_permutation)
        else:
            non_viable.append(current_permutation)

        ID += 1

    # Write permutations to file (viable first)
    record_permutations(permutations_viable=True, final=False)
    return True


def sum_components(components):
    cost = 0
    volume = 0
    for component in components:
        cost += float(component.cost) * float(component.quantity)
        volume += float(component.volume) * float(component.quantity)

    return [cost, volume]


# Write permutations to file
def record_permutations(permutations_viable, final):
    [viability, permutations] = ['viable', viable] if permutations_viable else ['non-viable', non_viable]

    # Write permutations
    with open(viability + ' ' + permutations_filename + ' ' + datetime.now().strftime("%Y-%m-%d %H_%M_%S") + '.csv',
              'w',  newline='') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        columns_headers= ['ID', 'Total Cost (£)', 'Total Volume (mm3)']
        for header in id_headers:
            columns_headers.append(header)

        f_writer.writerow(columns_headers)

        if len(permutations) != 0:
            for permutation in permutations:
                row = [permutation.ID, str(permutation.cost), str(permutation.volume)]
                for component in permutation.components:
                    row.append(component)

                f_writer.writerow(row)

    # Write non-viable permutations
    if not final:
        record_permutations(permutations_viable=False, final=True)


if __name__ == '__main__':
    print('Script Running...')
    success = read_components(components_filename)
    print('Script Completed: ' + str(success))
