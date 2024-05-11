import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image
import os
import socket
import requests
import uuid
import subprocess

ACCESS_KEY_FILE = "access_key.txt"
WEBHOOK_URL = "WEBHOOK HERE"

cle_entree = None

def generer_et_envoyer_cle():
    try:
        cle_acces = str(uuid.uuid4())
        session_utilisateur = subprocess.check_output('whoami').decode().strip()
        
        reponse = requests.get("https://api.ipify.org")
        adresse_ip_publique = reponse.text
        
        message = {"content": f"Nouvelle clé d'accès générée par {session_utilisateur} depuis l'adresse IP publique : {adresse_ip_publique}\nClé : {cle_acces}",
                   "username": "Générateur de clés"}
        reponse = requests.post(WEBHOOK_URL, json=message)
        reponse.raise_for_status()
        print("Clé d'accès envoyée avec succès !")
        with open(ACCESS_KEY_FILE, "w") as f:
            f.write(cle_acces)
    except Exception as e:
        print(f"Erreur lors de l'envoi de la clé d'accès : {e}")

def verifier_cle_utilisateur():
    if os.path.exists(ACCESS_KEY_FILE):
        with open(ACCESS_KEY_FILE, "r") as f:
            cle_acces = f.read().strip()
            cle_utilisateur = cle_entree.get().strip()
            if cle_utilisateur == cle_acces:
                print("Clé correcte. Accès autorisé !")
                return True
            else:
                print("Clé incorrecte. Réessayez.")
                return False
    else:
        print("La clé d'accès n'a pas été générée. Veuillez contacter l'administrateur.")
        return False

def montrer_convertisseur():
    if verifier_cle_utilisateur():
        racine.withdraw()
        fenetre_convertisseur.deiconify()

def convertir():
    chemin_gif = champ_entree.get()
    dossier_sortie = champ_sortie.get()
    if chemin_gif and dossier_sortie:
        if variable.get() == 1:
            convertir_en_png(chemin_gif, dossier_sortie)
        elif variable.get() == 2:
            convertir_en_jpeg(chemin_gif, dossier_sortie)

def choisir_fichier():
    chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers GIF", "*.gif")])
    if chemin_fichier:
        champ_entree.delete(0, tk.END)
        champ_entree.insert(0, chemin_fichier)

def choisir_dossier():
    chemin_dossier = filedialog.askdirectory()
    if chemin_dossier:
        champ_sortie.delete(0, tk.END)
        champ_sortie.insert(0, chemin_dossier)

def convertir_en_png(chemin_gif, dossier_sortie):
    gif = Image.open(chemin_gif)
    dossier_converti = os.path.join(dossier_sortie, "Convert")
    os.makedirs(dossier_converti, exist_ok=True)
    for i in range(gif.n_frames):
        gif.seek(i)
        cadre = gif.copy().convert('RGBA')
        cadre.save(os.path.join(dossier_converti, f"frame_{i}.png"), format="PNG")
    messagebox.showinfo("Conversion terminée", "Conversion terminée en PNG !")

def convertir_en_jpeg(chemin_gif, dossier_sortie):
    gif = Image.open(chemin_gif)
    dossier_converti = os.path.join(dossier_sortie, "Convert")
    os.makedirs(dossier_converti, exist_ok=True)
    for i in range(gif.n_frames):
        gif.seek(i)
        cadre = gif.copy().convert('RGB')
        cadre.save(os.path.join(dossier_converti, f"frame_{i}.jpg"), format="JPEG")
    messagebox.showinfo("Conversion terminée", "Conversion terminée en JPEG !")

def nettoyer():
    if os.path.exists(ACCESS_KEY_FILE):
        os.remove(ACCESS_KEY_FILE)
        print("Fichier access_key.txt supprimé avec succès !")
    else:
        print("Le fichier access_key.txt n'existe pas.")

def a_la_fermeture():
    nettoyer()
    racine.quit()

def a_la_fermeture_convertisseur():
    fenetre_convertisseur.withdraw()
    racine.deiconify()
    nettoyer()

if not os.path.exists(ACCESS_KEY_FILE):
    generer_et_envoyer_cle()

racine = tk.Tk()
racine.title("Convertisseur GIF")
racine.protocol("WM_DELETE_WINDOW", a_la_fermeture)

cadre_principal = ttk.Frame(racine)
cadre_principal.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

label_cle = ttk.Label(cadre_principal, text="Entrez la clé générée :")
label_cle.grid(row=0, column=0, pady=5)
cle_entree = ttk.Entry(cadre_principal, show="*")
cle_entree.grid(row=0, column=1, pady=5)

bouton_verifier_cle = ttk.Button(cadre_principal, text="Vérifier la clé", command=montrer_convertisseur)
bouton_verifier_cle.grid(row=1, columnspan=2, pady=5)

fenetre_convertisseur = tk.Toplevel(racine)
fenetre_convertisseur.title("Convertisseur GIF")
fenetre_convertisseur.protocol("WM_DELETE_WINDOW", a_la_fermeture_convertisseur)

cadre_convertisseur = ttk.Frame(fenetre_convertisseur)
cadre_convertisseur.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

label_choix_fichier = ttk.Label(cadre_convertisseur, text="Choisir un fichier GIF :")
label_choix_fichier.grid(row=0, column=0, pady=(0, 5))
champ_entree = ttk.Entry(cadre_convertisseur, width=50)
champ_entree.grid(row=0, column=1, padx=(0, 5), pady=(0, 5), sticky="ew")
bouton_choisir_fichier = ttk.Button(cadre_convertisseur, text="Parcourir...", command=choisir_fichier)
bouton_choisir_fichier.grid(row=0, column=2, padx=(0, 0), pady=(0, 5), sticky="ew")

label_choix_dossier = ttk.Label(cadre_convertisseur, text="Dossier de sortie :")
label_choix_dossier.grid(row=1, column=0, pady=(0, 5))
champ_sortie = ttk.Entry(cadre_convertisseur, width=50)
champ_sortie.grid(row=1, column=1, padx=(0, 5), pady=(0, 5), sticky="ew")
bouton_choisir_dossier = ttk.Button(cadre_convertisseur, text="Parcourir...", command=choisir_dossier)
bouton_choisir_dossier.grid(row=1, column=2, padx=(0, 0), pady=(0, 5), sticky="ew")

variable = tk.IntVar()
variable.set(1)
png_radio = ttk.Radiobutton(cadre_convertisseur, text="Convertir en PNG", variable=variable, value=1)
png_radio.grid(row=2, column=0, columnspan=3, pady=(0, 5), sticky="w")

jpeg_radio = ttk.Radiobutton(cadre_convertisseur, text="Convertir en JPEG", variable=variable, value=2)
jpeg_radio.grid(row=3, column=0, columnspan=3, pady=(0, 5), sticky="w")

bouton_convertir = ttk.Button(cadre_convertisseur, text="Convertir", command=convertir)
bouton_convertir.grid(row=4, column=0, columnspan=3, pady=(0, 5), sticky="ew")

bouton_quitter = ttk.Button(cadre_convertisseur, text="Quitter", command=a_la_fermeture_convertisseur)
bouton_quitter.grid(row=5, column=2, pady=(0, 5), sticky="e")

fenetre_convertisseur.withdraw()

for i in range(3):
    cadre_principal.columnconfigure(i, weight=1)
    cadre_convertisseur.columnconfigure(i, weight=1)

racine.mainloop()
