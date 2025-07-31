from formula_parser import calculate_molar_mass

AVOGADROS_NUMBER = 6.022e23  # atoms/moles
MOLAR_VOLUME_STP = 22.4      # liters/mole (for gases at STP)

# --- Conversions ---

def grams_to_moles(grams, formula):
    try:
        molar_mass = calculate_molar_mass(formula)
    except ValueError as e:
        print(f"❌ Error: {e}")
        exit()
    return grams / molar_mass

def moles_to_grams(moles, formula):
    try:
        molar_mass = calculate_molar_mass(formula)
    except ValueError as e:
        print(f"❌ Error: {e}")
        exit()
    return moles * molar_mass

def moles_to_atoms(moles):
    return moles * AVOGADROS_NUMBER

def atoms_to_moles(atoms):
    return atoms / AVOGADROS_NUMBER

def volume_to_moles(volume_liters):
    return volume_liters / MOLAR_VOLUME_STP

def molarity_to_moles(molarity, volume_liters):
    return molarity * volume_liters

# --- Main program ---
if __name__ == "__main__":
    print("==== Mole ↔ Mass ↔ Atoms ↔ Volume Tool ====")
    print("1: Convert grams → moles")
    print("2: Convert moles → grams")
    print("3: Convert moles → atoms")
    print("4: Convert atoms → moles")
    print("5: Convert grams → atoms")
    print("6: Convert atoms → grams")
    print("7: Convert volume (L) → moles (gas at STP)")
    print("8: Convert molarity (M) and volume (L) → moles")
    
    choice = input("Choose an option (1–8): ").strip()

    if choice in ("1", "2", "5", "6"):
        formula = input("Enter an element or chemical formula (e.g. H2O, Ca(OH)2, CuSO4·5H2O): ").strip()

    if choice == "1":
        grams = float(input("Enter mass in grams: "))
        moles = grams_to_moles(grams, formula)
        print(f"{grams} grams of {formula} = {moles:.6f} moles")

    elif choice == "2":
        moles = float(input("Enter amount in moles: "))
        grams = moles_to_grams(moles, formula)
        print(f"{moles} moles of {formula} = {grams:.6f} grams")

    elif choice == "3":
        moles = float(input("Enter amount in moles: "))
        atoms = moles_to_atoms(moles)
        print(f"{moles} moles = {atoms:.3e} atoms/molecules")

    elif choice == "4":
        atoms_input = input("Enter number of atoms/molecules: ").strip()
        atoms_input = atoms_input.replace("*10", "e").replace("×10", "e")
        try:
            atoms = float(atoms_input)
        except ValueError:
            print("❌ Invalid number format. Please use something like 6.02e23 or 6.02*10^23.")
            exit()
        moles = atoms_to_moles(atoms)
        print(f"{atoms:.3e} atoms/molecules = {moles:.6f} moles")

    elif choice == "5":
        grams = float(input("Enter mass in grams: "))
        moles = grams_to_moles(grams, formula)
        atoms = moles_to_atoms(moles)
        print(f"{grams} grams of {formula} = {atoms:.3e} atoms/molecules")

    elif choice == "6":
        atoms_input = input("Enter number of atoms/molecules: ").strip()
        atoms_input = atoms_input.replace("*10", "e").replace("×10", "e")
        try:
            atoms = float(atoms_input)
        except ValueError:
            print("❌ Invalid number format.")
            exit()
        moles = atoms_to_moles(atoms)
        grams = moles_to_grams(moles, formula)
        print(f"{atoms:.3e} atoms of {formula} = {grams:.6f} grams")

    elif choice == "7":
        volume = float(input("Enter volume in liters: "))
        moles = volume_to_moles(volume)
        print(f"{volume} L of gas at STP = {moles:.6f} moles")

    elif choice == "8":
        molarity = float(input("Enter molarity (mol/L): "))
        volume = float(input("Enter volume (L): "))
        moles = molarity_to_moles(molarity, volume)
        print(f"{volume} L of {molarity} M solution = {moles:.6f} moles")

    else:
        print("Invalid choice. Please enter a number from 1 to 8.")