# Brisbane Bin Chicken Offering Day

A Python command-line tool to help Brisbane residents check when to make their weekly food offerings to the sacred bin chickens, i.e., check when their bin collection day is and what bins to take out.

### Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.6 or higher
- pip (Python package installer)

You can check to see if you have Python and pip installed by running:

```sh
  python --version
  pip --version
```

First, clone the repository:

```sh
git clone https://github.com/your-username/bin-chicken-offering-day.git
cd bin-chicken-offering-day
```

Then install the required packages using the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

Ensure you have the required data files in the root directory. You need:
- `suburbs-and-adjoining-suburbs.csv`
- `waste-collection-days-collection-days.csv`
- `waste-collection-weeks-collection-weeks.csv`

### Running the Program
Once you have everything set up, you can run the program using:

```sh
python main.py
```

Follow the on-screen prompts to enter you suburb, street, and address to get your bin collection details. You can press 'tab' to cycle through the autocomplete options.

### Example Usage

```text
$ python main.py
--- Brisbane Bin Chicken Offering Day ---
What suburb do you live in? Kangaroo Point
What street do you live in? Main st
What is your address? 1/123 Main St, Kangaroo Point
Your bin collection day is Wednesday.
Don't forget to take out your yellow recycling bin!
```
