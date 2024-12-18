import json
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory, asksaveasfilename

def preprocess_wikisimple(input_folder, output_file):
    normal_file = f"{input_folder}/normal.txt"
    simple_file = f"{input_folder}/simple.txt"

    with open(normal_file, 'r', encoding='utf-8') as normal, \
         open(simple_file, 'r', encoding='utf-8') as simple, \
         open(output_file, 'w', encoding='utf-8') as output:
        # Procesează liniile
        for normal_line, simple_line in zip(normal, simple):
            data = {
                "normal": normal_line.strip(),
                "simplified": simple_line.strip()
            }
            output.write(json.dumps(data) + "\n")

def preprocess_asset(input_dir, output_file):
    """Preprocess Asset dataset (test and valid) and convert to JSON."""
    normal_files = [
        os.path.join(input_dir, "asset.test.orig"),
        os.path.join(input_dir, "asset.valid.orig")
    ]
    simplified_file_groups = [
        [os.path.join(input_dir, f"asset.test.simp.{i}") for i in range(10)],
        [os.path.join(input_dir, f"asset.valid.simp.{i}") for i in range(10)]
    ]
    pairs = []
    for normal_file, simplified_files in zip(normal_files, simplified_file_groups):
        try:
            with open(normal_file, 'r', encoding='utf-8') as n_file:
                normal_lines = [line.strip() for line in n_file]
            simplified_lines = []
            for simp_file in simplified_files:
                with open(simp_file, 'r', encoding='utf-8') as s_file:
                    simplified_lines.append([line.strip() for line in s_file])
            for i, normal_text in enumerate(normal_lines):
                simplified_versions = [simp_lines[i] for simp_lines in simplified_lines]
                pairs.append({"normal": normal_text, "simplified": simplified_versions})
        except FileNotFoundError as e:
            print(f"Error: {e}")
    # Save as JSON
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(pairs, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Initialize Tkinter and hide root window
    Tk().withdraw()

    dataset_type = input("Enter dataset type (wiki/asset): ").strip().lower()
    if dataset_type == "wiki":
        print("Select the WikiSimple input file:")
        wiki_input_file = askdirectory()
        print("Select the location and name for the output JSON file:")
        wiki_output_file = asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        preprocess_wikisimple(wiki_input_file, wiki_output_file)
        print(f"WikiSimple dataset converted and saved to {wiki_output_file}.")

    elif dataset_type == "asset":
        print("Select the Asset input directory:")
        asset_input_dir = askdirectory()
        print("Select the location and name for the output JSON file:")
        asset_output_file = asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        preprocess_asset(asset_input_dir, asset_output_file)
        print(f"Asset dataset converted and saved to {asset_output_file}.")
    else:
        print("Invalid dataset type. Please enter 'wiki' or 'asset'.")
