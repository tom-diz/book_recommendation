# Importation de librairies/modules nécessaires au fonctionnement du programme
import os
from numpy import dot
from numpy.linalg import norm

# Crée la matrice de recommandation de livres, en fonction des utilisateurs qui ont déjà renseigné leur avis sur des livres
def matrice():
    with open('booksread.txt', 'r') as file:
        contenu = file.readlines()
        readers_size = len(contenu)
    with open('books.txt', 'r') as file:
        contenu = file.readlines()
        books_size = len(contenu)
    notation = [[0 for _ in range(books_size)] for _ in range(readers_size)]
    notation_w_names = {}
    data = gather_notes()
    user = 0
    for i in data:
        pseudo = i[0]
        book_data = i[1:]
        k = 0
        for j in book_data[0]:
            notation[user][j-1] = book_data[1][k]
            k = k + 1
        notation_w_names[pseudo] = notation[user]
        user = user + 1
    return notation_w_names

# Calcule la similarité cosinus entre le lecteur actuel et les autres et affiche les livres qui lui sont recommandés (non-lus)
def calc_recommandation(data, pseudo):
    other_ratings = {}
    for i in data.keys():
        if i != pseudo:
            other_ratings[i] = data[i]
    own_ratings = {pseudo: data[pseudo]}

    calculated_ratings = []
    max = 0
    max_name = ""
    for nom in other_ratings:
        calc = dot(own_ratings[pseudo], other_ratings[nom])/(norm(own_ratings[pseudo])*norm(other_ratings[nom]))
        if calc >= max and calc != 1:
            max = calc
            max_name = nom

    origin_ratings = data[pseudo]
    target_ratings = data[max_name]
    index = 0
    books_recommend_index = []
    for i in target_ratings:
        if i > 0:
            books_recommend_index.append(index)
        index = index + 1
    
    file = open("books.txt", "r")
    contenu = file.readlines()
    i = 0
    livre_recommandé = False
    for ligne in contenu:
        if i in books_recommend_index:
            if origin_ratings[i] == 0:
                print("-", ligne, end="")
                livre_recommandé = True
        i = i + 1
    if livre_recommandé == False:
        print("Aucun autre utilisateur n'a lu de livres, ou vous les avez déjà lus.")
    file.close()


# Récupère les notes du fichier "booksread.txt"
def gather_notes():
    with open("booksread.txt", "r") as file:
        data = []
        lignes = file.readlines()
        for temp1 in lignes:
            lecteur = ""
            livres = []
            notes = []
            temp2 = temp1.split(",")
            lecteur = temp2[0]
            temp2 = temp2[1:]
            for i in temp2:
                i = i.replace("\n", "")
                temp3 = i.split(":")
                livres.append(int(temp3[0]))
                notes.append(int(temp3[1]))
            data.append([lecteur, livres, notes])
        return data

# Première étape du programme - Permet de créer son compte ou se connecter
def menu_login(name=""):
    print("Bienvenue au programme de recommandation de livres !\n\n1 - Se connecter à un compte\n2 - S'inscrire\n3 - Quitter le programme\n")
    id = check_int(3)
    if id == 1:
        pseudo = login()
        menu(pseudo)
    elif id == 2:
        ajouter_lecteur()
    else:
        clear()
        print("Merci d'avoir utilisé le programme de recommandation de livres. A bientôt ! :)\n")
        exit()

# Menu de connexion - Permet à l'utilisateur d'accéder à ses services
def login():
    clear()
    print("Quel est votre pseudonyme?")
    pseudo = check_only_letters()
    with open('readers.txt') as file:
        lecteurs = []
        content = file.readlines()
        for i in content:
            lecteurs.append(i.split(",")[0])
        if pseudo in lecteurs:
            clear()
            return pseudo
        else:
            print("Ce pseudo n'existe pas.")
            menu_login()

# Menu Principal - Permet d'exécuter des actions en fonction du choix de l'utilisateur
def menu(pseudo):
    remove_empty_lines("books")
    remove_empty_lines("booksread")
    remove_empty_lines("readers")
    print("\nMENU PRINCIPAL - Veuillez faire un choix:\n1. Profils des lecteurs\n2. Visiter le dépôt des livres\n3. Recommandation de livres\n4. Déconnexion")
    select = check_int(4)
    select_list = {1: menu_profil,
                    2: menu_depot,
                    3: menu_recommandation,
                    4: menu_login}
    clear()
    select_list[select](pseudo)

