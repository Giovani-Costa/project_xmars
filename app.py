import os
import shutil
import tkinter as tk
import zipfile

import requests

appdata = os.getenv("APPDATA")
xmars_path = f"{appdata}\\.minecraft\\resourcepacks\\project_xmars.zip"


def get_last_commit_hash():
    url = "https://api.github.com/repos/Giovani-Costa/project_xmars/commits"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    commits = response.json()
    return commits[0]["sha"]


def downloadand_repack_zip():
    """
    Downloads a zip file, removes the top-level directory, and saves the
    contents as a new zip file.

    Args:
      url: The URL of the zip file.
      save_path: The path where the new zip file should be saved.
    """
    try:
        response = requests.get(
            "https://github.com/Giovani-Costa/project_xmars/archive/refs/heads/main.zip",
            stream=True,
        )
        response.raise_for_status()

        temp_dir = "temp_zip_extract"  # Create a temporary directory
        os.makedirs(temp_dir, exist_ok=True)

        with open("temp.zip", "wb") as f:  # Save the downloaded zip file
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        with zipfile.ZipFile("temp.zip", "r") as zip_ref:
            zip_ref.extractall(temp_dir)  # Extract to the temporary directory

        os.remove("temp.zip")  # Remove the temporary downloaded zip file

        # Get the name of the top-level directory
        root_folder = os.listdir(temp_dir)[0]
        extracted_path = os.path.join(temp_dir, root_folder)

        # Create the new zip file
        with zipfile.ZipFile(xmars_path, "w") as new_zip:
            for root, _, files in os.walk(extracted_path):
                # Remove the root folder from the paths in the new zip
                relative_path = os.path.relpath(root, extracted_path)
                for file in files:
                    new_zip.write(
                        os.path.join(root, file),
                        arcname=os.path.join(relative_path, file),
                    )

        shutil.rmtree(temp_dir)  # Clean up the temporary directory
        print("File downloaded and repacked successfully")
        with zipfile.ZipFile(xmars_path, "a") as zip_ref:
            with zip_ref.open("version.txt", "w") as file:
                file.write(ultimo_commit.enconde("utf-8"))

        tk.Label(frame, text="Está atualizado na última versão").grid(column=0, row=2)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
    except Exception as e:
        print(f"Error processing zip file: {e}")


ultimo_commit = get_last_commit_hash()
versao_atual = ""
if os.path.isfile(xmars_path):
    with zipfile.ZipFile(xmars_path, "r") as zip_ref:
        with zip_ref.open("version.txt", "r") as file:
            versao_atual = file.read().decode("utf-8")  # Decode to string


is_uptade = versao_atual == ultimo_commit

root = tk.Tk()

photo = tk.PhotoImage(file="pack.png")
root.wm_iconphoto(False, photo)

root.wm_title("XMars Updater")

root.maxsize(1000, 400)

frame = tk.Frame(root)
frame.grid(padx=200, pady=200)
tk.Label(frame, text=f"Última versão: {ultimo_commit[:7]}").grid(column=0, row=0)
tk.Label(frame, text=f"Versão atual: {versao_atual[:7]}").grid(column=0, row=1)
if is_uptade:
    tk.Label(frame, text="Está atualizado na última versão").grid(column=0, row=2)
else:
    tk.Label(frame, text="NÃO ESTÁ NA ÚLTIMA VERSÃO").grid(column=0, row=2)

botao_atualizar = tk.Button(
    frame,
    text="Atulizar",
    command=downloadand_repack_zip,
)
botao_atualizar.grid(column=1, row=3)
if is_uptade:
    botao_atualizar["state"] = tk.DISABLED

root.mainloop()
