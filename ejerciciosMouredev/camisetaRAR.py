
import zipfile
import os

def zip_file (path: str, file: str):

    file_path = os.path.join(path, file)

    if os.path.exists(file_path):

        zip_file = f"{file}.zip" # Concatenacion.  
        zip_path = os.path.join(path, zip_file)

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, zip_file)
            print(f"Archivo {file} comprimido como {zip_file}.")
    else:
        print(f"El archivo {file} no existe en el directorio {path}")


path = os.path.dirname(os.path.abspath(__file__)) # Calcula la ruta del sistema donde yo ejecuto el fichero.
file = "Tareas.pdf"    

zip_file(path, file)