# Menu du profil des lecteurs
def menu_profil(pseudo):
    clear()
    print("PROFIL DES LECTEURS - Veuillez choisir une option.\n1 - Afficher un lecteur\n2 - Ajouter un lecteur\n3 - Supprimer un lecteur\n4 - Modifier un lecteur")
    select = check_int(4)
    select_list = {1: afficher_lecteur,
                    2: ajouter_lecteur,
                    3: supprimer_lecteur,
                    4: modifier_lecteur}
    select_list[select](pseudo)

# Menu du dépôt
def menu_depot(pseudo):
    clear()
    print("DEPOT DES LIVRES - Veuillez choisir une option.\n1 - Afficher les livres (+ renseigner les livres lus)\n2 - Ajouter un livre\n3 - Modifier un livre\n4 - Supprimer un livre")
    select = check_int(4)
    select_list = {1: [afficher_livres, renseigner_livres],
                    2: ajouter_livre,
                    3: modifier_livre,
                    4: supprimer_livre}
    if isinstance(select_list[select], list):
        for i in select_list[select]:
            i(pseudo)
    else:
        select_list[select](pseudo)

# Menu de recommandation - Permet d'afficher des livres recommandés en comparant l'avis des autres utilisateurs
def menu_recommandation(pseudo):
    clear()
    print("MENU DE RECOMMANDATION\n\nBienvenue sur le système de recommandation. Voici les livres qui vous sont recommandés:")
    data = matrice()
    if pseudo in data:
        calc_recommandation(data, pseudo)
    else:
        print("Vous n'avez pas lu de livres. Vous ne pouvez donc pas vous faire recommander des livres.")
    print("\n-------------------------------------------------------\n")
    menu(pseudo)



# MANAGEMENT DES UTILISATEURS
# Ajouter un lecteur - Permet de stocker un nouvel utilisateur dans les fichiers
def ajouter_lecteur(pseudo=""):
    new_pseudo = ""
    with open("readers.txt", "r") as file:
        lines = file.readlines()
        names = []
        for i in lines:
            names.append(i.split(",")[0])

    print("PAGE DE CONNEXION\n")
    while True:
        print("\nQuel est votre pseudonyme ?")
        new_pseudo = check_only_letters()

        if new_pseudo not in names:
            if new_pseudo != "":
                break
            else:
                clear()
                print("Un nom ne peut pas être vide.")
        else:
            clear()
            print("Ce lecteur existe déjà.")

    clear()
    age = 0
    while age <= 0 or age >= 130:
        print("Quel est votre age ?")
        age = check_int(100)
    if age >= 0 or age <= 18:
        age = 1
    elif age < 25:
        age = 2
    else:
        age = 3
    clear()
    print("Voici les styles de lectures proposées :")
    style_livres = ["Sciencefiction", "Biographie", "Horreur", "Romance", "Fable", "Histoire", "Comédie"]
    while True:
        for item in style_livres:
            print(item)
        try:
            print("Quel est votre de style de lecture parmis ceux proposé dans la listes ci-dessus ?")
            style = str(style_livres.index(str(input())) + 1)
            break
        except:
            clear()
            print("Vous devez saisir un style correct.")
    clear()
    liste_genre = ["Homme", "Femme", "Peu importe"]
    while True:
        for item in liste_genre:
            print(item)
        try:
            print("Quel est votre genre selon la liste précédente?")
            genre = str(liste_genre.index(str(input())) + 1)
            break
        except:
            clear()
            print("Genre incorrect")
    
    f = open("readers.txt", "a")
    f.write("\n" + new_pseudo + "," + genre + "," + str(age) + "," + style)
    f.close()
    if pseudo == "":
        menu_login()
    else:
        menu(pseudo)

