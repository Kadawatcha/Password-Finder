import tkinter as tk           # L'affichage (Interface Graphique)
import multiprocessing         # Les muscles (Plusieurs cœurs en parallèle)
import itertools               # Logique : génération de combinaisons "à la volée"
import string                  # Alphabet, chiffres et symboles
import time                    # Pour le chronomètre et le calcul de vitesse
import threading               # Pour que l'interface ne freeze pas pendant le calcul
import ctypes                  # Pour faire clignoter la barre des tâches 
# autres (pour anotations de types)
from multiprocessing.synchronize import Event as EventType
from multiprocessing.sharedctypes import Synchronized


"""
TABLEAU DE COMPLEXITÉ 
Basé sur un alphabet de 95 caractères (Lettres + Chiffres + Symboles + Espace)
Formule : 95 ^ Longueur

L = 1 : 95 combinaisons ........... (Instantané)
L = 2 : 9 025 combinaisons ........ (Instantané)
L = 3 : 857 375 combinaisons ...... (< 1 seconde)
L = 4 : 81 450 625 combinaisons ... (Quelques secondes)
L = 5 : ~7,7 Milliards ............ (Plusieurs minutes)
L = 6 : ~735 Milliards ............ (Plusieurs heures / jours)

Gain Multiprocessing : Temps total / Nombre de cœurs actifs
"""

def initialiser_travailleur(compteur_init, stop_event_init):
    """ Initialise les variables partagées pour chaque processus travailleur au démarrage """
    global compteur_partage
    global stop_event
    compteur_partage = compteur_init
    stop_event = stop_event_init

def travailleur_crack(args):
    """ Moteur de calcul exécuté par chaque cœur séparément """
    premier_char, mdp_cible, longueur_max = args
    caracteres = string.ascii_letters + string.digits + string.punctuation + " "
    
    local_count = 0 # Compteur interne au cœur pour limiter les échanges mémoire
    
    # On définit les références locales une seule fois pour la performance
    stop_event_local: EventType = stop_event
    compteur_partage_local: Synchronized = compteur_partage

    # Test du premier caractère seul
    if premier_char == mdp_cible:
        return premier_char

    # Boucle sur les longueurs de mots
    for longueur in range(2, longueur_max + 1):
        for suite in itertools.product(caracteres, repeat=longueur - 1):
            # 1. VERIFICATION DU STOP : Si l'utilisateur clique sur STOP, on quitte
            if stop_event_local.is_set():
                return None

            local_count += 1
            mot_teste = premier_char + "".join(suite)
            
            # 2. MISE À JOUR DU COMPTEUR : On ne met à jour la mémoire partagée
            # que tous les 10 000 essais pour ne pas ralentir le processeur.
            if local_count % 10_000 == 0:
                with compteur_partage_local.get_lock():
                    compteur_partage_local.value += 10_000

            # 3. VERIFICATION DU MOT DE PASSE
            if mot_teste == mdp_cible:
                return mot_teste
                
    return None


    
   

def stop_attaque():
    """ Déclenchée par le bouton STOP pour arrêter les cœurs """
    if 'event_stop_global' in globals():
        event_stop_global.set()
    label_resultat.config(text="🛑 Attaque interrompue !", fg="orange")

def lancer_recherche_multicoeur():
    """ Gère la distribution du travail et les statistiques en temps réel """
    global event_stop_global
    
    mdp_a_crack = entree_mdp.get()
    if not mdp_a_crack: return # Sécurité si vide
    
    longueur_max = len(mdp_a_crack) # Ta fameuse "triche" sur la longueur
    caracteres_possibles = string.ascii_letters + string.digits + string.punctuation + " "
    
    # --- OUTILS PARTAGÉS ---
    # 'q' = long long (pour compter des milliards), Value = mémoire commune
    compteur = multiprocessing.Value('q', 0)
    event_stop_global = multiprocessing.Event()
    event_stop_global.clear()
    
    # Préparation des tâches (une par lettre de l'alphabet)
    taches = [(char, mdp_a_crack, longueur_max) for char in caracteres_possibles]
    
    temps_debut = time.time()
    
    # Utilisation de 6 cœurs (8 processeurs logiques - 2 de sécurité)
    nb_coeurs = max(1, multiprocessing.cpu_count() - 2)
    
    with multiprocessing.Pool(processes=nb_coeurs, initializer=initialiser_travailleur, initargs=(compteur, event_stop_global)) as pool:
        # Lancement asynchrone pour garder la main sur le chronomètre
        resultat_async = pool.imap_unordered(travailleur_crack, taches)
        
        while True:
            # 1. CALCUL DE LA VITESSE
            temps_ecoule = time.time() - temps_debut
            total_essais = compteur.value
            vitesse = total_essais / temps_ecoule if temps_ecoule > 0 else 0
            
            # 2. MISE À JOUR VISUELLE (Stats)
            # On affiche la vitesse brute, convertie en entier, avec des virgules/espaces pour les milliers
            stats_txt = f"Essais : {total_essais:,}\nVitesse : {int(vitesse):,} Mots/sec"
            fenetre.after(0, lambda t=stats_txt: label_stats.config(text=t))
            
            # 3. RÉCUPÉRATION DU RÉSULTAT (si un cœur a fini)
            try:
                res = resultat_async.next(timeout=0.1) # On attend 100ms
                if res:
                    msg_final = f"✅ Trouvé : {res}\n⏱️ {temps_ecoule:.2f}s | {total_essais:,} essais"
                    print(msg_final)
                    fenetre.after(0, lambda: label_resultat.config(text=msg_final, fg="red"))
                    pool.terminate()
                    break
            except (multiprocessing.TimeoutError, StopIteration):
                pass
            
            # 4. ARRÊT MANUEL
            if event_stop_global.is_set():
                pool.terminate()
                break

