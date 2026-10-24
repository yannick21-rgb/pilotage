---
type: carte
---

# Carte — OS & Mobile

Ce n'est **pas une todo-list**. C'est la carte du territoire, pour savoir où on va sur 5 ans.
La todo active est [[Cycle 1 — Orane.d]]. La version détaillée (125 étapes) reste dans [[Plan général — reprise]], en lecture seule.

## Le plan OS — 5 marches

| Marche | Contenu | Durée | Livrable |
|---|---|---|---|
| 1 | Comprendre la machine — nand2tetris 1, C, CSAPP 1–3 | 3–4 mois | machine nand2tetris + programme C |
| 2 | Du matériel au logiciel — nand2tetris 2, assembleur, build | 4–6 mois | assembleur + mini-compilateur + OS nand2tetris |
| 3 | Concepts des OS — OSTEP, xv6, Kerrisk | 4–6 mois | TP xv6 complets |
| 4 | Rust et premier noyau — le livre Rust, QEMU, interruptions | 4–6 mois | noyau qui boote et ordonnance 2 tâches |
| 5 | Un vrai OS — mémoire, processus, syscalls, FS, shell, réseau | 12–24 mois | OS qui boote, exécute des programmes, a un shell |

## Le plan mobile — 7 niveaux

| Niveau | Contenu | Durée | Livrable |
|---|---|---|---|
| 1 | JavaScript et TypeScript en profondeur | 2–3 mois | librairie TS sur npm |
| 2 | React en profondeur | 3–4 mois | Orane.d publié |
| 3 | React Native et Expo avancés | 4–6 mois | une app publiée et maintenue |
| 4 | Kotlin et Swift | 6–9 mois | la même app en RN, Kotlin, Swift |
| 5 | Sous la plateforme — OS, réseau, BDD, compilation | 6–9 mois | backend + client natif |
| 6 | Embarqué et bas niveau — C, Rust, ESP32 | 9–12 mois | objet connecté + app |
| 7 | Ton propre OS | 12–24 mois | OS avec shell et programmes |

## Comment on s'en sert

- Une marche ou un niveau ne se coche **qu'avec son livrable poussé sur GitHub**.
- Pendant un cycle, on ne travaille que sur ce qui sert l'objectif du cycle.
- Le cycle 2 (7 déc → 17 janv) est un cycle **LEARN** : nand2tetris projets 1 et 2.
- Le cycle 3 (19 janv → 1 mars) est un cycle **SHIP** : Scribe et les revenus.

## La règle d'alternance

```
Cycle 1  SHIP   Orane.d      → une chose finie et publiée
Cycle 2  LEARN  nand2tetris  → une compétence prouvée
Cycle 3  SHIP   Scribe       → un euro encaissé
```

Un cycle ne mélange jamais deux natures. C'est ce qui évite les trois moitiés de projet.
