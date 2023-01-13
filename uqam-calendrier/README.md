# Uqam-Calendrier

Cet outil permet d'exporter plus facilement le calendrier des horaires de cours affiché sur le site de l'UQAM vers un calendrier compatible avec Google Calendar, Apple Calendar, Outlook, etc.


### Prérequis

- Python 3.6+
- Selenium
- ChromeDriver
- dateparser
- Un compte étudiant à l'UQAM
    - Vous devrez fournir votre **code permanent** et votre **mot de passe** pour accéder à votre calendrier

### Utilisation

1. Téléchargez le fichier `uqam-calendrier.py` et placez-le dans un dossier vide.
2. Lancez un terminal et placez-vous dans le dossier où vous avez placé le fichier `uqam-calendrier.py`.
3. Exécutez la commande `pip install -r requirements.txt` pour installer les dépendances.
4. Exécutez la commande `python uqam-calendrier.py` et suivez les instructions à l'écran.
5. Le fichier `uqam-calendrier.ics` sera créé dans le dossier où vous avez placé le fichier `uqam-calendrier.py`.
6. Importez le fichier `uqam-calendrier.ics` dans votre calendrier préféré.

## Import de fichiers .ics

### Google Calendar

1. Dans Google Calendar, cliquez sur settings.
2. Cliquez sur "Import & Export".
3. Choisir "Import from file".
4. Sélectionnez le fichier `uqam-calendrier.ics` et cliquez sur "Import".


### Apple Calendar

1. Ouvrez iCal. et cliquez sur "File" puis "Import".
2. Sélectionnez le fichier `uqam-calendrier.ics` et cliquez sur "Import".
3. Sélectionnez "Import all events" et cliquez sur "Import".

### Outlook

1. Dans Outlook, cliquez sur "File" puis "Open & Export".
2. Cliquez sur "Import/Export".
3. Sélectionnez "Import an iCalendar (.ics) or vCalendar (.vcs) file" et cliquez sur "Next".
4. Sélectionnez le fichier `uqam-calendrier.ics` et cliquez sur "Next".
5. Sélectionnez "Import all items" et cliquez sur "Finish".


### Autres calendriers

Consultez la documentation de votre calendrier pour savoir comment importer un fichier .ics.