def demarrer_thread():
    """ Lance le moteur dans un thread pour ne pas figer la fenêtre """
    label_resultat.config(text="🔥 Analyse en cours...", fg="black")
    t = threading.Thread(target=lancer_recherche_multicoeur, daemon=True)
    t.start()
    
def basculer_visibilite():
    """ Alterne entre l'affichage masqué (*) et l'affichage en clair de notre mdp"""
    if entree_mdp.cget('show') == '*':
        entree_mdp.config(show='') # Affiche le texte
        bouton_oeil.config(text="👁️") # Oeil ouvert
    else:
        entree_mdp.config(show='*') # Masque le texte
        bouton_oeil.config(text="🔒") # Cadenas fermé

# --- INTERFACE GRAPHIQUE ---
if __name__ == '__main__':
    print("Démarage en cours...")
    nb_coeurs = max(1, multiprocessing.cpu_count() - 2)
    print(f"Nombre de processeurs logiques utilisés : {nb_coeurs} / {multiprocessing.cpu_count()}")
        
    fenetre = tk.Tk()
    fenetre.title("Cyber-Dashboard Multi-Cœurs")
    fenetre.resizable(False, False) # pas bouger oh !
    fenetre.geometry("450x350")

    # Titre et Champ de saisie
    tk.Label(fenetre, text="Simulateur de crackage de MDP", font=("Arial", 16, "bold")).pack(pady=10)
    # On crée un cadre pour grouper l'entrée et l'œil sur la même ligne
    cadre_saisie = tk.Frame(fenetre)
    cadre_saisie.pack(pady=10)

    # Le champ de saisie (maintenant dans cadre_saisie)
    entree_mdp = tk.Entry(cadre_saisie, show="*", font=("Arial", 14), justify="center", width=15)
    entree_mdp.pack(side="left")

    # Le petit bouton "œil" juste à côté
    bouton_oeil = tk.Button(cadre_saisie, text="🔒", font=("Arial", 10), 
                            command=basculer_visibilite, relief="flat")
    bouton_oeil.pack(side="left", padx=5)

    # Boutons de contrôle
    cadre_boutons = tk.Frame(fenetre)
    cadre_boutons.pack(pady=10)
    
    tk.Button(cadre_boutons, text="🚀 LANCER", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), 
              command=demarrer_thread, width=12).pack(side="left", padx=10)
    
    tk.Button(cadre_boutons, text="🛑 STOP", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), 
              command=stop_attaque, width=12).pack(side="left", padx=10)
    
    label_mdp_infos = tk.Label(fenetre, text="Caractéristiques du mdp choisi : Longueur = 0",
                               font="Arial", justify="center")
    label_mdp_infos.pack(pady=10)

    # Mise à jour dynamique de la longueur à chaque frappe clavier
    entree_mdp.bind("<KeyRelease>", lambda event: label_mdp_infos.config(
        text=f"Caractéristiques du mdp choisi : Longueur = {len(entree_mdp.get())}"))


    # Zone de statistiques (Vitesse et Compteur)
    label_stats = tk.Label(fenetre, text="Vitesse : 0.00 Mots/sec\nEssais : 0", 
                          font=("Consolas", 11), fg="#2980b9", justify="center")
    label_stats.pack(pady=15)

    # Zone de résultat final
    label_resultat = tk.Label(fenetre, text="En attente...", font=("Arial", 12))
    label_resultat.pack(pady=20)

    fenetre.mainloop()