from flask import Flask, request, render_template_string        
from waitress import serve                             
                                                                                                 
app = Flask(__name__)                                                                        
                                                                                                 
# Le code HTML de notre fausse page de connexion                                             
PAGE_HTML = """                                                                              
    <!DOCTYPE html>                                                                              
    <html>                                                                                       
    <head>                                                                                       
        <title>Test Serveur</title>                                                              
    </head>                                                                                      
    <body>                                                                                       
        <h2>Page de test</h2>                                                                    
        <!-- Le formulaire envoie les données à l'URL /api/login via la méthode POST -->         
        <form action="/login" method="POST">                                                 
            <label for="user">Utilisateur:</label><br>                                           
            <input type="text" id="user" name="username"><br><br>                                
                                                                                                 
            <label for="pass">Mot de passe:</label><br>                                          
            <input type="password" id="pass" name="password"><br><br>                            
                                                                                                 
            <input type="submit" value="Envoyer">                                                
        </form>                                                                                  
    </body>                                                                                      
    </html>                                                                                      
    """                                                                                          
                                                                                                 
# Route 1 : Affiche la page web quand on va sur http://127.0.0.1:5000/                       
@app.route('/')                                                                              
def accueil():                                                                               
    return render_template_string(PAGE_HTML)                                                 
                                                                                                 
    # Route 2 : C'est ici que les données POST arrivent !                                        
@app.route('/login', methods=['POST'])                                                   
def traitement_login():                                                                      
    # request.form permet de récupérer les données envoyées par le formulaire HTML           
    # ou par votre script Python 'requests' !                                                
    nom_utilisateur = request.form.get('username')                                           
    mot_de_passe = request.form.get('password')                                              
                                                                                                 
    print(f"📡 [SERVEUR] Tentative de connexion reçue : {nom_utilisateur} / {mot_de_passe}") 
                                                                                                 
    # Petite logique de test                                                                 
    if nom_utilisateur == "admin" and mot_de_passe == "secret":                              
        return "Connexion réussie !", 200                                                    
    else:                                                                                    
        # On renvoie un code 401 (Unauthorized) si c'est faux                                
        return "Identifiants incorrects.", 401                                               
          
          
          
# Seule diff avec serv_lent (import)                                                                                 
if __name__ == '__main__':                                                                   
    print("🚀 Serveur de PRODUCTION démarré sur http://127.0.0.1:9000")                                    
    serve(app, host='127.0.0.1', port=9000, threads=100) # On lui donne 100 threads d'action !