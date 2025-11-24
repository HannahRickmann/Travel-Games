import os
import random
from PIL import Image
from collections import defaultdict

# === CONFIGURATION ===

script_dir = os.path.dirname(os.path.abspath(__file__))   # Path to "images" folder relative to this Python file
image_folder = os.path.join(script_dir, "images")
output_file = os.path.join(script_dir, "bingo_card.jpg")  # output file name
grid_size = 5                                             # 5x5 bingo
cell_size = 200                                           # each image cell will be resized to 200x200 pixels
margin = 50                                               # spacing between images in pixels
max_per_category = 3                                      # max images from the same category

# === STEP 1: Load images ===

# Load all image file paths
image_files = [
    os.path.join(image_folder, f)
    for f in os.listdir(image_folder)
    if f.lower().endswith(('.jpg', '.jpeg', '.png'))
]

image_files = [os.path.join(image_folder, f)
               for f in os.listdir(image_folder)
               if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

if len(image_files) < grid_size * grid_size:
    print(f"Gefundene Bilder: {len(image_files)}")
    #raise ValueError(f"Not enough images! Need {grid_size * grid_size}, found {len(image_files)}")

# Randomly choose 25 images
#chosen_files = random.sample(image_files, grid_size * grid_size)


# === STEP 1: Load images and assign categories ===
image_data = []  # (path, category)

for root, dirs, files in os.walk(image_folder):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png')):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, image_folder)
            parts = rel_path.split(os.sep)
            category = parts[0] if len(parts) > 1 else "other"
            image_data.append((full_path, category))

if not image_data:
    raise ValueError("Keine Bilder gefunden!")

print(f"{len(image_data)} Bilder geladen in {len(set(cat for _, cat in image_data))} Kategorien.")

# === STEP 2: Randomly pick 25 images ===
needed = grid_size * grid_size
chosen = random.sample(image_data, needed)

# === STEP 3: Check and fix category limits ===
def category_counts(images):
    counts = defaultdict(int)
    for _, cat in images:
        counts[cat] += 1
    return counts

counts = category_counts(chosen)
overfull = {cat: c for cat, c in counts.items() if c > max_per_category and cat != "other"}

if overfull:
    print("Zu viele aus Kategorien:", overfull)

    # create pools
    all_images = set(image_data)
    chosen_set = set(chosen)
    available = list(all_images - chosen_set)

    for cat, count in overfull.items():
        while counts[cat] > max_per_category and available:
            # find index of an overfull image
            for i, (path, c) in enumerate(chosen):
                if c == cat:
                    # replace it with a valid one
                    candidate = None
                    random.shuffle(available)
                    for new_img in available:
                        _, new_cat = new_img
                        if new_cat == "other" or category_counts(chosen)[new_cat] < max_per_category:
                            candidate = new_img
                            break
                    if candidate:
                        chosen[i] = candidate
                        available.remove(candidate)
                        counts = category_counts(chosen)
                    break

# === STEP 4: Build bingo grid ===
grid_width = grid_size * cell_size + (grid_size + 1) * margin
grid_height = grid_width
bingo_card = Image.new("RGB", (grid_width, grid_height), color="white")

# === STEP 5: Paste images ===
for i, (path, cat) in enumerate(chosen):
    img = Image.open(path).convert("RGBA")
    img = Image.alpha_composite(Image.new("RGBA", img.size, "WHITE"), img).convert("RGB")
    img = img.resize((cell_size, cell_size))
    x = margin + (i % grid_size) * (cell_size + margin)
    y = margin + (i // grid_size) * (cell_size + margin)
    bingo_card.paste(img, (x, y))

# === STEP 6: Save output ===
bingo_card.save(output_file)
print(f"Bingo-Karte gespeichert als {output_file}")