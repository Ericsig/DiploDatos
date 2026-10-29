"""Ejecutar curación y modelado desde cualquier carpeta del proyecto.

Uso: python scripts/ejecutar_revision.py
Se usa el mismo intérprete que ejecuta este archivo, sin depender de un kernel global.
"""
import sys,time
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root=Path(__file__).resolve().parents[1]
for name in ['curacion','modelado']:
    p=root/'notebook'/f'{name}.ipynb'
    nb=nbformat.read(p,as_version=4)
    km=KernelManager(kernel_name='python3')
    km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
    started=time.time()
    def progress(cell_index,**kwargs):
        print(f'{name}: celda {cell_index+1}/{len(nb.cells)}',flush=True)
    try:
        NotebookClient(nb,timeout=3600,km=km,on_cell_start=progress,
            resources={'metadata':{'path':str(p.parent)}}).execute()
    finally:
        nbformat.write(nb,p)
    print(f'{name}: ejecutado en {time.time()-started:.1f} segundos',flush=True)

# Usa resultados recién calculados y comprueba la presentación editada por el equipo.
sys.path.insert(0, str(root/'notebook'))
from valores_presentacion import exportar_valores
_, audit = exportar_valores()
print(f"Presentación: {audit['graficos_verificados']} gráficos y "
      f"{audit['valores_graficos_verificados']} valores coinciden con los cálculos.")
