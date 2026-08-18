'''VERSION ASYNCHRONE : ENVOI REQUETES EN MASSE ET ATTENDS LA REPONSE
Pour les commentaires spécifiques a des variables "de base" voir /spam_V3/sync.py
'''
 
import httpx     
import asyncio
import sys # pour faire joli dans le terminal
from requests import Response # biblio synchrone oui mais utilisée uniquement pour le type 


CHARGEMENT = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

async def send_request() -> int: # renvoie un entier
    url = "http://127.0.0.1:8000/login"
    donnees = {                                                                                  
        "username": "fake_user",                                                    
        "password": "123456"                                                           
    }
    headers = {                                                                                                             
            "User-Agent": "Mon-Script-Asynchrone-V2",                                                                               
            "Accept": "text/html,application/xhtml+xml"                                                                             
        }     
    
    async with httpx.AsyncClient() as client:
        reponse: Response = await client.post(url, datas=donnees) #hearders=headers
        # Afficher le dictionnaire complet des en-têtes renvoyés par le serveur                                                 
        # print("En-têtes reçus :", reponse.headers)  
        statut = reponse.status_code                                                
        return statut
                                                                         
async def main():
    print('🚀 Démarrage du script...')
    while True:
        try:
            
            symbole = CHARGEMENT[compteur_animation % len(CHARGEMENT)]
            tentatives += 1
        
        #    \r remet le curseur au début de la ligne, end="" évite le saut de ligne
            sys.stdout.write(f"\r{symbole} Recherche en cours... Tentative n°{tentatives}")
            sys.stdout.flush()
            compteur_animation += 1
            
            statut = await send_request()
            await asyncio.sleep(0.1) # eviter de faire planter le pc de la ménagère 
            if statut == 200:      
                sys.stdout.write("\r" + " " * 50 + "\r")                                                                      
                print("✅ Succès ! Mot de passe et user correct") 
                break
            elif statut == 404: 
                print('404')                                                                         
                break                  
            elif statut == 401:                                                   
                pass           
            elif statut == 403:
                print('403 - Interdit')
                break                                      
            else:                                                                                        
                sys.stdout.write("\r" + " " * 50 + "\r")
                print(f"⚠️ Autre code reçu : {statut}")   
                await asyncio.sleep(2) # Pause plus longue en cas d'anomalie
                          
                        
        except Exception as e:
            print(f"Erreur réseau détectée : {e}")
            # Pause plus longue en cas d'erreur
            await asyncio.sleep(10)

asyncio.run(main()) 
