import os
import pandas as pd

cleaned_folder = "data/cleaned"

# Get only cleaned CSV files
files = [f for f in os.listdir(cleaned_folder) if f.endswith("_cleaned.csv")]

if not files:
    print("❌ No cleaned CSV files found in data/cleaned folder. Please check filenames.")
    exit()

merged_data = []

for file in files:
    file_path = os.path.join(cleaned_folder, file)
    print(f"📌 Adding: {file}")

    df = pd.read_csv(file_path)

    # Add business source column
    df["source"] = file.replace("_cleaned.csv", "")
    
    merged_data.append(df)

# Merge all
final_df = pd.concat(merged_data, ignore_index=True)

# Save as CSV + JSON for flexibility
final_df.to_csv("data/final_cleaned_dataset.csv", index=False)
final_df.to_json("data/final_cleaned_dataset.json", orient="records", indent=4, force_ascii=False)

print("\n🎉 SUCCESS! Final merged dataset created:")
print(f"📄 CSV: data/final_cleaned_dataset.csv")
print(f"📄 JSON: data/final_cleaned_dataset.json")
print(f"📊 Total Reviews: {len(final_df)}")
