from datetime import date
import readline
import pandas as pd

def load_csv(file_path):
    return pd.read_csv(file_path)

def format_address(row):
    unit_number = ''
    if pd.notna(row['UNIT_NUMBER']):
        unit_number = f"{str(int(row['UNIT_NUMBER']))}/"

    house_number = str(row['HOUSE_NUMBER'])

    house_number_suffix = ''
    if pd.notna(row['HOUSE_NUMBER_SUFFIX']):
        house_number_suffix = row['HOUSE_NUMBER_SUFFIX']

    # address += f" {row['STREET_NAME']}, {row['SUBURB']}"
    street_name = row['STREET_NAME']
    suburb = row['SUBURB']

    address = f"{unit_number}{house_number}{house_number_suffix} {street_name}, {suburb}"

    return address

def create_completer(completion_matches):
    def completer(text, state):
        matches = list(filter(lambda match: match.startswith(text.upper()), completion_matches))
        titlecased_matches = list(map(
            lambda match: match.title(),
            matches
        ))

        if not titlecased_matches:
            return None

        return titlecased_matches[state]
    return completer

def main():
    suburbs_and_adjoining_suburbs = load_csv('suburbs-and-adjoining-suburbs.csv')
    waste_collection_days = load_csv('waste-collection-days-collection-days.csv')
    waste_collection_weeks = load_csv('waste-collection-days-collection-weeks.csv')

    suburbs = suburbs_and_adjoining_suburbs['SUBURB_NAME'].drop_duplicates().tolist()

    waste_collection_weeks['WEEK_STARTING'].apply(
        lambda week_starting: date.fromisoformat(week_starting)
    )

    waste_collection_weeks['WEEK_STARTING'] = pd.to_datetime(waste_collection_weeks['WEEK_STARTING'])

    suburb = None
    suburb_streets = None
    street_name = None
    address_input = None

    readline.parse_and_bind('tab: menu-complete')
    readline.set_completer_delims('')

    print('--- Brisbane Bin Chicken Offering Day ---')

    readline.set_completer(create_completer(suburbs))

    while suburb not in suburbs:
        suburb = input('What suburb do you live in? ').upper()
        if suburb not in suburbs:
            print(f"Please enter a valid suburb.")

    filtered_suburb_streets = waste_collection_days[waste_collection_days['SUBURB'] == suburb]
    suburb_streets = filtered_suburb_streets['STREET_NAME'].drop_duplicates().tolist()

    readline.set_completer(create_completer(suburb_streets))

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

    readline.set_completer(create_completer(addresses))
    
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