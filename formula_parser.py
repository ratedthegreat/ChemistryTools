import re
import json

# ------------------ Helper Functions ------------------

def multiply_group(group_dict, multiplier):
    """Multiplies all element counts in a dictionary by a multiplier."""
    return {element: count * multiplier for element, count in group_dict.items()}

def merge_dicts(dict1, dict2):
    """Merges two dictionaries of elements by adding the counts."""
    for element, count in dict2.items():
        dict1[element] = dict1.get(element, 0) + count
    return dict1

# ------------------ Formula Parser ------------------

def parse_formula(formula):
    """
    Parses a chemical formula string into a dictionary of element counts.
    Supports nested parentheses like Ca(OH)2 or Al2(SO4)3.
    """
    stack = []
    i = 0

    while i < len(formula):
        if formula[i] == "(":
            stack.append("(")
            i += 1
        elif formula[i] == ")":
            i += 1
            multiplier = ''
            while i < len(formula) and formula[i].isdigit():
                multiplier += formula[i]
                i += 1
            multiplier = int(multiplier) if multiplier else 1
            group = {}
            while stack and stack[-1] != "(":
                group = merge_dicts(group, stack.pop())
            stack.pop()  # Remove the "("
            stack.append(multiply_group(group, multiplier))
        else:
            match = re.match(r"([A-Z][a-z]?)(\d*)", formula[i:])
            if match:
                symbol = match.group(1)
                count = int(match.group(2)) if match.group(2) else 1
                stack.append({symbol: count})
                i += len(match.group(0))
            else:
                raise ValueError(f"Invalid formula at index {i}: {formula[i:]}")
    
    result = {}
    for group in stack:
        result = merge_dicts(result, group)

    return result

# ------------------ Hydrate Parser ------------------

def parse_formula_with_hydrate(formula):
    """
    Supports dot-separated hydrates like CuSO4·5H2O or CuSO4.5H2O.
    Splits and parses each part and combines them.
    """
    formula = formula.strip()
    formula = formula.replace('[', '(').replace(']', ')')
    parts = re.split(r"[·.]", formula)
    final_result = {}

    for part in parts:
        part = part.strip()
        match = re.match(r"^(\d+)([A-Za-z(].*)$", part)
        if match:
            multiplier = int(match.group(1))
            subformula = match.group(2)
            parsed = parse_formula(subformula)
            parsed = {el: cnt * multiplier for el, cnt in parsed.items()}
        else:
            parsed = parse_formula(part)

        for element, count in parsed.items():
            final_result[element] = final_result.get(element, 0) + count

    return final_result

# ------------------ Molar Mass Calculator ------------------

def calculate_molar_mass(formula):
    """
    Calculates the molar mass of a chemical compound using parsed formula.
    Works with JSON formatted like: {"elements": [{"symbol": "H", "atomic_mass": 1.008}, ...]}
    """
    with open("chemistry_tools/PeriodicTableJSON.json", "r") as f:
        data = json.load(f)

    # Build symbol → atomic_mass dictionary from list
    periodic_table = {}
    for element in data["elements"]:
        symbol = element["symbol"]
        mass = element.get("atomic_mass")
        if symbol and isinstance(mass, (int, float)):
            periodic_table[symbol] = mass

    elements = parse_formula_with_hydrate(formula)

    total_mass = 0.0

    for symbol, count in elements.items():
        if symbol in periodic_table:
            total_mass += periodic_table[symbol] * count
        else:
            raise ValueError(f"Element '{symbol}' not found in periodic table.")

    return total_mass

# ------------------ Testing ------------------

if __name__ == "__main__":
    test_formula = "CuSO4·5H2O"
    print("Parsed:", parse_formula_with_hydrate(test_formula))
    print("Molar Mass of", test_formula, "=", calculate_molar_mass(test_formula), "g/mol")