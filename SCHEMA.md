# Wiki Schema — Ideologiekritik-Vault

## Domain
Ideologiekritik, Diskursanalyse, linke Theorie, Corporate PowerWatch, Neurodiversität-Erkenntnisse, Konflikt-Briefings, gesellschaftliche Machtstrukturen

## Conventions
- File names: lowercase, hyphens, no spaces
- Every page starts with YAML frontmatter
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound per page)
- On update: bump `updated` date
- Every new page → `index.md` under correct section
- Every action → `log.md`
- **Provenance markers:** `^[Quellenmappen/quellenmappe_YYYY-MM-DD.md]` bei Absätzen aus spezifischer Quelle

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | briefing | reflexion
tags: [from taxonomy below]
sources: [Quellenmappen/quellenmappe_YYYY-MM-DD.md]
confidence: high | medium | low
contested: true
contradictions: [other-page]
---
```

## Tag Taxonomy
- **Theorie:** ideologiekritik, diskursanalyse, macht, hegemonie, reifikation, funktionale-intransparenz, herrschaft, kapitalismuskritik, biopolitik
- **Akteure:** corporate, staat, lobbyismus, billionaire, regulatorisch, arbeit
- **Phänomene:** schwurbel, ideologie, propaganda, gaslighting, normalisierung, othering
- **Methoden:** dekonstruktion, immanent-kritik, genealogie, diskursarchäologie
- **Neurodiversität:** adhd, neurodivergenz, erfahrungserlebnis, masking, rsd
- **Formate:** quellenmappe, briefing, radar, reflexion, theorie-spur

## Page Thresholds
- **Create** when entity appears in 2+ sources OR is central to one
- **Add to existing** when source mentions something already covered
- **DON'T create** for passing mentions
- **Split** when page exceeds ~200 lines
