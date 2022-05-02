# OC_P12
### *Epic_Events_CRM*

---


# 1. Description du programme
Application de gestion de relation client d'Epic Events

---


# 2. Créer l'environnement virtuel puis l'activer
#### Windows :
* Créer l'environnement virtuel avec la commande du terminal suivante : "python -m venv env".
* Activer l'environnement virutel depuis le terminal grâce à la commande suivante : "env/scripts/activate".
#### Unix :
* Créer l'environnement virtuel avec la commande du terminal suivante : "virtutalenv -p env venv".
* Activer l'environnement virutel depuis le terminal grâce à la commande suivante : "source env/bin/activate".

---


# 3. Installation les dépendances
Afin d'installer automatiquement tous les dépendences nécessaires au projet, dans le terminal, utilisez la commande suivante :
#### Windows :
" *pip install -r requirements.txt* "
#### Unix :
" *python3 -m pip install -r requirments.txt* "

---


# 4. Installer et Initialiser le git
* Si vous n'avez pas encore git, utilisez la commande suivante :
#### Windows :
" *pip install git* "
#### Unix :
" *python3 -m pip install git* "
Ou veuillez cliquer sur le lien suivant : [Installer git](https://git-scm.com/downloads) et suivez les instructions du site.
* Initialiser ensuite le git avec la commande suivante dans votre console (assurez-vous que vous vous situez bien dans le dossier qui va contenir votre projet avant de lancer la commande): " *git init* " (Fonctionne pour Windows et Unix).

---


# 5. Importer le projet depuis github
Veuillez taper la commande suivante dans votre console : " *git clone https://github.com/GuillaumeP29/OC_P12.git* ".

---


# 6. se rendre dans le dossier src
Veuillez taper la commande suivante dans votre console : " *cd src* ".

---


# 7. Installer PostgreSQL
Rendez-vous sur le lien suivant :[Installer PostgresSQL](https://www.postgresql.org/download/windows/) et suivez les instructions.

---


# 8. Créer la base de donnée
Ouvrez le shell psql ("SQL Shell (psql)"), connectez-vous avec votre profil postgresql et tapez la commande suivante :
" *CREATE DATABASE Epic_Event;* ".

---


# 9. Créer le superuser
Dans la console de votre IDE du projet, veuillez taper la commande suivante :
#### Windows :
" *python manage.py createsuperuser* "
#### Unix :
" *python3 manage.py createsuperuser* "

Suivez ensuite les instructions en renseignant les données suivantes :
Username: " *admin* "
Mot de passe : " *EpicEvent2022* "
Vous pouvez entrez d'autres données, mais il faudra également les modifier dans le dictionnaire DATABASES de settings.py

---


# 9. Charger les fixtures pour la base de donnée
Lancer la commande suivante :
#### Windows :
" *python manage.py loaddata core/fixtures/initial_data.yaml* "
#### Unix :
" *python3 manage.py loaddata core/fixtures/initial_data.yaml* "

**!!! Les permissions générées automatiquement par django peuvent avoir un id différent d'un projet à l'autre, ce qui causera des problèmes lors de l'attribution des permissions aux différents groupes. Dans le fichier fixtures/initial_data.yaml, les permissions souaitées risquent de ne plus correspondre à celles accordées. Il est possible et récitifer ça dans l'interface administrateur en sélectionnant les différents groupes et vérifiant que les permissions correspondent aux commentaires du fichier de fixture !!!**

---


# 10. Lancer le serveur
Lancer la commande suivante :
#### Windows :
" *python manage.py runserver* "
#### Unix :
" *python3 manage.py runserver* "

---