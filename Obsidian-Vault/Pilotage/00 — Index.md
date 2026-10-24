---
type: index
tags: [pilotage, index]
date: 2026-10-23
statut: actif
---

# Pilotage — le poste de commande

Trois couches, **une seule source de vérité**.

| Couche | Fichier | Rôle |
|---|---|---|
| Source | ce dossier (`Pilotage/`) | tu écris ici |
| Vue | `/home/jhpy/dashboard.html` | généré, lecture seule |
| Rappel | Telegram, 7h30 lun–ven | généré, 7 lignes |

> [Ouvrir le dashboard](file:///home/jhpy/dashboard.html) — l'onglet **Progression** montre les 30 leçons et les 8 sections Play Store.

## Les 5 écrans

- **Aujourd'hui** — la seule prochaine action, la leçon du jour, le streak, le journal
- **Progression** — 30 leçons cochées, groupées par semaine + les 8 sections Play Store
- **Cycle** — 1 objectif, 3 jalons, 9 actions, 8 preuves, l'avancement Play Store
- **Projets** — les actifs, les gelés, les archivés
- **Preuves** — ce qui existe et qu'on peut montrer

## Les 3 rituels

1. **Chaque soir (1 h)** : une action, un commit, une ligne de journal.
2. **Dimanche (30 min)** : revue, une preuve publiée, la semaine suivante.
3. **Fin de cycle (6 semaines)** : démo, rétro, cycle suivant.

## Les règles

- **Un seul objectif par cycle.** Le reste est gelé, pas « en pause ».
- Le cap est dans [[Objectifs]] : chaque cycle sert **un** des trois objectifs.
- Une action ne compte que si elle produit un commit, un fichier ou un lien.
- Une semaine sans preuve est une semaine ratée, même avec des commits.
- On ne rouvre un projet gelé qu'à la fin du cycle.
- Les 5 marches OS et les 7 niveaux mobiles sont une **carte**, pas une todo : [[Carte — OS & Mobile]].

## Les commandes

```bash
python3 ~/.hermes/scripts/pilotage.py            # régénère le dashboard
python3 ~/.hermes/scripts/pilotage.py --brief    # le briefing 7 lignes
python3 ~/.hermes/scripts/pilotage.py --check    # vérifie les notes
python3 ~/.hermes/scripts/pilotage.py --log "Orane.d | fait : … | bloqué : … | demain : …"
python3 ~/.hermes/scripts/pilotage.py --done 3       # coche la leçon 3 + régénère
python3 ~/.hermes/scripts/pilotage.py --undone 3     # décoche la leçon 3
```

## Les notes

- [[Objectifs]]
- [[Parcours — App mobile]]
- [[Checklist — Play Store]]
- [[Cycle 1 — Orane.d]]
- [[Projets]]
- [[Journal]]
- [[Preuves]]
- [[Revue hebdo]]
- [[Carte — OS & Mobile]]

## Ce qui a changé le 23 octobre 2026

- 10 dépôts morts archivés sur GitHub (réversible).
- 2 PR fermées sur `start-up` (branches conservées).
- Orane.d devient l'objectif du cycle 1. Scribe est gelé.
- nand2tetris passe à 1 soir/semaine. NIA reste 1 h/semaine.
- L'ancien dashboard à 6 onglets et 125 étapes est remplacé par ces 5 écrans.
- La progression des 30 leçons se coche dans [[Parcours — App mobile]] (`## Ma progression`) et s'affiche dans l'onglet **Progression**.
