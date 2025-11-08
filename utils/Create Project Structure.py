import os

project_structure = {
    "image_repair_agents/agents": [
        "__init__.py",
        "base.py",
        "detector.py",
        "router.py",
        "denoising.py",
        "inpainting.py",
        "deblurring.py",
        "superres.py"
    ],
    "image_repair_agents/models": [
        "__init__.py",
        "classifier_model.py",
        "restormer_wrapper.py",
        "utils.py"
    ],
    "image_repair_agents/evaluation": [
        "evaluator.py"
    ],
    "image_repair_agents/ui": [
        "app.py"
    ],
    "image_repair_agents/data/sample_images": [],
    "image_repair_agents": [
        "main.py",
        "config.py",
        "requirements.txt",
        "README.md"
    ]
}

def create_structure(structure):
    for folder, files in structure.items():
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")
        for file in files:
            file_path = os.path.join(folder, file)
            with open(file_path, 'w') as f:
                f.write(f"# {file}\n")
            print(f"  └─ Created file: {file_path}")

if __name__ == "__main__":
    create_structure(project_structure)