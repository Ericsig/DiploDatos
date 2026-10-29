"""Regenerar la trazabilidad de cifras y verificar el PPTX final, sin reentrenar."""
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'notebook'))
from valores_presentacion import exportar_valores

if __name__ == '__main__':
    _, audit = exportar_valores()
    print(json.dumps(audit, ensure_ascii=False, indent=2))
