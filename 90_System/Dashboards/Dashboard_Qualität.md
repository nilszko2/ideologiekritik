---
typ: dashboard
---

# Dashboard: Vault-Qualität

## Alle Zettel nach Feld

```dataview
TABLE typ, status, erstellt
FROM "01_Zettel"
WHERE typ
SORT erstellt DESC
```

## Zettel im Entwurfsstatus

```dataview
TABLE typ, tags
FROM "01_Zettel"
WHERE contains(tags, "status/entwurf")
SORT file.name ASC
```

## Filmanalysen

```dataview
TABLE film_titel, film_jahr, regie
FROM "01_Zettel"
WHERE typ = "analyse"
SORT film_jahr DESC
```

## Alle Exegese-Blöcke

```dataview
TABLE werk, kapitel, datum
FROM "04_Projekte"
WHERE typ = "exegese"
SORT datum DESC
```

## Literaturnotizen

```dataview
TABLE typ, status, erstellt
FROM "02_Literatur"
SORT erstellt DESC
```

## Letzte 20 bearbeitete Dateien

```dataview
TABLE file.mtime AS "Geändert", typ
FROM ""
WHERE typ
SORT file.mtime DESC
LIMIT 20
```
