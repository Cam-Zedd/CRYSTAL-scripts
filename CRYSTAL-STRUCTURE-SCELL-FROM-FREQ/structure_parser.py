import os

def process_files_in_directory(directory_path):
    # Extensions à exclure
    excluded_extensions = {'.xyz', '.png', '.py', '.tiff', '.eps', '.svg', '.jpg', '.jpeg'}
    
    # Parcourir tous les fichiers dans le répertoire donné, et exclure ceux avec les extensions non désirées
    file_list = [f for f in os.listdir(directory_path) 
                 if os.path.isfile(os.path.join(directory_path, f)) and not f.endswith(tuple(excluded_extensions))]

    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)
        
        # Lire le fichier
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Trouver l'occurrence de "CARTESIAN COORDINATES - PRIMITIVE CELL"
        start_index = None
        num_lines_to_read = None
        
        for i, line in enumerate(lines):
            if "CARTESIAN COORDINATES - PRIMITIVE CELL" in line:
                start_index = i + 1  # Ligne de départ pour les coordonnées
            if "ATOMS IN THE ASYMMETRIC UNIT" in line:
                # Extraire le nombre de lignes à lire
                num_lines_to_read = int(line.split()[-1])  # Le dernier élément de la ligne contient le nombre

        if start_index is None or num_lines_to_read is None:
            print(f"Une information n'a pas été trouvée dans {file_name}")
            continue

        # Extraire les lignes 3 à num_lines_to_read + 3 après l'occurrence
        data_lines = lines[start_index + 3 : start_index + 3 + num_lines_to_read]

        # Ne conserver que les colonnes 2 à 5
        processed_data = []
        for line in data_lines:
            columns = line.split()
            if len(columns) >= 6:  # Vérifier qu'il y a assez de colonnes
                selected_columns = columns[2:6]  # Garder les colonnes 2 à 5 (indices 2, 3, 4, 5)
                processed_data.append(" ".join(selected_columns))

        # Créer le fichier .xyz (ajout de ".xyz" à la fin du nom du fichier original)
        xyz_filename = f"{file_name}.xyz"
        xyz_file_path = os.path.join(directory_path, xyz_filename)
        with open(xyz_file_path, 'w') as xyz_file:
            # Nombre de lignes
            xyz_file.write(f"{num_lines_to_read}\n")
            # Nom du fichier
            xyz_file.write(f"{file_name}\n")
            # Écrire les données extraites
            for line in processed_data:
                xyz_file.write(line + "\n")

        print(f"Fichier {xyz_filename} créé avec succès.")

# Exemple d'utilisation
directory_path = "C:\DATA\CLOUD2\GaS-GaSe\RAMAN\log"  # Remplace par ton répertoire
process_files_in_directory(directory_path)
