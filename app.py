import base64
import os
import shutil
import tkinter as tk
import zipfile

import requests

appdata = os.getenv("APPDATA")
xmars_path = f"{appdata}\\.minecraft\\resourcepacks\\project_xmars.zip"
icone = "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"


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
                file.write(ultimo_commit.encode("utf-8"))

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

photo = tk.PhotoImage(data=base64.b64decode(icone))
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
