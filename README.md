> # Deprecated
> Seit dem QIS Update im Sommer 2023 ist die Parserimplementierung nicht mehr nutzbar und bedarf einer Anpassung.
> Da für mich und in meinem Umfeld kein Bedarf mehr an der Fortführung des Projekts besteht, wird dieses Repository derzeit nicht weiter betreut.
> 
> Feel free 2 fork 🍴

# HISinOne QIS - Parser für Prüfungsleistungen

Basiert auf dem Repository: [https://github.com/MrKrisKrisu/HISinOne-QIS-exam-notification](https://github.com/MrKrisKrisu/HISinOne-QIS-exam-notification)

Dieses Script wurde auf die HISinOne Instanz der **Hochschule Fulda** (horstl) angepasst und wird vermutlich für keine andere Hochschule funktionieren.

## Was ist das?
Ein Python Script, das sich für dich in iCMS (horstl) einloggt und schaut, ob sich Änderungen (zum Beispiel eine neue eingetragene Note) in der Prüfungsübersicht bei dir ergeben haben.

Falls gewünscht benachrichtigt dich das Script dann direkt per Telegram oder E-Mail.

Optional können alle Noten als JSON Datenstruktur oder nur die Änderungen als Text auf der Konsole ausgegeben werden.

Es ist also dafür gedacht, beispielsweise alle 30 Minuten ausgeführt zu werden.
 
> Tut dem Hochschulserver einen Gefallen und fragt **nicht** alle 10 Sekunden ab!
 
## Installationsanleitung
### Telegram einrichten
#### Telegram Bot erstellen
Erstelle über den [BotFather](https://t.me/botfather) einen neuen Bot und schreibe dir den Token heraus.
Mehr Informationen zum Erstellen von Telegram Bots: [https://core.telegram.org/bots](https://core.telegram.org/bots)

#### Eigene Telegram ID herausfinden
* Erstelle eine neue Gruppe und füge den [TelegramRawBot](https://t.me/RawDataBot) (RawDataBot) als Mitglied hinzu
* Schreibe nun eine Nachricht in die Gruppe, der RawDataBot wird dir antworten, falls er nicht schon eine Nachricht geschickt hat
* Schreibe dir deine ID heraus, die in der Nachricht unter **message -> from -> id** steht (nicht die mit dem Minus!)
* Deine ID muss später in der Script Konfigurationsdatei als `telegramChatId` hinzugefügt werden

### Python Umgebung
Die Module requests und lxml sind standardmäßig nicht installiert. Diese können mit pip nachinstalliert werden:
> pip install -r requirements.txt

Alternativ kann auch das gebaute Release für Linux verwendet werden

### Script installieren
- Lade das Script in deine Python Umgebung (zum Ausführen der bereits gebauten Version nicht notwendig)
- Lass dir mit `python3 crawl.py --config myHisConfig.cfg` oder `./crawl --config myHisConfig.cfg` eine Konfigurationsdatei erstellen (der Pfad zur Datei kann geändert werden, muss aber schreibbar sein)
- Die Konfigurationsdatei nun manuell anpassen
    - Nutzername und Passwort benötigt (iCMS Zugangsdaten)
    - gerne auch schon mit Telegram oder Mail Support (optional)
- Wenn du das Script jetzt erneut ausführst, solltest du einmalig über **alle** eingetragenen Prüfungen benachrichtigt werden.

### Automatisches ausführen
Du kannst dein Script automatisch regelmäßig ausführen lassen (dafür ist es ja auch gedacht). Das kannst du mit einem CronJob realisieren. Erstelle einfach folgenden CronJob und ersetze das Fragezeichen (?) durch eine beliebige Anzahl an Stunden, nach welchen das Script wiederholt ausgeführt werden soll:

> 0 */? * * * python3 /path/to/crawl.py -c /path/to/myHisConfig.cfg

oder

> 30 */? * * * /path/to/crawl -c /path/to/myHisConfig.cfg

Dies führt dein Script automatisch alle ? Stunden zur Minute 30 aus. Den Wert kannst du anpassen, aber denk dabei bitte an die armen, armen Hochschulserver! Um das ganze noch mehr einzuschränken, kann man die Ausführung auf die prüfungsrelevanten Monate begrenzen:

> 0 */? * 1,2,6,7 * python3 /path/to/crawl.py -c /path/to/myHisConfig.cfg

oder

> 30 */? * 1,2,6,7 * /path/to/crawl -c /path/to/myHisConfig.cfg

Um eine gute Performance der Abfragen zu erreichen, die Hochschulserver zu schonen und keine ungewollte DDoS Attacke zu starten, lohnt es sich die Cronjobs anzupassen und eine eigene Minuten/Stundenzahl zu wählen. Wenn es dir reicht, kannst du das Script ja auch nur 1x am Tag zu einem beliebigen Zeitpunkt ausführen lassen.

Optional kannst du dir ja auch ein Desktop Icon erstellen und das Script manuell ausführen, falls du dir nur den manuellen horstl Login sparen möchtest.

Informationen dazu, wie Cronjobs richtig konfiguriert werden können, gibt es z.B. hier: https://www.stetic.com/developer/cronjob-linux-tutorial-und-crontab-syntax/
## Sicherheitshinweis
Du musst dein zentrales Passwort für deinen Hochschulaccount im **Klartext** in der Konfigurationsdatei speichern. Achte daher bitte darauf, dass das Script nur in einer gesicherten Umgebung läuft und durch geeignete Berechtigungen von dem Zugriff Dritter geschützt ist.

## Ausführbare Datei bauen
Um eine größtmögliche Kompatibilität zu anderen Systemen (bzw. zu dessen glibc Version) herstellen zu können, empfiehlt es sich in einem Docker Container zu bauen.

Bauen der ausführbaren Datei in einem Docker Container kann durch Aufruf von `linux_build_env/build.sh` angestoßen werden.
Das Resultat liegt danach im Pfad `dist/crawl`.

Optional kann die Installation der Abhängigkeiten und Bauen der ausführbaren Datei durch Aufruf von `linux_build_env/package.sh` angestoßen werden.
Beachte, dass dabei die Abhängigkeiten direkt durch deinen Benutzer in deinem System installiert werden. Python muss bereits vorhanden sein

## Starten mit Docker
> Todo: irgendwas im Container ist eventuell kaputt gegangen

### Eigenen Container bauen (optional)
`docker build -t his-in-one_qis_exam-notification .`

### Container nutzen
Die Anwendung steht auch als Docker Container zur Verfügung. Dieser wird von DockerHub heruntergeladen und kann z.B. über die Kommandozeile genutzt werden.

Der Standardpfad `/home/$USER/HISinOne-docker-config` zum Speichern der Konfiguration auf dem Host kann natürlich geändert werden.

```bash
# Erstelle einen Ordner für die Konfiguration des Scripts im Docker Container
mkdir /home/$USER/HISinOne-docker-config

# Lasse die Beispielkonfiguration automatisch in dem Ordner erstellen, falls noch nicht vorhanden
docker run --rm -v /home/$USER/HISinOne-docker-config:/data binsky/his-in-one_qis_exam-notification:latest

# Starte den Container im Hintergrund für regelmäßige Checks
docker run --rm -d -v /home/$USER/HISinOne-docker-config:/data --name my_his-in-one_exam-notifications binsky/his-in-one_qis_exam-notification:latest
```

Nach dem ersten Ausführen des Containers werden im Ordner `/home/$USER/HISinOne-docker-config` die Dateien `crontab` und `myHisConfig.cfg` hinterlegt.

Der Container führt das Script für die Prüfungsleistungen im Standard alle 2 Stunden zu einer zufälligen (festgelegten) Minute aus.
Das Intervall ist in der Datei `/home/$USER/HISinOne-docker-config/crontab` festgelegt.

Die Konfigurationsdatei `/home/$USER/HISinOne-docker-config/myHisConfig.cfg` sollte vor dem Start des Containers im Hintergrund (mit -d) wie oben beschrieben angepasst und getestet werden.
Dafür kann der Befehl `docker run --rm -v /home/$USER/HISinOne-docker-config:/data binsky/his-in-one_qis_exam-notification:latest` verwendet und mit STRG-C abgebrochen werden.

Es ist empfehlenswert den Container zusammen mit dem `watchtower` Image auszuführen, sodass man so immer den aktuellen Stand hat und das Image des Containers automatisch aktualisiert wird.
Sollte das Script im Zuge von Veränderungen am iCMS (horstl) angepasst werden müssen, kann die Aktualisierung so automatisch geladen werden.
