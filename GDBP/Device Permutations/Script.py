import Components

# TODO: - Try/catch read/writes
#       - Add sorting
#       - Use CSV files for Excel exporting
#       - Multiple sensor logic (for now different string IDs is the only way)

# Filenames
components_filename = 'components.txt'
permutations_filename = 'permutations.txt'


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
                if 'S' in fields[0]:
                    sensors.append(Components.Sensor(fields[0], fields[1], fields[2], fields[3]))
                elif 'W' in fields[0]:
                    wireless_modules.append(Components.Wireless(fields[0], fields[1], fields[2], fields[3]))
                elif 'B' in fields[0]:
                    batteries.append(Components.Battery(fields[0], fields[1], fields[2], fields[3]))
                else:
                    print('Error determining component: ' + fields[0])
                    return False

    okay = create_permutations(sensors, wireless_modules, batteries)
    return okay


# Create permutations (remember to account for quantities
def create_permutations(sensors, wireless_modules, batteries):
    ID = 0
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
    with open(permutations_filename, 'w') as f:
        f.write('Viable Permutations:\n\n')
        for permutation in viable:
            f.write('\tID: ' + permutation.ID + ',\n\tComponents: ')
            for component in permutation.components:
                f.write(component + ', ')
            f.write('\n\tUnit Cost: ' + str(permutation.cost) + ',\n')
            f.write('\tVolume: ' + str(permutation.volume) + '\n\n')

        f.write('\nNon-Viable Permutations:\n\n')
        for permutation in non_viable:
            f.write('\tID: ' + permutation.ID + ',\n\tComponents: ')
            for component in permutation.components:
                f.write(component + ', ')
            f.write('\n\tUnit Cost: ' + str(permutation.cost) + ',\n')
            f.write('\tVolume: ' + str(permutation.volume) + '\n\n')

    return True


if __name__ == "__main__":
    success = read_components(components_filename)
    print('Fixed Costs: ' + str(total_fixed_costs))
    print('Script Completed: ' + str(success))
