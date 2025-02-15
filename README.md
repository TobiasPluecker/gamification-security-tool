# gamification-security-tool

Dieses Repository enthält das lokale Tool zur Bewertung eines Gamification-Systems in einer Studie. Das Tool benötigt Zugriff auf eine API und eine Website, um zu funktionieren. Ohne diese Komponenten liefert es keine aussagekräftigen Ergebnisse. Teilnehmer werden es während der Bewertung installieren und verwenden.

## Installation & Setup

Um das Tool für die Studie zu verwenden, folgen Sie diesen Schritten:

### 1. Repository klonen
```sh
git clone https://github.com/your-username/gamification-security-tool.git
cd gamification-security-tool
pip install -e .
```

### 2. Pre-Commit-Hook konfigurieren
Erstellen Sie in dem Repository, in dem Sie das Tool verwenden möchten, eine `.pre-commit-config.yml` mit folgendem Inhalt:
```yaml
repos:
  - repo: local
    hooks:
      - id: local-tool
        name: Pre-Commit Sicherheitscheck
        entry: local_tool
        language: system
        verbose: true
```

### 3. Umgebungsvariablen setzen
Öffnen Sie ein Terminal und führen Sie die folgenden Befehle aus:
```sh
set PYTHONPATH=C:\Path\to\your\gamification-security-tool\installation
set PYTHONIOENCODING=utf-8
```

Erstellen Sie eine `.env`-Datei im Verzeichnis `Local_Tool` und setzen Sie die Variablen, die in der `.env.dist` erwähnt sind.

### 4. Fragen
Fragen Sie nach, wenn Sie einen Parameter nicht kennen.