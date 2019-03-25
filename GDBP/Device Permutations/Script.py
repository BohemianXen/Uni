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
enclosure_cost = 0
pcb_cost = 0
software_cost = 0
battery_cost = 0
misc = 0.0
total_fixed_costs = enclosure_cost + pcb_cost + software_cost + battery_cost + misc


# Constraints
constraints = {
    'cost': 125.00,  # GBP
    'volume': 80000  # mm^3
}


# Possible Permutations
variants = []
viable = []
non_viable = []


# Read components
def read_components(filename):
    with open(filename, 'r') as f_in:

        MEM = []
        CON = []
        MOT = []
        PRE = []
        HRT = []
        AIR = []
        PCB = []
        BLE = []
        WIFI = []
        WANT = []
        GPS = []
        BAT = []
        ENC = []

        for line in f_in:
            if line is not '\n':
                fields = line.split(',')
                if 'MEM' in fields[index['ID']]:
                    MEM.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'CON' in fields[index['ID']]:
                    CON.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'MOT' in fields[index['ID']]:
                    MOT.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'PRE' in fields[index['ID']]:
                    PRE.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'HRT' in fields[index['ID']]:
                    HRT.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'AIR' in fields[index['ID']]:
                    AIR.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'PCB' in fields[index['ID']]:
                    PCB.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'BLE' in fields[index['ID']]:
                    BLE.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'WIFI' in fields[index['ID']]:
                    WIFI.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'WANT' in fields[index['ID']]:
                    WANT.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'GPS' in fields[index['ID']]:
                    GPS.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'BAT' in fields[index['ID']]:
                    BAT.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'ENC' in fields[index['ID']]:
                    ENC.append(
                        Components.Component(fields[index['ID']], fields[index['cost']], fields[index['volume']], fields[index['quantity']]))
                elif 'Name' in fields[index['name']]:
                    continue
                else:
                    print('Error determining component')
                    return False

    okay = create_permutations(MEM, CON, MOT, PRE, HRT, AIR, PCB, BLE, WIFI, WANT, GPS, BAT, ENC)
    return okay


# Create permutations (remember to account for quantities
def create_permutations(MEM, CON, MOT, PRE, HRT, AIR, PCB, BLE, WIFI, WANT, GPS, BAT, ENC):
    ID = 0
    # TODO: Loop will now be different since only one class needed for components
    for enc in ENC:
        for bat in BAT:
            for gps in GPS:
                for want in WANT:
                    for wifi in WIFI:
                        for ble in BLE:
                            for pcb in PCB:
                                for air in AIR:
                                    for hrt in HRT:
                                        for pre in PRE:
                                            for mot in MOT:
                                                for con in CON:
                                                    for mem in MEM:
                                                        comps = [mem, con, mot, pre, hrt, air, pcb, ble, wifi, want, gps, bat, enc]
                                                        ids = list(map(lambda comp: comp.ID, comps))
                                                        [total_cost, total_volume] = sum_components(comps)
                                                        total_cost += total_fixed_costs

                                                        current_permutation = Components.Permutations('PER_' + format(ID, '05d'),
                                                                                                      ids,
                                                                                                      total_cost,
                                                                                                      total_volume)

                                                        if (current_permutation.cost <= constraints['cost']): # and (current_permutation.volume <= constraints['volume']):
                                                            viable.append(current_permutation)
                                                        else:
                                                            non_viable.append(current_permutation)

                                                        ID += 1

    okay = record_permutations()
    return okay


def sum_components(components):
    cost = 0
    volume = 0
    for component in components:
        cost += float(component.cost) * float(component.quantity)
        volume += float(component.volume) * float(component.quantity)

    return [cost, volume]


# Write permutations to file
def record_permutations():
    # Viable Permutations
    with open('viable ' + permutations_filename + ' ' + datetime.now().strftime("%Y-%m-%d %H_%M_%S") + '.csv',
              'w',  newline='') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow(['ID', 'Total Cost (£)', 'Total Volume (mm3)', 'Components'])

        for permutation in viable:
            components = ''
            for component in permutation.components:
                components += component + '; '
            f_writer.writerow([permutation.ID, str(permutation.cost), str(permutation.volume), components])

    # Non-Viable Permutations
    with open('non-viable ' + permutations_filename + ' ' + datetime.now().strftime("%Y-%m-%d %H_%M_%S") + '.csv',
              'w',  newline='') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow(['ID', 'Total Cost (£)', 'Total Volume (mm3)', 'Components'])

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
