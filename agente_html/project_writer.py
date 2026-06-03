import re
from pathlib import Path


WORKSPACE_DIR = Path("workspace")


def extract_project_name(response_text: str) -> str:
    match = re.search(
        r'<project\s+name="([^"]+)">',
        response_text
    )

    if not match:
        raise ValueError("No se encontró <project name=\"...\">")

    return match.group(1).strip()


def extract_files(response_text: str):
    pattern = r'<file\s+name="([^"]+)">\s*(.*?)\s*</file>'

    files = re.findall(
        pattern,
        response_text,
        re.DOTALL
    )

    if not files:
        raise ValueError("No se encontraron etiquetas <file>...</file>")

    return files


def save_project_from_response(response_text: str) -> Path:
    project_name = extract_project_name(response_text)
    files = extract_files(response_text)

    project_dir = WORKSPACE_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in files:
        file_path = project_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(
            content.strip(),
            encoding="utf-8"
        )

        print(f"✓ Archivo creado: {file_path}")

    print(f"\nProyecto creado en: {project_dir}")

    return project_dir