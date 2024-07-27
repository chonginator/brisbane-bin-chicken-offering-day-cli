def load_suburbs():
  with open("suburbs-and-adjoining-suburbs.csv", "r") as file:
    lines = file.readlines()

    suburbs = set()
    for line in lines[1:]:
      suburb = line.strip().split(",")[0].lower()
      suburbs.add(suburb)

    return suburbs
