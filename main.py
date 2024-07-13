import re

def main():
  suburbs = load_suburbs()

  print("--- Brisbane Bin Chicken Offering Day ---")

  is_suburb_valid = False
  while not is_suburb_valid:
    suburb = input("What is your suburb? ").strip()
    if not suburb:
      print("Input cannot be empty. Please try again.")
    elif suburb.lower() not in suburbs:
      print("Invalid suburb. Please try again.")
    else:
      is_suburb_valid = True
      print(f"{suburb.capitalize()} is a valid suburb!")

  is_street_name_valid = False
  while not is_street_name_valid:
    street_name = input("What is your street name? ").strip()
    if not street_name:
      print("Input cannot be empty. Please try again.")
    elif street_name.lower() not in suburbs:
      print("Invalid street name. Please try again.")
    else:
      is_street_name_valid = True
      print(f"{street_name.capitalize()} is a valid street name!")

  is_street_name_valid = False

def load_suburbs():
  with open("suburbs-and-adjoining-suburbs.csv", "r") as file:
    lines = file.readlines()

    suburbs = set()
    for line in lines[1:]:
      suburb = line.strip().split(",")[0].lower()
      suburbs.add(suburb)

    return suburbs

if __name__ == "__main__":
  main()
  