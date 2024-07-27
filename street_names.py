def load_street_names():
  with open("street-names-with-suburbs.csv", "r") as file:
    lines = file.readlines()

    street_names = set()
    for line in lines[1:]:
      fields = line.strip().split(",")
      name = fields[0]
      street_type = fields[1]
      street_suffix = fields[2]
      street_name = " ".join(filter(None, [name, street_type, street_suffix])).lower()
      street_names.add(street_name)
    
    return street_names
