from datetime import date
import readline
import pandas as pd

def load_data(file_paths):
    return [pd.read_csv(path) for path in file_paths]

def format_address(address):
    unit_number = address['UNIT_NUMBER']
    house_number_suffix = address['HOUSE_NUMBER_SUFFIX']
    house_number = str(address['HOUSE_NUMBER'])
    street_name = address['STREET_NAME']
    suburb = address['SUBURB']

    unit_number = f"{str(int(unit_number))}/" if pd.notna(unit_number) else ''
    house_number_suffix = f"{house_number_suffix}" if pd.notna(house_number_suffix) else ''

    address = f"{unit_number}{house_number}{house_number_suffix} {street_name}, {suburb}"

    return address

def create_completer_from(completion_matches):
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

def get_validated_input(prompt, valid_options):
    user_input = None
    while user_input not in valid_options:
        user_input = input(prompt).upper()

        if user_input not in valid_options:
            print("Please enter a valid option.")

    return user_input

def print_collection_message_for_address(address):
    collection_day = address['COLLECTION_DAY']

    print(f"Your bin collection day is {collection_day.title()}.")
    
    if is_yellow_recycling_bin_week_for_address(address):
        print("Don't forget to take out your yellow recycling bin!")
    else:
        print("Don't forget to take out your green waste bin!")

def is_yellow_recycling_bin_week_for_address(address):
    waste_collection_weeks = pd.read_csv('waste-collection-days-collection-weeks.csv')
    waste_collection_weeks['WEEK_STARTING'] = pd.to_datetime(waste_collection_weeks['WEEK_STARTING'])

    zone = address['ZONE']

    today = pd.to_datetime(date.today())
    week_starting = waste_collection_weeks[waste_collection_weeks['WEEK_STARTING'] <= today].tail(1)
    zone_for_the_week = week_starting['ZONE'].item().upper()

    if zone == zone_for_the_week:
        return True
    return False

def main():
    suburbs_and_adjoining_suburbs, waste_collection_days = load_data([
        'suburbs-and-adjoining-suburbs.csv',
        'waste-collection-days-collection-days.csv'
    ])

    suburbs = suburbs_and_adjoining_suburbs['SUBURB_NAME'].drop_duplicates().tolist()

    readline.parse_and_bind('tab: menu-complete')
    readline.set_completer_delims('')

    print('--- Brisbane Bin Chicken Offering Day ---')

    readline.set_completer(create_completer_from(suburbs))
    suburb = get_validated_input(
        'What suburb do you live in? ',
        suburbs
    )

    filtered_suburb_streets = waste_collection_days[waste_collection_days['SUBURB'] == suburb]
    suburb_streets = filtered_suburb_streets['STREET_NAME'].drop_duplicates().tolist()

    readline.set_completer(create_completer_from(suburb_streets))
    street_name = get_validated_input(
        'What street do you live in? ',
        suburb_streets
    )

    filtered_addresses = waste_collection_days[
        (waste_collection_days["SUBURB"] == suburb) &
        (waste_collection_days["STREET_NAME"] == street_name)
    ]
    addresses = filtered_addresses.apply(format_address, axis=1).tolist()

    readline.set_completer(create_completer_from(addresses))
    address_input = get_validated_input('What is your address? ', addresses)

    address = filtered_addresses.iloc[addresses.index(address_input)]

    print_collection_message_for_address(address)

if __name__ == '__main__':
    main()