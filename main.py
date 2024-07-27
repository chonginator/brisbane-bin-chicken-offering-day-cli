import pandas as pd
import readline
from suburbs import load_suburbs
from street_names import load_street_names
from street_abbreviations import STREET_TYPE_ABBREVIATIONS, STREET_SUFFIX_ABBREVIATIONS

SUBURBS_AND_ADJOINING_SUBURBS = pd.read_csv('suburbs-and-adjoining-suburbs.csv')
SUBURBS = SUBURBS_AND_ADJOINING_SUBURBS['SUBURB_NAME'].drop_duplicates()
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
    global SUBURBS
    matches = [suburb for suburb in SUBURBS if suburb.startswith(text.upper())]
    # print(matches)

    if not matches:
        return None

    return matches[state]

street_completer_num_calls = 0

def street_completer(text, state):
    global suburb, suburb_streets, street_completer_num_calls

    street_completer_num_calls += 1
    # print(f"Number of street completer calls: {street_completer_num_calls}")

    if not suburb:
        return None

    # suburb_streets = STREET_NAMES_WITH_SUBURBS[STREET_NAMES_WITH_SUBURBS['SUBURB'] == suburb]
    filtered_streets = suburb_streets[suburb_streets['STREET NAME'].str.startswith(text.upper())]

    matches = filtered_streets.apply(
        lambda row: f"{row['STREET NAME']} {row['STREET TYPE']} {row['STREET SUFFIX']}".strip(),
        axis=1
    ).tolist()

    # print(f"number of matches: {len(matches)}")

    if not matches:
        return None

    # print(matches)
    return matches[state]

def address_completer(text, state):
    global suburb, street_name

    if not suburb or not street_name:
        return None
    
    # filtered_addresses = WASTE_COLLECTION_DAYS_COLLECTION_DAYS[
    #     (WASTE_COLLECTION_DAYS_COLLECTION_DAYS["SUBURB"] == suburb) &
    #     (WASTE_COLLECTION_DAYS_COLLECTION_DAYS["STREET_NAME"] == street_name)
    # ]
    # print(filtered_addresses)


    # def format_address(row):
    #     address = ''
    #     if pd.notna(row['UNIT_NUMBER']):
    #         address += f"{str(int(row['UNIT_NUMBER']))}/"

    #     address += str(row['HOUSE_NUMBER'])

    #     if pd.notna(row['HOUSE_NUMBER_SUFFIX']):
    #         address += row['HOUSE_NUMBER_SUFFIX']

    #     address += f" {row['STREET_NAME']}, {row['SUBURB']}"

    #     return address

    # formatted_addresses = addresses.apply(format_address, axis=1)
    matches = addresses[addresses.str.startswith(text)].tolist()

    return matches[state]

def main():
    global suburb, suburb_streets, addresses, street_name

    readline.parse_and_bind('tab: menu-complete')
    print('--- Brisbane Bin Chicken Offering Day ---')

    readline.set_completer(suburb_completer)
    suburb = input('What suburb do you live in? ')

    suburb_streets = STREET_NAMES_WITH_SUBURBS[STREET_NAMES_WITH_SUBURBS['SUBURB'] == suburb]

    readline.set_completer(street_completer)
    street_name = input('What street do you live in? ')

    addresses = WASTE_COLLECTION_DAYS_COLLECTION_DAYS[
        (WASTE_COLLECTION_DAYS_COLLECTION_DAYS["SUBURB"] == suburb) &
        (WASTE_COLLECTION_DAYS_COLLECTION_DAYS["STREET_NAME"] == street_name)
    ]
    addresses = addresses.apply(format_address, axis=1)

    readline.set_completer(address_completer)
    street_name = input('What is your address? ')


if __name__ == '__main__':
    main()