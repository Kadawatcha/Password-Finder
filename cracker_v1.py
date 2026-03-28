import tkinter as tk
import string 
import itertools
import time 

def crack_password():
    mdp_a_crack = entree_mdp.get()
    time_start= time.time()
    essais = 0 
    
    # Ajout des majuscules, de la ponctuation et des espaces
    caracteres = string.ascii_letters + string.digits 
    """
    Pour des questions de rapidités on néglige :
    + string.punctuation | a ajouter si on veut accepter la ponctuation
    + " "  | a ajouter si on veut accepter les espaces
    """
    
    # On limite la recherche à 10 caractères max (11 non inclus)
    for i in range(1, 11):
        for tests in itertools.product(caracteres, repeat=i): # product : boucles de boucles
            essais += 1   
            mot_genere = "".join(tests)
            
            # time.time() : secondes actuels
                       
            # underscore pour lisibilité 
            if essais % 100_000 == 0:  # % : modulo reste de la division euclidienne = 0 ( uniquement 10k 20k...)
                try:
                    temps_ecoule = time.time() - time_start                                                                             # .4f : chiffres apès ,
                    label_resultat.config(text=f"Recherche en cours...\nEssais : {essais:,}\nTest actuel : {mot_genere}\nTemps écoulé : {temps_ecoule} s")
                    fenetre.update() # Rafraîchit l'interface graphique
                except tk.TclError:
                    return # si on kill la fenetre 

            if mot_genere == mdp_a_crack:
                fin = time.time()
                temps_ecoule = fin - time_start
                label_resultat.config(text=f"Trouvé : {mot_genere}\nEssais : {essais:,}\nTemps : {temps_ecoule:.4f} s")
                return # Mot de passe trouvé avec succès fin de la boucle
    
    # Si on sort des boucles sans avoir fait de "return", c'est qu'on a dépassé les 10 caractères
    label_resultat.config(text=f"Abandon : Limite de 10 caractères dépassée ou mot de passe avec caractères")
    
    
# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Simulateur de crack de mot de passe")
fenetre.geometry("400x250") # Largeur x Hauteur


label_titre = tk.Label(fenetre, 
                       text="Testeur de Mot de Passe", 
                       font=("Arial", 14, "bold"))

label_titre.pack(pady=10)

# Champ de saisie (show="*" masque les caractères)
entree_mdp = tk.Entry(fenetre, show="*", font=("Arial", 12))
entree_mdp.pack(pady=10)

# Bouton de lancement fonction
bouton_lancer = tk.Button(fenetre, text="Lancer l'attaque", font=("Arial", 12), command=crack_password)
bouton_lancer.pack(pady=10)

# Zone d'affichage des résultats
label_resultat = tk.Label(fenetre, text="En attente...", font=("Arial", 12))
label_resultat.pack(pady=20)

# Garde interface ouverte 
fenetre.mainloop()
    
    
    