# Afficher un lecteur - Permet d'afficher des informations liés à un certain utilisateur
def afficher_lecteur(pseudo):
    # RECUPERATION DES LECTEURS
    file = open("readers.txt", "r")
    contenu = file.readlines()
    i = 0
    name_show = ""
    for ligne in contenu:
        ligne = ligne.split(",")
        name_show = ligne[0]
        i += 1
        print(i, "-", name_show, end="\n")
    file.close()

    # SELECTION D'UN LECTEUR
    id = check_int(i)
    items = contenu[id-1].split(",")
    name = items[0]

    # AFFICHAGE DES INFOS DE BASE
    liste_genre = ["Homme", "Femme", "Peu importe"]
    genre = int(items[1])
    genre = liste_genre[genre-1]

    age = int(items[2])
    if age <= 18:
        age = "<= 18 ans"
    elif (age > 18) and (age < 25):
        age = "18-24 ans"
    else:
        age = "> 25 ans"

    style_livres = ["Sciencefiction", "Biographie", "Horreur", "Romance", "Fable", "Histoire", "Comédie"]
    style = int(items[3])
    style = style_livres[style-1]

    # RECUPERATION DES LIVRES LUS
    file = open("booksread.txt", "r")
    contenu = file.readlines()
    i = 0
    livres = []

    for ligne in contenu:
        if name in ligne:
            ligne = ligne.split(",")
            name = ligne[0]
            livres = ligne[1:]

    print("\nLecteur: {}\n- Genre: {}\n- Age: {}\n- Style: {}".format(name, genre, age, style))

    books = []
    file = open("books.txt", "r")
    lines = file.readlines()
    for i in livres:
        i = i.split(":")[0]
        if lines[int(i)-1].endswith("\n"):
            lines[int(i)-1] = lines[int(i)-1][:-1]
        books.append(lines[int(i)-1])
    file.close()

    print("\nLivres lus:")
    if books == []:
        print("Ce lecteur n'a lu aucun livre.")
    else:
        for i in books:
            print("-", i)
    menu(pseudo)

# A FAIRE - Supprimer un lecteur - Permet de supprimer un utilisateur des bases de données
def supprimer_lecteur(pseudo):
    with open("readers.txt", "r") as file:
        contenu = file.readlines()
        i = 0
        names = []
        for ligne in contenu:
            ligne = ligne.split(",")
            ligne = ligne[0]
            names.append(ligne)
            i += 1
            print(i, "-", ligne, end="\n")
        print("Quel lecteur voulez-vous supprimer? (Taper le numéro)")
        line = check_int(i)
    del_pseudo = names[line - 1]
    with open("readers.txt", "w") as file:
        del contenu[line - 1]
        file.writelines(contenu)
    
    with open("booksread.txt", "r") as file:
        contenu = file.readlines()
        index = 0
        for i in contenu:
            if "{},".format(del_pseudo) in i:
                del contenu[index]
                break
            index = index + 1

    with open("booksread.txt", "w") as file:
        file.writelines(contenu)
    
    clear()
    print("Le lecteur sélectionné a bien été supprimé.")
    menu(pseudo)

# Modifier un utilisateur - Permet de modifier le nom d'un utilisateur
def modifier_lecteur(pseudo):
    clear()

    with open("readers.txt", "r") as file:
        lines = file.readlines()
        names = []
        for i in lines:
            names.append(i.split(",")[0])
    
    new_pseudo = ""
    while True:
        print("Veuillez saisir un nouveau pseudo pour votre compte.\n")
        new_pseudo = check_only_letters()
        if new_pseudo not in names:
            if new_pseudo != "":
                break
            else:
                clear()
                print("Un nom ne peut pas être vide.")
        else:
            clear()
            print("Ce lecteur existe déjà.")

    # MODIF FICHIER READERS
    file = open("readers.txt", "r")
    contenu = file.readlines()
    lines = []
    for i in contenu:
        if "{},".format(pseudo) in i:
            lines.append(i.replace(pseudo, new_pseudo))
        else:
            lines.append(i)
    file.close()
    with open('readers.txt', 'w') as file:
        file.writelines(lines)
    
    # MODIF FICHIER BOOKSREAD
    file = open("booksread.txt", "r")
    contenu = file.readlines()
    lines = []
    for i in contenu:
        if "{},".format(pseudo) in i:
            lines.append(i.replace(pseudo, new_pseudo))
            break
        else:
            lines.append(i)
    file.close()
    with open('booksread.txt', 'w') as file:
        file.writelines(lines)
    
    print("Votre pseudo a été modifié.")
    menu(new_pseudo)

