import pandas as pd
import readline
from street_abbreviations import STREET_TYPE_ABBREVIATIONS, STREET_SUFFIX_ABBREVIATIONS

SUBURBS_AND_ADJOINING_SUBURBS = pd.read_csv('suburbs-and-adjoining-suburbs.csv')
SUBURBS = SUBURBS_AND_ADJOINING_SUBURBS['SUBURB_NAME'].drop_duplicates().tolist()
STREET_NAMES_WITH_SUBURBS = pd.read_csv('street-names-with-suburbs.csv', keep_default_na=False)
WASTE_COLLECTION_DAYS_COLLECTION_DAYS = pd.read_csv('waste-collection-days-collection-days.csv')

STREET_NAMES_WITH_SUBURBS.loc[:, 'STREET TYPE'] = (
    STREET_NAMES_WITH_SUBURBS.loc[:, 'STREET TYPE'].str.upper().map(STREET_TYPE_ABBREVIATIONS)
)

STREET_NAMES_WITH_SUBURBS.loc[:, 'STREET SUFFIX'] = (
    STREET_NAMES_WITH_SUBURBS.loc[:, 'STREET SUFFIX'].apply(
        lambda suffix: STREET_SUFFIX_ABBREVIATIONS.get(suffix.upper(), '')
    )
)

# print(WASTE_COLLECTION_DAYS_COLLECTION_DAYS[(WASTE_COLLECTION_DAYS_COLLECTION_DAYS["UNIT_NUMBER"].notna()) & (WASTE_COLLECTION_DAYS_COLLECTION_DAYS["HOUSE_NUMBER_SUFFIX"].notna())])
# print(STREET_NAMES_WITH_SUBURBS["STREET TYPE"].drop_duplicates())
# print(STREET_NAMES_WITH_SUBURBS["STREET SUFFIX"].drop_duplicates())

def format_address(row):
    address = ''
    if pd.notna(row['UNIT_NUMBER']):
        address += f"{str(int(row['UNIT_NUMBER']))}/"

    address += str(row['HOUSE_NUMBER'])

    if pd.notna(row['HOUSE_NUMBER_SUFFIX']):
        address += row['HOUSE_NUMBER_SUFFIX']

    address += f" {row['STREET_NAME']}, {row['SUBURB']}"

    return address

suburb = None
suburb_streets = None
street_name = None
addresses = None

def suburb_completer(text, state):
    suburbs = list(filter(lambda suburb: suburb.startswith(text.upper()), SUBURBS))

    if not suburbs:
        return None

    return suburbs[state]

street_completer_num_calls = 0

def street_completer(text, state):
    if not suburb:
        return None

    streets = list(filter(lambda street: street.startswith(text.upper()), suburb_streets))

    if not streets:
        return None

    # print(matches)
    return streets[state]

def address_completer(text, state):
    if not suburb or not street_name:
        return None
    
    # matches = addresses[addresses.str.startswith(text)].tolist()
    matches = list(filter(lambda address: address.startswith(text), addresses))

    return matches[state]

def main():
    global suburb, suburb_streets, addresses, street_name

    readline.parse_and_bind('tab: menu-complete')
    print('--- Brisbane Bin Chicken Offering Day ---')

    readline.set_completer(suburb_completer)

    suburb = None
    while suburb not in SUBURBS:
        suburb = input('What suburb do you live in? ')
        if suburb not in SUBURBS:
            print(f"Please enter a valid suburb.")

    suburb_streets = STREET_NAMES_WITH_SUBURBS[STREET_NAMES_WITH_SUBURBS['SUBURB'] == suburb]
    suburb_streets = suburb_streets['STREET NAME'].str.cat(suburb_streets['STREET TYPE'], sep=' ').tolist()

    readline.set_completer(street_completer)

    street_name = None
    street_name = input('What street do you live in? ')

    addresses = WASTE_COLLECTION_DAYS_COLLECTION_DAYS[
        (WASTE_COLLECTION_DAYS_COLLECTION_DAYS["SUBURB"] == suburb) &
        (WASTE_COLLECTION_DAYS_COLLECTION_DAYS["STREET_NAME"] == street_name)
    ]
    addresses = addresses.apply(format_address, axis=1).tolist()

    readline.set_completer(address_completer)
    street_name = input('What is your address? ')


if __name__ == '__main__':
    main()