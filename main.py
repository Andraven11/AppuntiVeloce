#!/usr/bin/env python3
"""
Appunti Veloce - CLI per gestione appunti locali.
Uso: python main.py [comando] [argomenti]
"""

import sys
from appunti import crea, leggi, aggiorna, elimina, get_db_path


def cmd_aggiungi(testo: str) -> None:
    try:
        id_nuovo = crea(testo)
        print(f"✓ Appunto #{id_nuovo} salvato.")
    except ValueError as e:
        print(f"Errore: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_lista() -> None:
    appunti = leggi()
    if not appunti:
        print("Nessun appunto salvato.")
        return
    for a in appunti:
        print(f"\n--- #{a['id']} ---")
        print(a["contenuto"])
        print(f"(creato: {a['creato']}, modificato: {a['modificato']})")


def cmd_mostra(id_appunto: int) -> None:
    appunti = leggi(id_appunto)
    if not appunti:
        print(f"Appunto #{id_appunto} non trovato.")
        sys.exit(1)
    a = appunti[0]
    print(f"--- #{a['id']} ---")
    print(a["contenuto"])
    print(f"Creato: {a['creato']}")
    print(f"Modificato: {a['modificato']}")


def cmd_modifica(id_appunto: int, nuovo_testo: str) -> None:
    try:
        ok = aggiorna(id_appunto, nuovo_testo)
        if ok:
            print(f"✓ Appunto #{id_appunto} aggiornato.")
        else:
            print(f"Appunto #{id_appunto} non trovato.")
            sys.exit(1)
    except ValueError as e:
        print(f"Errore: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_elimina(id_appunto: int) -> None:
    ok = elimina(id_appunto)
    if ok:
        print(f"✓ Appunto #{id_appunto} eliminato.")
    else:
        print(f"Appunto #{id_appunto} non trovato.")
        sys.exit(1)


def stampa_help() -> None:
    print("""
Appunti Veloce - Salva appunti su database locale SQLite

Comandi:
  add <testo>       Aggiungi un nuovo appunto
  list              Elenca tutti gli appunti
  show <id>         Mostra un appunto per id
  edit <id> <testo> Modifica un appunto
  delete <id>       Elimina un appunto
  path              Mostra il path del database (per backup)
  help              Mostra questo messaggio

Esempi:
  python main.py add "Ricordati di chiamare Mario"
  python main.py list
  python main.py show 1
  python main.py edit 1 "Nuovo testo"
  python main.py delete 1
""")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        stampa_help()
        return

    cmd = args[0].lower()

    if cmd == "add":
        if len(args) < 2:
            print("Uso: add <testo>")
            sys.exit(1)
        cmd_aggiungi(" ".join(args[1:]))

    elif cmd == "list":
        cmd_lista()

    elif cmd == "show":
        if len(args) < 2:
            print("Uso: show <id>")
            sys.exit(1)
        try:
            cmd_mostra(int(args[1]))
        except ValueError:
            print("L'id deve essere un numero.")
            sys.exit(1)

    elif cmd == "edit":
        if len(args) < 3:
            print("Uso: edit <id> <nuovo_testo>")
            sys.exit(1)
        try:
            cmd_modifica(int(args[1]), " ".join(args[2:]))
        except ValueError:
            print("L'id deve essere un numero.")
            sys.exit(1)

    elif cmd == "delete":
        if len(args) < 2:
            print("Uso: delete <id>")
            sys.exit(1)
        try:
            cmd_elimina(int(args[1]))
        except ValueError:
            print("L'id deve essere un numero.")
            sys.exit(1)

    elif cmd == "path":
        print(f"Database: {get_db_path()}")

    elif cmd == "help":
        stampa_help()

    else:
        print(f"Comando sconosciuto: {cmd}")
        stampa_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
