# Travel Game – Travel Bingo

Travel Bingo is a small Python game that generates a printable bingo card filled with things you might spot while traveling (car rides, train rides, etc.).
Items are organized into subcategories—such as animals or transport—and the generator ensures no category is over-represented (max three items per category). This keeps each bingo card varied and fun.

## 📁 Repository Structure
```text
/travel-bingo
│
├── travel-bingo.py        # Main script to generate a bingo card
├── bingo_card.jpg         # Output file (generated after running the script)
└── images/                # Folder containing images used on the bingo card
    ├── animals/
    ├── transport/
    └── ...
```

- `travel_bingo.py`:  The executable Python file. Running it will select random items, enforce category balancing, and generate a new bingo card image.

- `images/`-folder: Contains all available icons/photos grouped into subcategories. The script automatically uses these images when building the bingo card.

## 🎲 How It Works

The script scans all subfolders inside images/.

Each subfolder is treated as a subcategory (e.g., animals, transport).

Items are randomly chosen to fill the bingo grid.

A rule ensures that no more than 3 images from the same subcategory appear on a single bingo card.

A completed bingo card image (e.g., bingo-card.png) is generated.

## ▶️ How to Run

Make sure you have Python 3 installed.

```bash
python travel_bingo.py
```

A bingo card image will appear in the repository directory after execution.

## 🧩 Features

Automatic bingo card generation

Category balancing to avoid duplicates or overuse

Expandable image library—just drop new images into subfolders

Reproducible and easy to modify

## ➕ Adding More Items

To add new things players can spot:

Create a new subfolder inside images/ or add an image to an existing category.

Make sure the file is an image format supported by your script (e.g., PNG/JPG).

The generator will automatically include it in future cards.
