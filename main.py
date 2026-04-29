# ============================================================
# Unit 3 Deliverable: MedTrack — Patient Medication Tracker
# Name: Jalal el ghandour
# Course: CS 138 | MiraCosta College | Spring 2026
# Description: Track patient medications using lists,
#              dictionaries, and file I/O for data continuity.
# ============================================================

import json
import os

# ── DATA STRUCTURES ──────────────────────────────────────────
# Dictionary chosen for patients: each patient has a unique ID
# (the key), making lookups instant without scanning a whole list.
# List chosen for medications: order matters, duplicates allowed.

patients = {}
DATA_FILE = "patients_data.json"


# ── FILE I/O ─────────────────────────────────────────────────

def save_data():
    """Save all patient records to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(patients, f, indent=2)
    print("\n✅ Data saved to '" + DATA_FILE + "'.")


def load_data():
    """Load patient records from file if it exists."""
    global patients
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            patients = json.load(f)
        print("📂 Loaded " + str(len(patients)) + " patient record(s).")
    else:
        print("📋 No saved data found. Starting fresh.")


# ── RECURSION (BONUS) ─────────────────────────────────────────

def count_medications(patient_ids, index=0):
    """
    Recursively count total medications across all patients.
    Base case: index reaches end of list → return 0.
    Recursive case: add current patient's count + recurse.
    """
    if index == len(patient_ids):       # Base case
        return 0
    pid = patient_ids[index]
    current = len(patients[pid]["medications"])
    return current + count_medications(patient_ids, index + 1)


# ── FUNCTIONS ─────────────────────────────────────────────────

def add_patient():
    """Add a new patient to the records."""
    pid = input("Enter Patient ID (e.g., P001): ").strip().upper()
    if pid in patients:
        print("⚠️  Patient " + pid + " already exists.")
        return
    name = input("Enter Patient Name: ").strip().title()
    patients[pid] = {"name": name, "medications": []}
    print("\n✅ Patient '" + name + "' added with ID " + pid + ".")


def add_medication():
    """Add a medication entry to a patient's list."""
    pid = input("Enter Patient ID: ").strip().upper()
    if pid not in patients:
        print("❌ Patient not found.")
        return
    med_name  = input("Medication name: ").strip().title()
    dosage    = input("Dosage (e.g., 500mg): ").strip()
    frequency = input("Frequency (e.g., twice daily): ").strip()
    medication = {
        "name": med_name,
        "dosage": dosage,
        "frequency": frequency
    }
    patients[pid]["medications"].append(medication)
    print("\n✅ Added " + med_name + " to " + patients[pid]["name"] + "'s record.")


def view_patient():
    """Display a patient's full medication record."""
    pid = input("Enter Patient ID: ").strip().upper()
    if pid not in patients:
        print("❌ Patient not found.")
        return
    p = patients[pid]
    print("\n" + "-" * 40)
    print("  Patient: " + p["name"] + "  (ID: " + pid + ")")
    print("-" * 40)
    if not p["medications"]:
        print("  No medications on record.")
    else:
        for i, med in enumerate(p["medications"], start=1):
            print("  " + str(i) + ". " + med["name"] +
                  " — " + med["dosage"] +
                  " — " + med["frequency"])
    print("-" * 40 + "\n")


def view_all_patients():
    """List all patients with a medication summary."""
    if not patients:
        print("\n📋 No patients on record.\n")
        return
    pid_list = list(patients.keys())
    total_meds = count_medications(pid_list)
    print("\n" + "-" * 50)
    print("  {:<8} {:<20} {:>6}".format("ID", "Name", "# Meds"))
    print("-" * 50)
    for pid, data in patients.items():
        print("  {:<8} {:<20} {:>6}".format(
            pid, data["name"], len(data["medications"])))
    print("-" * 50)
    print("  Total patients: " + str(len(patients)) +
          "   |   Total medications: " + str(total_meds))
    print("-" * 50 + "\n")


def remove_medication():
    """Remove a medication from a patient's list."""
    pid = input("Enter Patient ID: ").strip().upper()
    if pid not in patients:
        print("❌ Patient not found.")
        return
    view_patient()
    if not patients[pid]["medications"]:
        return
    try:
        idx = int(input("Enter medication number to remove: ")) - 1
        removed = patients[pid]["medications"].pop(idx)
        print("✅ Removed '" + removed["name"] +
              "' from " + patients[pid]["name"] + "'s record.")
    except (IndexError, ValueError):
        print("❌ Invalid selection.")


# ── MAIN ──────────────────────────────────────────────────────

def main():
    load_data()
    print("\n" + "=" * 50)
    print("   💊 MedTrack — Patient Medication Tracker")
    print("=" * 50)

    while True:
        print("\n--- MENU ---")
        print("  1. Add New Patient")
        print("  2. Add Medication")
        print("  3. View Patient Record")
        print("  4. View All Patients")
        print("  5. Remove a Medication")
        print("  6. Save & Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            add_patient()
        elif choice == "2":
            add_medication()
        elif choice == "3":
            view_patient()
        elif choice == "4":
            view_all_patients()
        elif choice == "5":
            remove_medication()
        elif choice == "6":
            save_data()
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")


main()