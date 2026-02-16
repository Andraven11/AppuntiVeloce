# Appunti Veloce

Applicazione per salvare appunti veloci su database SQLite locale, con best practice di sicurezza.

## Requisiti
- Python 3.8+

## Installazione
Nessuna dipendenza esterna. Clona e usa:

```bash
cd AppuntiVeloce
python main.py help
```

## Comandi

| Comando | Descrizione |
|---------|-------------|
| `add <testo>` | Aggiungi un appunto |
| `list` | Elenca tutti gli appunti |
| `show <id>` | Mostra un appunto |
| `edit <id> <testo>` | Modifica un appunto |
| `delete <id>` | Elimina un appunto |
| `path` | Mostra path database (per backup) |

## Sicurezza
- Query parametrizzate (anti SQL injection)
- PRAGMA sicuri: WAL, synchronous=FULL, foreign_keys
- Extension loading disabilitato
- Validazione e limite lunghezza input (max 10000 caratteri)
- Database in `%LOCALAPPDATA%\AppuntiVeloce\` (Windows) o `~/.local/share/AppuntiVeloce/` (Linux)

## Backup
Il database è un singolo file. Per fare backup:
```bash
python main.py path   # mostra il path
# Copia il file appunti.db
```

## Documentazione
- `PLAN.md` - Piano della funzionalità
- `DECISIONS.md` - Decisioni architetturali (ADR)
