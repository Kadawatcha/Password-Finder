'''VERSION ASYNCHRONE : ENVOI REQUETES EN MASSE ET ATTENDS LA REPONSE
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
        reponse = await client.post(url, data=donnees ) # headers=headers 
        statut = reponse.status_code                                                
        return statut
                                                                         
async def main():
    print('🚀 Démarrage du script...')
    
    # FIX: Initialisation des variables AVANT la boucle
    compteur_animation = 0
    tentatives = 0
    
    while True:
        try:
            # Gestion de l'animation
            symbole = CHARGEMENT[compteur_animation % len(CHARGEMENT)]
            tentatives += 1
        
            sys.stdout.write(f"\r{symbole} Recherche en cours... Tentative n°{tentatives}")
            sys.stdout.flush()
            compteur_animation += 1
            
            # Requetes TODO appeller la fonction de recherche dynamique nom utilisateur / mdp
            # Au lieu de variables de bases statiques que nous ne sommes pas censés connaitres
            username = 'admin'
            password = 'secret'
            
            statut = await send_request(username=username, password=password)
            
            # Pause pour ne pas saturer la machine
            await asyncio.sleep(0.1) 
            
            # Analyse des statuts
            if statut == 200:      
                sys.stdout.write("\r" + " " * 50 + "\r")                                                                      
                print(f"✅ tentatives : {tentatives}")
                print(f"👤 Login : {username}")
                print(f"🔑 MDP   : {password}")
                break
              
            elif statut == 404: 
                sys.stdout.write("\r" + " " * 50 + "\r")
                print('❌ 404')                                                                         
                break                  
                
            elif statut == 401:                                                   
                pass # C'est un mauvais mot de passe, l'animation continue au prochain tour          
                
            elif statut == 403:
                sys.stdout.write("\r" + " " * 50 + "\r")
                print('🔒 Erreur 403 : Accès interdit (IP bloquée ou pare-feu)')
                break                                      
                
            else:                                                                                        
                sys.stdout.write("\r" + " " * 50 + "\r")
                print(f"⚠️ Autre code reçu : {statut}")   
                await asyncio.sleep(2) # Pause plus longue en cas d'anomalie
                          
        except Exception as e:
            sys.stdout.write("\r" + " " * 50 + "\r")
            print(f"Erreur réseau détectée : {e}")
            # Pause plus longue en cas d'erreur
            await asyncio.sleep(10)

asyncio.run(main()) 