# MANAGEMENT DES LIVRES
# Afficher les livres - Permet d'afficher à l'utilisateur les livres actuellement disponibles en bibliothèque
def afficher_livres(pseudo):
    clear()
    print("Les livres disponibles sont :")
    file = open("books.txt", "r")
    contenu = file.readlines()
    i = 0
    for ligne in contenu:
        i+=1
        print(i, "-", ligne, end="")
    file.close()

# Ajouter un livre - Permet d'ajouter un livre dans la bibliothèque
def ajouter_livre(pseudo):
    while True:
        print("Quel livre voulez-vous ajouter?")
        livre = check_only_letters()
        file = open("books.txt", "r")
        lines = file.readlines()
        lines2 = []
        for i in lines:
            lines2.append(i.replace("\n", ""))
        file.close()
        if livre in lines2:
            print("Ce livre existe déjà.")
        else:
            clear()
            print("Le livre", livre ,"a été ajouté à la bibliothèque.")
            file = open("books.txt", "a")
            file.write("\n{}".format(livre))
            file.close()
            menu(pseudo)
            break

# Modifier un livre - Permet de modifier le nom d'un livre
def modifier_livre(pseudo):
    livres = []
    file = open("books.txt", "r")
    contenu = file.readlines()
    i = 0
    for ligne in contenu:
        livres.append(ligne.replace("\n", ""))
        i += 1
        print(i, "-", ligne, end="")
    print("\nQuel livre voulez-vous modifier? (Taper le numéro)")
    line = check_int(i)
    titre = contenu[line - 1]
    file.close()

    while True:
        print("Vous avez sélectionné: {}\nQuel nom voulez-vous?".format(titre))
        nom = check_only_letters()

        if nom not in livres:
            if nom != "":
                break
            else:
                clear()
                print("Un nom ne peut pas être vide.")
        else:
            clear()
            print("Ce livre existe déjà.")

    file = open("books.txt", "w")
    contenu[line-1] = "{}\n".format(nom)
    file.writelines(contenu)
    file.close()
    
    clear()
    print("Le nom de ce livre a bien été modifié.")
    menu(pseudo)

# Supprimer un livre - Permet d'enlever un livre de la bibliothèque
def supprimer_livre(pseudo):
    file = open("books.txt", "r")
    contenu = file.readlines()
    i = 0
    for ligne in contenu:
        i += 1
        print(i, "-", ligne, end="")
    print("\nQuel livre voulez-vous supprimer? (Taper le numéro)")
    line = check_int(i)
    file.close()
    file = open("books.txt", "w")
    name_deleted_book = contenu[line - 1]
    del contenu[line - 1]
    file.writelines(contenu)
    file.close()

    # Modification du fichier "booksread.txt" en fonction de l'index du livre (réécriture de fichier)
    index = line
    new_data = []
    with open("booksread.txt", "r") as file:
        lines = file.readlines()
        for i in lines:
            new_user = []
            name = i.split(",")[0]
            new_user.append(name)
            i = i.split(",")[1:]
            for j in i:
                j = j.split(":")
                # Inférieur à l'index: l'ajouter dans la liste "new_user"
                if int(j[0]) < index:
                    new_user.append("{}:{}".format(j[0],j[1]))
                # Supérieur à l'index: réduction de l'index du livre de 1 (pour concorder avec celle de la liste de livres)
                elif int(j[0]) > index:
                    new_user.append("{}:{}".format(int(j[0])-1,j[1]))
                # Egal à l'index: ne pas l'ajouter dans la liste "new_user", donc ne rien faire
            new_user = ",".join(new_user)
            new_data.append(new_user)
    with open("booksread.txt", "w") as file:
        file.writelines(new_data)
    print("Le livre {} a bien été supprimé du dépôt.".format(name_deleted_book.replace("\n", "")))
    menu(pseudo)

