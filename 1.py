import csv

# Function to generate unique passwords and update the CSV
def update_csv_with_passwords(input_file, output_file):
    updated_rows = []
    with open("NOW.csv", "r") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Password"] if "Password" not in reader.fieldnames else reader.fieldnames
        
        for row in reader:
            # Generate password
            name = row["Name"].strip().lower()
            mobile = row["Mobile Number"].strip()
            password = name[:4] + mobile[:4]
            row["Password"] = password
            updated_rows.append(row)

    # Write to new file
    with open("hi", "w", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

# File paths
input_csv = "NOW.csv"
output_csv = "hi.csv"

update_csv_with_passwords(input_csv, output_csv)
print(f"Updated file saved as {output_csv}.")
