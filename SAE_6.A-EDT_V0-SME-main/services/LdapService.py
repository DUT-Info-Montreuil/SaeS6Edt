from ldap3 import Server, Connection, ALL, SUBTREE
import json

class LdapService:

    SERVER_IP = "ldap1.iut.univ-paris8.fr"
    SERVER_PORT = 389
    BASE_DN = 'ou=utilisateurs,o=iut.univ-paris8.fr'

    @staticmethod
    def convert_dn_to_dict(dn_str):
        paires = dn_str.split(',')
        dictionnaire = {}
        for paire in paires:
            cle, valeur = paire.split('=')
            if cle in dictionnaire:
                if isinstance(dictionnaire[cle], list):
                    dictionnaire[cle].append(valeur)
                else:
                    dictionnaire[cle] = [dictionnaire[cle], valeur]
            else:
                dictionnaire[cle] = valeur
        return dictionnaire

    @staticmethod
    def find_user_dn(username):
        server = Server(LdapService.SERVER_IP, port=LdapService.SERVER_PORT, get_info=ALL)
        conn = Connection(server, authentication='ANONYMOUS', raise_exceptions=False)
        if not conn.bind():
            print("Échec de la connexion au serveur LDAP.")
            return None

        search_filter = f"(uid={username})"
        search_base = LdapService.BASE_DN
        search_attributes = ['givenName', 'sn']
        try:
            if not conn.search(search_base=search_base, search_filter=search_filter, search_scope=SUBTREE, attributes=search_attributes):
                print("Échec de l'opération de recherche.")
                return None

            if len(conn.entries) == 0:
                print("Aucun utilisateur trouvé.")
                return None

            user_dn = conn.entries[0].entry_dn
            conn.unbind()
            return user_dn
        except Exception as e:
            print("Erreur lors de la recherche:", e)
            return None
        
    @staticmethod
    def authenticate_user(username, password):
        server = Server(LdapService.SERVER_IP, port=LdapService.SERVER_PORT, get_info=ALL)
        try:
            user_dn = LdapService.find_user_dn(username)
            if user_dn is None:
                print(f"Utilisateur {username} introuvable.")
                return None
            conn = Connection(server, user=user_dn, password=password, authentication='SIMPLE', raise_exceptions=False)
            if conn.bind():
                return conn
            else:
                print(f"Échec de l'authentification pour l'utilisateur {username}.")
                return None
        except Exception as e:
            print(f"Erreur d'authentification LDAP pour l'utilisateur {username} : {e}")
            return None

    @staticmethod
    def get_user_role(username):   
        try:
            user_dn = LdapService.find_user_dn(username)
            if user_dn is None:
                return None
            dn_dict = LdapService.convert_dn_to_dict(user_dn)
            if 'ou' in dn_dict:
                return dn_dict['ou']
            else:
                print("Rôle de l'utilisateur introuvable.")
                return None
        except Exception as e:
            print("Erreur lors de la récupération du rôle de l'utilisateur :", e)
            return None