# Renseigner des livres - Permet à l'utilisateur de renseigner les livres qu'il a lu
def renseigner_livres(pseudo):
    choice = ""
    while True:
        if choice != "OUI":
            if choice != "NON":
                print("\nVoulez-vous renseigner et noter les livres que vous avez lu? (OUI/NON)")
            else:
                menu(pseudo)
                break
        else:
            break
        
        choice = input()
    if choice == "OUI":
        livres_already_chosen = []
        livres_formatted = "{},".format(pseudo)
        while True:
            # Vérifie le nombre de livres et les affiche
            file = open("books.txt", "r")
            contenu = file.readlines()
            i = 0
            for ligne in contenu:
                print(i+1, "-", ligne, end="")
                i+=1
            
            print("\nVeuillez saisir l'ID d'un livre que vous avez lu. Tapez 0 pour terminer.\n")
            int_input = check_int0(i)
            if int_input == 0:
                break
            elif int_input in livres_already_chosen:
                print("Vous avez déjà noté ce livre.")
            else:
                print("Quelle est la note que vous voulez attribuer à ce livre?")
                note = check_int(5)
                livres_formatted = livres_formatted + "{}:{},".format(int_input, note)
                livres_already_chosen.append(int_input)
            
        # Vérifie si la ligne de l'utilisateur existe dans le fichier "booksread.txt"
        livres_formatted = livres_formatted[:-1]
        line_number = 0
        with open("booksread.txt", "r") as file:
            contenu = file.readlines()
            i = 1
            for line in contenu:
                if pseudo in line:
                    line_number = i
                    break
                i = i + 1
        if line_number != 0:
            add_line("booksread.txt", line_number, contenu, livres_formatted)
        else:
            create_line("booksread.txt", livres_formatted)
        print("Votre liste de livres lus a bien été mis à jour.")
        menu(pseudo)


# FONCTIONS SECONDAIRES
# Ajoute une ligne et écrit du contenu dans un certain fichier
def add_line(a, line, contenu, content):
    with open(a, "w") as file:
        contenu[line-1] = content + "\n"
        file.writelines(contenu)

# Sert à écrire du contenu dans un fichier "a"
def create_line(a, content):
    with open(a, "a") as file:
        file.write("\n{}".format(content))

# Vérifie si une entrée est un nombre entier supérieur à 0. Dans le cas contraire, le programme va répéter cette action.
def check_int(max_value):
    while True:
        try:
            select = input("-> Veuillez taper le chiffre correspondant.")
            select = int(select)
            if select <= max_value and select >= 1:
                return int(select)
        except:
            print("Vous devez taper un chiffre correspondant entre 1 et {}.".format(max_value))

# Vérifie si une entrée est un nombre entier égal à 0. Dans le cas contraire, le programme va répéter cette action.
def check_int0(max_value):
    while True:
        try:
            select = input("-> Veuillez taper le chiffre correspondant.")
            select = int(select)
            if select <= max_value and select >= 0:
                return int(select)
        except:
            print("Vous devez taper un chiffre correspondant entre 0 et {}.".format(max_value))

# Permet de "nettoyer" la console
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# String To List - Permet de convertir les données composées de virgule en listes. (Utile dans le cas de récupération de données)
def string_to_list(string, a, r):
    file = open(a, r)
    contenu = file.readlines()
    i = 0
    name_show = ""
    content = []
    for ligne in contenu:
        content.append(ligne.split(","))
    file.close()
    return content

# Vérifie si une chaîne de caractère ne contient pas de caractères spéciaux
def check_only_letters():
    while True:
        text = input()
        if all(x.isalpha() or x.isspace() for x in text):
            return text
        else:
            print("Veuillez taper une chaîne de caractère valide (lettres & espaces seulement).")

# Supprime les lignes vides dans certains fichiers, pouvant rendre problématique l'utilisation du programme
def remove_empty_lines(fichier):
    with open('{}.txt'.format(fichier), 'r') as file:
        string_e_lignes = ""
        contenu = file.read()
        lignes = contenu.split("\n")
        n_empty_lignes = [ligne for ligne in lignes if ligne.strip() != ""]
        for ligne in n_empty_lignes:
            string_e_lignes += ligne + "\n"
    with open('{}.txt'.format(fichier), 'w') as file:
        file.write(string_e_lignes)