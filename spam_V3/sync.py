'''VERSION SYNCHRONE : "LENTE" : ENVOIE REQUETE / ATTENDS REPONSE '''

import requests                                                                              
                                                                                                 
# 1. L'URL cible (l'endroit où les données sont envoyées)                   
url = "http://127.0.0.1:8000/login" # Exemple d'URL de votre serveur local      
# Cela doit etre l'url POST qui sera enevoyée quand on appuiera sur le bouton     
# Inspecter la page et trouver : <form action="/cette_url"> au niveau du bouton                                                             
                                                                                                 
# 2. Les données à envoyer (sous forme de dictionnaire Python)                               
# Les clés ('username', 'password') doivent correspondre à ce que le serveur attend          
donnees = {                                                                                  
        "username": "fake_user",                                                    
        "password": "123456"                                                           
    }                          

# Les clés username/password se ditue dans le champ "name" du fichier html    
# dans les "<input>"  (champs de texte)                                                           
                                                                                                 
# (Optionnel) 3. Les en-têtes (Headers)                                                      
# Parfois, le serveur a besoin de savoir quel type de données il reçoit                      
'''headers = {                                                                                  
    "Content-Type": "application/x-www-form-urlencoded" # ou "application/json" selon l'API  
    }'''           
    
'''Besoin d'en-tetes ? : vérifier -> 

  1. Ouvrez le site web que vous voulez cibler dans Chrome ou Firefox.                           
  2. Appuyez sur F12 pour ouvrir les outils de développement.                                    
  3. Allez dans l'onglet Réseau (ou Network).                                                    
  4. Faites l'action que vous voulez simuler en Python (par exemple, remplissez le formulaire de 
  connexion et cliquez sur valider).                                                             
  5. Vous allez voir une ligne apparaître dans la liste des requêtes (souvent avec la méthode    
  POST). Cliquez dessus.                                                                         
  6. Cherchez la section En-têtes de requête (ou Request Headers).                               
                                                                                                 
                                                         
                                                        
'''                                                                                 
while True:
    try:                                                                                         
        # 4. L'envoi de la requête POST                                                          
        reponse = requests.post(url, data=donnees) # headers=headers si besoin                              
        statut = reponse.status_code                                                                           
        # 5. Analyser la réponse du serveur                                                      
        print(f"Code de statut : {statut}")    
        # 3. On peut utiliser ce statut dans des conditions                                          
        if statut == 200:                                                                            
            print("✅ Succès ! La requête a bien fonctionné.")                                       
        elif statut == 404:                                                                          
            print("❌ Erreur 404 : La page n'a pas été trouvée.")                                    
        elif statut == 401 or statut == 403:                                                         
            print("🔒 Accès refusé (Non autorisé).")                                                 
        else:                                                                                        
            print(f"⚠️ Autre code reçu : {statut}")                                         
                                                                                                 
    # Si le serveur répond en JSON (ce qui est très courant aujourd'hui)                     
        try:                                                                                     
            print("Réponse JSON :", reponse.json())                                              
        except:                                                                                  
        # Sinon on affiche le texte brut                                                     
            print("Réponse Texte :", reponse.text)                                               
                                                                                                 
    except requests.exceptions.RequestException as e:                                            
        print(f"Une erreur de connexion est survenue : {e}")                                     
                                                                                                 
                                 