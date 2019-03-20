import Components
import csv
from datetime import datetime

# TODO: - Try/catch read/writes
#       - Multiple sensor logic (for now different string IDs is the only way)

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


# Fixed Unit Costs (5000 batch)
enclosure_cost = 7.32
pcb_cost = 5
software_cost = 0.23
misc = 0.0
total_fixed_costs = enclosure_cost + pcb_cost + software_cost + misc


# Constraints
constraints = {
    'cost': 85.02,  # GBP
    'volume': 80000  # mm^3
}


# Possible Permutations
viable = []
non_viable = []


# Read components
def read_components(filename):
    with open(filename, 'r') as f_in:

        sensors = []
        wireless_modules = []
        batteries = []

        for line in f_in:
            if line is not '\n':
                fields = line.split(',')
                if 'S' in fields[index['name']]:
                    sensors.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'W' in fields[index['name']]:
                    wireless_modules.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'B' in fields[index['name']]:
                    batteries.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'Name' in fields[index['name']]:
                    continue
                else:
                    print('Error determining component')
                    return False

    okay = create_permutations(sensors, wireless_modules, batteries)
    return okay


# Create permutations (remember to account for quantities
def create_permutations(sensors, wireless_modules, batteries):
    ID = 0
    # TODO: Loop will now be different since only one class needed for components
    for battery in batteries:
        for wireless in wireless_modules:
            for sensor in sensors:
                [total_cost, total_volume] = sum_components(sensor, wireless, battery)
                total_cost += total_fixed_costs

                current_permutation = Components.Permutations('P' + format(ID, '05d'),
                                                              [sensor.ID, wireless.ID, battery.ID],
                                                              total_cost,
                                                              total_volume)

                if (current_permutation.cost <= constraints['cost']) and (current_permutation.volume <= constraints['volume']):
                    viable.append(current_permutation)
                else:
                    non_viable.append(current_permutation)

                ID += 1

    okay = record_permutations()
    return okay


def sum_components(sensor, wireless, battery):
    cost = (float(sensor.cost) * float(sensor.quantity)) + (float(wireless.cost) * float(wireless.quantity)) + (float(battery.cost) * float(battery.quantity))
    volume = (float(sensor.volume) * float(sensor.quantity)) + (float(wireless.volume) * float(wireless.quantity)) + (float(battery.volume) * float(battery.quantity))
    return [cost, volume]


# Write permutations to file
def record_permutations():
    # Viable Permutations
    with open('viable ' + permutations_filename + ' ' + datetime.now().strftime("%Y-%m-%d %H_%M_%S") + '.csv',
              'w',  newline='') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow(['ID', 'Total Cost', 'Total Volume', 'Components'])

        for permutation in viable:
            components = ''
            for component in permutation.components:
                components += component + '; '
            f_writer.writerow([permutation.ID, str(permutation.cost), str(permutation.volume), components])

    # Non-Viable Permutations
    with open('non-viable ' + permutations_filename + ' ' + datetime.now().strftime("%Y-%m-%d %H_%M_%S") + '.csv',
              'w',  newline='') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow(['ID', 'Total Cost', 'Total Volume', 'Components'])

        for permutation in non_viable:
            components = ''
            for component in permutation.components:
                components += component + '; '
            f_writer.writerow([permutation.ID, str(permutation.cost), str(permutation.volume), components])

    return True


if __name__ == '__main__':
    success = read_components(components_filename)
    print('Fixed Costs: ' + str(total_fixed_costs))
    print('Script Completed: ' + str(success))
