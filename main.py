from datetime import date
import readline
import pandas as pd

def load_csv(file_path):
    return pd.read_csv(file_path)

suburbs_and_adjoining_suburbs = load_csv('suburbs-and-adjoining-suburbs.csv')
street_names_with_suburbs = load_csv('street-names-with-suburbs.csv')
waste_collection_days = load_csv('waste-collection-days-collection-days.csv')
waste_collection_weeks = load_csv('waste-collection-days-collection-weeks.csv')

suburbs = suburbs_and_adjoining_suburbs['SUBURB_NAME'].drop_duplicates().tolist()

waste_collection_weeks['WEEK_STARTING'].apply(
    lambda week_starting: date.fromisoformat(week_starting)
)

waste_collection_weeks['WEEK_STARTING'] = pd.to_datetime(waste_collection_weeks['WEEK_STARTING'])

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
address_input = None

def suburb_completer(text, state):
    matches = list(filter(lambda suburb: suburb.startswith(text.upper()), suburbs))
    titlecased_matches = list(map(
        lambda suburb: suburb.title(),
        matches
    ))

    if not titlecased_matches:
        return None

    return titlecased_matches[state]

def street_completer(text, state):
    if not suburb_streets:
        return None

    matches = list(filter(lambda street: street.startswith(text.upper()), suburb_streets))
    titlecased_matches = list(map(
        lambda street: street.title(),
        matches
    ))

    if not titlecased_matches:
        return None

    return titlecased_matches[state]

def address_completer(text, state):
    if not addresses:
        return None
    
    matches = list(filter(lambda address: address.startswith(text), addresses))
    titlecased_matches = list(map(lambda address: address.title(), matches))

    return titlecased_matches[state]

def main():
    global suburb, suburb_streets, street_name, address_input, addresses

    readline.parse_and_bind('tab: menu-complete')
    readline.set_completer_delims('')

    print('--- Brisbane Bin Chicken Offering Day ---')

    readline.set_completer(suburb_completer)

    while suburb not in suburbs:
        suburb = input('What suburb do you live in? ').upper()
        if suburb not in suburbs:
            print(f"Please enter a valid suburb.")

    filtered_suburb_streets = waste_collection_days[waste_collection_days['SUBURB'] == suburb]
    suburb_streets = filtered_suburb_streets['STREET_NAME'].drop_duplicates().tolist()

    readline.set_completer(street_completer)

    street_name = None
    while street_name not in suburb_streets:
        street_name = input('What street do you live in? ').upper()

        if street_name not in suburb_streets:
            print(f"Please enter a valid street.")

    filtered_addresses = waste_collection_days[
        (waste_collection_days["SUBURB"] == suburb) &
        (waste_collection_days["STREET_NAME"] == street_name)
    ]
    addresses = filtered_addresses.apply(format_address, axis=1).tolist()

    readline.set_completer(address_completer)
    
    while address_input not in addresses:
        address_input = input('What is your address? ').upper()
        if address_input not in addresses:
            print(f"Please enter a valid address")

    address = filtered_addresses.iloc[addresses.index(address_input)]
    collection_day = address['COLLECTION_DAY']
    address_zone = address['ZONE']
    print(f"Your bin collection day is {collection_day.title()}.")

    today = pd.to_datetime(date.today())
    week_starting = waste_collection_weeks[waste_collection_weeks['WEEK_STARTING'] <= today].tail(1)
    zone_for_the_week = week_starting['ZONE'].item().upper()
    
    if address_zone == zone_for_the_week:
        print("Don't forget to take out your yellow recycling bin!")
    else:
        print("Don't forget to take out your green waste bin!")

if __name__ == '__main__':
    main()