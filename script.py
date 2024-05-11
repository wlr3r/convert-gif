import PyInstaller.__main__

PyInstaller.__main__.run([
    'convert.py',  # Remplacez 'votre_script_principal.py' par le nom de votre script principal
    '--onefile',  # Crée un seul fichier exécutable
    '--windowed',  # Masque la console lors de l'exécution de l'application
    '--name=Convert',  # Remplacez 'Nom_de_votre_application' par le nom souhaité pour votre exécutable
    '--icon=convert.ico',  # Remplacez 'icone.ico' par le chemin de votre icône (facultatif)
])