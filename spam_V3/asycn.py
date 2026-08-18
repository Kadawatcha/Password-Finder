'''VERSION ASYNCHRONE : ENVOI REQUETES EN MASSE ET ATTENDS LA REPONSE
Pour les commentaires spécifiques a des variables "de base" voir /spam_V3/sync.py
'''
 
import httpx     
from requests import Response # biblio synchrone oui mais utilisée uniquement pour le type 


async def send_request():
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
        if statut == 200:                                                                            
            print("✅ Succès ! Mot de passe et user correct") 
        elif statut == 404:                                                                          
            print("❌ Erreur 404 : La page n'a pas été trouvée.")                                    
        elif statut == 401 or statut == 403:                                                         
            print("🔒 Accès refusé (Non autorisé).")                                                 
        else:                                                                                        
            print(f"⚠️ Autre code reçu : {statut}")   
                                                                         
                                                                                                 
