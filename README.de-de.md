# LunaGC-7.0.0 WIP

[繁體中文 (Traditional Chinese)](README.md)

## Hinweis vom Maintainer
Könnte gelegentlich auf die neueste Version aktualisiert werden, hängt von meiner Stimmung und Situation ab. Natürlich veröffentliche ich die Protocol-Buffer-Definitionen auf [GitLab](https://gitlab.com/kitkat-multiverse/genshin-protocol).

## Aktualisierte Version von Grasscutters mit einigen neu implementierten Funktionen.
Altes LunaGC Discord https://discord.gg/7D5gkyJR5Y (bitte fragen Sie dort nicht nach Unterstützung, da es von anderen Personen übernommen wurde, erstellen Sie stattdessen ein Problem in diesem Repository)

Die Funktionen und Funktionalität des PS sind nicht garantiert, probieren Sie es selbst aus und sehen Sie, was funktioniert und was nicht.

Tragen Sie bei, wenn Sie möchten/können...

# Lesen Sie das [Handbuch](handbook.md)!

# Installationsanleitung
- Lesen Sie die folgende Anleitung, sie ist gerade ausreichend, um den Server und den Client zum Laufen zu bringen.

## Hauptanforderungen

- Holen Sie sich [Java 17](https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html)
- Holen Sie sich [MongoDB Community Server](https://www.mongodb.com/try/download/community)
- Holen Sie sich [NodeJS](https://nodejs.org/dist/v20.15.0/node-v20.15.0-x64.msi) (für die Handbucherstellung)
- Holen Sie sich die Spielversion REL7.0.0
- Stellen Sie sicher, dass Sie Java installiert haben und die Umgebungsvariablen festgelegt haben.
- Erstellen Sie den Server (siehe "Eigentlichen Server kompilieren" in dieser Anleitung.)
- Laden Sie die [Ressourcen](https://github.com/fjyczcr/LunaGC-Resources) herunter, erstellen Sie einen neuen Ordner namens `resources` im heruntergeladenen LunaGC-Ordner und extrahieren Sie die Ressourcen in diesen neuen Ordner.
- Setzen Sie useEncryption, Questing und useInRouting auf false (sollte standardmäßig false sein, ändern Sie es, wenn nicht)
- [Patchen Sie das Spiel](#spiel-patchen)
- Starten Sie den Server und das Spiel. Stellen Sie sicher, dass Sie auch ein Konto in der LunaGC-Konsole erstellen!
- Viel Spaß (oder nicht)

### Spiel patchen
- Kopieren Sie `patch/Astrolabe.dll` in den Spielordner unter `GenshinImpact_Data/Plugins`. Sichern Sie zuvor die alte `Astrolabe.dll` im Plugins-Ordner.
- Falls Sie es selbst erstellen möchten, klonen Sie [hk4e-patch-universal](https://github.com/fjyczcr/hk4e-patch-universal), installieren Sie [**Rust**](https://rust-lang.org/learn/get-started/) und **Cargo** (wird mit rustup geliefert), führen Sie `cargo build --release` aus und benennen Sie die DLL in `target/release` in `Astrolabe.dll` um.

### Erste Schritte

- Klonen Sie das Repository (installieren Sie zuerst [Git](https://git-scm.com))

  ```
  git clone --recurse-submodules https://github.com/fjyczcr/LunaGC.git
  ```

- Jetzt können Sie mit den folgenden Schritten fortfahren.


### Eigentlichen Server kompilieren

**Anforderungen**:

[Java Development Kit 17 | JDK](https://oracle.com/java/technologies/javase/jdk17-archive-downloads.html) oder höher

- **Hinweis**: Die Handbucherstellung kann auf einigen Systemen fehlschlagen. Um die Handbucherstellung zu deaktivieren, fügen Sie `-PskipHandbook=1` zum Befehl `gradlew jar` hinzu.

- **Für Windows**:

  ```shell
  .\gradlew.bat
  .\gradlew.bat jar
  ```

- **Für Linux**:

  ```bash
  chmod +x gradlew
  ./gradlew
  ./gradlew jar
  ```

### Die Ausgabe-JAR befindet sich im Projektstammverzeichnis.

### Handbuch manuell kompilieren

```shell
./gradlew generateHandbook
```

## Fehlerbehebung

- Stellen Sie sicher, dass Sie useEncryption und useInRouting beide auf false setzen, sonst können Fehler auftreten.
- Um Windy zu verwenden, stellen Sie sicher, dass Sie Ihre Luac-Dateien in C:\Windy ablegen (erstellen Sie den Ordner, falls er nicht vorhanden ist)
- Wenn Sie einen Fehler im Zusammenhang mit einem MongoDB-Verbindungs-Timeout erhalten, überprüfen Sie, ob der MongoDB-Dienst läuft. Unter Windows: Drücken Sie die Windows-Taste und R, geben Sie dann `services.msc` ein, suchen Sie nach dem MongoDB-Server und falls er nicht gestartet ist, starten Sie ihn, indem Sie mit der rechten Maustaste darauf klicken und Start auswählen. Unter Linux können Sie `systemctl status mongod` verwenden, um zu überprüfen, ob er läuft. Falls nicht, geben Sie `systemctl start mongod` ein. Wenn Sie jedoch unter Linux den Fehler 14 erhalten, ändern Sie den Besitzer des MongoDB-Ordners und der .sock-Datei (`sudo chown -R mongodb:mongodb /var/lib/mongodb` und `sudo chown mongodb:mongodb /tmp/mongodb-27017.sock`) und versuchen Sie dann erneut, den Dienst zu starten.

## Gutschrift

Proto-Repository [hk4e-protos](https://gitlab.com/kitkat-multiverse/genshin-protocol)

Patch-Repository [hk4e-patch-universal](https://github.com/kitkat033/hk4e-patch-universal)
