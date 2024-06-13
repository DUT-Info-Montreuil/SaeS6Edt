from ldap3 import Server, Connection, ALL, SUBTREE
import json

class LdapService:

    SERVER_IP = "ldap1.iut.univ-paris8.fr"
    SERVER_PORT = 389
    BASE_DN = 'ou=personnel,ou=utilisateurs,o=iut.univ-paris8.fr'

    @staticmethod
    def to_dict(dn_str):
        paires = dn_str.split(',')
        dictionnaire = {}
        for paire in paires:
            cle, valeur = paire.split('=')
            dictionnaire[cle] = valeur
        return dictionnaire

    @staticmethod
    def get_ldap_login(username):
        return f"uid={username},ou=info,ou=etudiants,ou=enseignement,ou=utilisateurs,o=iut.univ-paris8.fr"

    @staticmethod
    def get_connection(username, password):
        server = Server(LdapService.SERVER_IP, port=LdapService.SERVER_PORT, get_info=ALL)
        try:
            conn = Connection(server, user=LdapService.get_ldap_login(username), password=password, authentication='SIMPLE', raise_exceptions=False)
            if conn.bind():
                print(f"User {username} authenticated successfully.")
                return conn
            else:
                print(f"Failed to authenticate user {username}.")
                return None
        except Exception as e:
            print(f"LDAP authentication error for user {username}: {e}")
            return None

    @staticmethod
    def get_user_role(username, password):   
        conn = LdapService.get_connection(username, password)
        if conn:
            search_filter = "(objectClass=*)"
            search_attributes = ['givenName', 'sn']
            try:
                if not conn.search(search_base=LdapService.BASE_DN, search_filter=search_filter, search_scope=SUBTREE, attributes=search_attributes):
                    print("Search operation failed")
                    print(conn.result)
                    return None
                
                print("Récupération des utilisateurs: RÉUSSI")
                users = []
                for entry in conn.entries:
                    print(entry)
                    user = json.loads(entry.entry_to_json())
                    if user["dn"]:
                        dn_dict = LdapService.to_dict(user["dn"])
                        if 'uid' in dn_dict:
                            login = dn_dict['uid']
                            prenom = user['attributes']['givenName'][0] if 'givenName' in user['attributes'] else ''
                            nom = user['attributes']['sn'][0] if 'sn' in user['attributes'] else ''
                            users.append({'uid': login, 'prenom': prenom, 'nom': nom})
                            print(f"uid: {login}, nom: {nom}, prenom: {prenom}")
                conn.unbind()
                return users
            except Exception as e:
                print("Recherche dans le serveur: ÉCHOUÉ")
                print(e)
                return None
        else:
            print("Connexion échouée")
            return None
        
    @staticmethod
    def get_user(username, password):   
        conn = LdapService.get_connection(username, password)
        if conn:
            search_filter = f"(uid={username})"
            search_attributes = ['givenName', 'sn']
            try:
                if not conn.search(search_base=LdapService.BASE_DN, search_filter=search_filter, search_scope=SUBTREE, attributes=search_attributes):
                    print("Search operation failed")
                    print(conn.result)
                    return None
                print("Récupération de l'utilisateur courant: RÉUSSI")
                user = {}
                if conn.entries:
                    entry = conn.entries[0]
                    user_data = json.loads(entry.entry_to_json())
                    dn_dict = LdapService.to_dict(user_data["dn"])
                    if 'uid' in dn_dict:
                        login = dn_dict['uid']
                        prenom = user_data['attributes']['givenName'][0] if 'givenName' in user_data['attributes'] else ''
                        nom = user_data['attributes']['sn'][0] if 'sn' in user_data['attributes'] else ''
                        user = {'uid': login, 'prenom': prenom, 'nom': nom}
                        print(f"uid: {login}, nom: {nom}, prenom: {prenom}")
                conn.unbind()
                return user
            except Exception as e:
                print("Recherche dans le serveur: ÉCHOUÉ")
                print(e)
                return None
        else:
            print("Connexion échouée")
            return None
