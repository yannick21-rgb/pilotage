---
type: cycle
numero: 1
nom: Orane.d
objectif: "Orane.d en test fermé sur le Play Store, avec 12 testeurs opt-in pendant 14 jours"
projet: Orane.d
debut: 2026-10-26
fin: 2026-12-06
statut: actif
---

# Cycle 1 — Orane.d

> **Objectif unique :** Orane.d en test fermé sur le Play Store, avec 12 testeurs opt-in pendant 14 jours.
> 6 semaines. Le périmètre peut rétrécir, la date ne bouge pas.

**Hors cycle, explicitement :**
- Scribe : gelé jusqu'au 6 décembre (sauf bug bloquant).
- nand2tetris : 1 soir/semaine, le mardi. Pas une piste, un entretien.
- NIA Clipper : 1 h/semaine, le jeudi. Prospection seulement, zéro code.
- site-web-C : 1 h de fermeture sécurité, puis archivage.
- Tout le reste : archivé sur GitHub.

## Jalon 1 — Fermer les écrans et les bugs
*Échéance : dimanche 8 novembre*

- [ ] Terminer l'écran Objectifs
- [ ] Terminer l'écran Rapports
- [ ] Fermer les bugs bloquants listés dans `STATE.md`

## Jalon 2 — Compte, build et fiche Play
*Échéance : dimanche 22 novembre*

- [ ] Compte développeur Play créé et vérifié (25 $, identité)
- [ ] EAS Build + signature + targetSdk 36, build interne installé
- [ ] Fiche Play et formulaires de conformité remplis

## Jalon 3 — Test réel et décision
*Échéance : dimanche 6 décembre*

- [ ] Test fermé lancé avec 12 testeurs opt-in (au plus tard le 23 novembre)
- [ ] Corriger les 3 retours les plus importants
- [ ] Démo devant 5 étudiants + décision écrite

## Notes de cycle

- **La règle Play 2026** : un compte personnel doit avoir 12 testeurs opt-in **en continu pendant 14 jours** avant de demander l'accès production. 5 étudiants suffisent pour le feedback, pas pour débloquer la production. Si le test démarre le 27 novembre, les 14 jours finissent le 11 décembre : demande le 11, accès vers le 18. La release production se fait alors en 2 soirs au début du cycle 2 — ce n'est pas un nouveau projet, c'est la clôture du cycle 1.
- **targetSdk 36** (Android 16) est obligatoire depuis le 31 août 2026. Sans ça, Google refuse l'envoi.
- Les détails techniques vivent dans le dépôt : `STATE.md` et `ROADMAP.md` (remis à jour le 23 octobre).
- Une action n'est cochée que si elle est poussée sur GitHub ou visible dans un lien.
- Le parcours quotidien est dans [[Parcours — App mobile]]. La partie non-code est dans [[Checklist — Play Store]].
- Les preuves de la semaine sont dans [[Preuves]].
- La revue du dimanche est dans [[Revue hebdo]].
