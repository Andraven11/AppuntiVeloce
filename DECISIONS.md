# Decisioni architetturali

## ADR-001: Database locale per appunti veloci

**Data**: 2026-02-16  
**Stato**: Accettato

### Contesto
Necessità di salvare appunti veloci in modo persistente su dispositivo locale.

### Decisione
Utilizzo di **SQLite** come database locale, con le seguenti motivazioni:

1. **Semplicità**: Zero configurazione, incluso in Python standard library
2. **Portabilità**: Singolo file .db, facile backup e migrazione
3. **Affidabilità**: Transazioni ACID, supporto WAL per concorrenza
4. **Performance**: Adeguato per migliaia di record senza overhead

### Alternative considerate
- **JSON file**: Scartato per mancanza di transazioni, rischio corruzione su scritture concorrenti
- **SQLCipher**: Valutato per dati sensibili; non necessario per appunti personali non critici

### Sicurezza implementata (fonti: OWASP, blackhawk.sh, dev.to)
- Query sempre parametrizzate (anti SQL injection)
- PRAGMA: foreign_keys=ON, journal_mode=WAL, synchronous=FULL
- Extension loading disabilitato
- Database in path utente (AppData/Local su Windows)
- Validazione e sanitizzazione input prima dell'inserimento

### Conseguenze
- Nessuna dipendenza esterna oltre a Python stdlib
- Backup = copia file .db
- Possibile migrazione futura a SQLCipher se servisse cifratura
