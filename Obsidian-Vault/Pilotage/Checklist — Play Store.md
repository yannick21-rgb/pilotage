---
type: checklist
maj: 2026-10-23
---

# Checklist — Play Store

> Tout ce qui doit être vrai avant de publier Orane.d. Coche au fur et à mesure.
> **124 points au total — mais tu n'en lis qu'un à la fois.** Le dashboard affiche seulement la section en cours et la prochaine case.
> Les règles changent : revérifie les 3 bloquants avant chaque cycle.

## 0. Les 3 bloquants 2026

| Bloquant | Ce qu'il impose | Où on en est |
|---|---|---|
| **targetSdk 36** | Depuis le 31 août 2026, tout nouvel envoi doit cibler Android 16 (API 36) | À vérifier au build (leçon 20) |
| **12 testeurs × 14 jours** | Compte personnel créé après le 13 nov. 2023 : test fermé avec 12 testeurs opt-in **en continu** pendant 14 jours avant de demander la production | 5 étudiants ne suffisent pas |
| **Suppression de compte** | Si l'app crée des comptes : suppression dans l'app **et** URL web publique, déclarée dans Data safety | À construire (leçon 24) |

## 1. Compte développeur

- [ ] Compte Google dédié à Orane.d, pas le compte personnel
- [ ] Inscription sur play.google.com/console
- [ ] Payer les 25 $ une fois (carte Visa ou Mastercard)
- [ ] Vérification d'identité lancée (pièce + adresse)
- [ ] Vérification d'identité validée (1 à 3 jours, parfois plus)
- [ ] Profil développeur public rempli (nom, email, site)
- [ ] Email de support vérifié
- [ ] Validation en 2 étapes activée sur le compte Google
- [ ] Developer Distribution Agreement accepté
- [ ] Pays du compte vérifié : Bénin = inscription développeur et marchand supportées, devise USD
- [ ] Date de vérification notée dans le journal

## 2. Identité de l'app

- [ ] Nom de l'app décidé, 30 caractères maximum
- [ ] Nom vérifié : marque, homonyme, disponibilité
- [ ] `applicationId` définitif choisi (ex. `com.jhpy.oraned`)
- [ ] Même identifiant dans `app.json`, `build.gradle` et EAS
- [ ] Icône 512×512, PNG 32 bits, moins de 1 Mo
- [ ] Icône adaptative (foreground + background) dans l'app
- [ ] Splash screen aux couleurs de l'app
- [ ] Version `1.0.0`, `versionCode` 1
- [ ] Catégorie Play : Finance
- [ ] Langue par défaut : français
- [ ] Public cible : 13+ ou 18+, pas « enfants »

## 3. Build et signature

- [ ] Expo SDK à jour, compatible targetSdk 36 (SDK 54 minimum, RN 0.81+)
- [ ] `targetSdkVersion` = 36
- [ ] `compileSdkVersion` = 36
- [ ] `minSdkVersion` décidé (24 = Android 7)
- [ ] Build de production en **AAB**, pas en APK
- [ ] Play App Signing activé au premier envoi
- [ ] Keystore et upload key sauvegardés hors du projet (2 endroits)
- [ ] Credentials EAS configurées et testées
- [ ] `versionCode` incrémenté à chaque envoi
- [ ] `versionName` lisible (1.0.0)
- [ ] Build release testé, pas seulement le build dev
- [ ] R8 / ProGuard et Hermes vérifiés sur le build release
- [ ] Bibliothèques 64-bit présentes
- [ ] Permissions nettoyées : pas de permission de debug
- [ ] `npx expo-doctor` sans erreur
- [ ] `npm audit` sans vulnérabilité critique
- [ ] Secrets dev et prod séparés
- [ ] Clé `service_role` absente du bundle
- [ ] Logs de debug désactivés en production
- [ ] Deep links testés (si utilisés)
- [ ] Notifications testées sur Android 13+ (si utilisées)
- [ ] Icône et splash vérifiés sur un appareil réel
- [ ] Build installé sur un Android récent et un Android ancien

## 4. Conformité et politiques

- [ ] Privacy policy rédigée : données, finalité, durée, tiers, contact
- [ ] Privacy policy publiée à une URL publique, sans login
- [ ] URL de la privacy policy ajoutée dans Play Console
- [ ] Lien vers la privacy policy dans l'app
- [ ] Data safety rempli : types, finalité, partage, chiffrement, suppression
- [ ] Data safety cohérent avec la privacy policy
- [ ] Content rating IARC rempli honnêtement
- [ ] Public cible déclaré (13+ ou 18+)
- [ ] Déclaration « ads » : non
- [ ] Déclaration « news app » : non
- [ ] Déclaration « government app » : non
- [ ] Déclaration « health » : non
- [ ] Déclaration « financial features » : budgeting, pas de produit financier
- [ ] Suppression de compte disponible **dans l'app**
- [ ] URL web de suppression de compte publique
- [ ] Suppression effective : données, fichiers, compte auth
- [ ] Délai de suppression annoncé (ex. 30 jours)
- [ ] App access : compte de test fourni à Google
- [ ] Identifiants de test valides au moment de la review
- [ ] Permissions sensibles justifiées dans la console
- [ ] Consentement analytics et pubs si utilisateur UE
- [ ] Aucune donnée collectée sans déclaration
- [ ] Export compliance / cryptographie rempli si demandé

## 5. Fiche Play

- [ ] Nom : 30 caractères maximum
- [ ] Description courte : 80 caractères maximum
- [ ] Description longue : 4000 caractères maximum
- [ ] Icône : 512×512, PNG 32 bits
- [ ] Feature graphic : 1024×500, JPEG ou PNG 24 bits, sans alpha
- [ ] 4 à 8 captures téléphone (1080×1920 recommandé)
- [ ] Captures qui montrent l'usage, pas seulement le login
- [ ] Aucun texte trompeur dans les captures
- [ ] Vidéo promo (optionnelle)
- [ ] Catégorie et tags choisis
- [ ] Email de support affiché
- [ ] Site web (optionnel) affiché
- [ ] URL de privacy policy affichée
- [ ] Pays de distribution sélectionnés
- [ ] Prix : gratuit
- [ ] Type : application, pas jeu
- [ ] Fiche relue sur mobile, pas seulement sur desktop

## 6. Tests et tracks

- [ ] Build interne uploadé et installé
- [ ] Internal app sharing testé (optionnel)
- [ ] Pré-launch report lu : captures, crashs, ANR
- [ ] Test interne validé sur ton téléphone
- [ ] 5 étudiants recrutés pour le feedback qualitatif
- [ ] 12 testeurs avec une adresse Google recrutés
- [ ] Liste d'emails créée dans Play Console
- [ ] Track « test fermé » configuré
- [ ] Release notes rédigées pour les testeurs
- [ ] 12 opt-in confirmés (capture)
- [ ] Date de début des 14 jours notée
- [ ] Date de fin des 14 jours notée (début + 14)
- [ ] Canal de feedback ouvert (WhatsApp, formulaire)
- [ ] Crashs et ANR surveillés pendant le test
- [ ] 3 correctifs prioritaires livrés
- [ ] Test suspendu ou arrêté si crash bloquant

## 7. Production

- [ ] 14 jours continus terminés
- [ ] Demande d'accès production remplie
- [ ] Réponses honnêtes : testeurs, feedback, pays, usage
- [ ] Revue Google terminée (souvent ≤ 7 jours)
- [ ] Accès production accordé
- [ ] Release de production créée avec le même AAB
- [ ] Staged rollout à 10–20 %
- [ ] Vitals surveillés 48 h
- [ ] Seuils d'arrêt définis : crash > 1 %, ANR > 0,5 %, login cassé
- [ ] Rollout augmenté ou arrêté selon les chiffres
- [ ] Version à 100 %
- [ ] Fiche vérifiée en ligne
- [ ] Lien Play partagé (étudiants, réseaux)

## 8. Après publication

- [ ] Répondre à tous les avis, surtout les 1–3 étoiles
- [ ] Alertes Sentry configurées
- [ ] Android vitals vérifiés chaque semaine
- [ ] Events analytics vérifiés dans le dashboard
- [ ] Rétention J1 et J7 mesurées
- [ ] Bugs triés dans le backlog
- [ ] Prochaine release planifiée (2 à 4 semaines)
- [ ] `targetSdk` surveillé pour la prochaine obligation
- [ ] Sauvegarde et restauration testées
- [ ] Post-mortem du lancement écrit

## 9. Motifs de rejet à éviter

| Motif | La cause | Le correctif |
|---|---|---|
| targetSdk trop bas | Build configuré sur 35 ou moins | Passer à 36 |
| Privacy policy absente | URL vide ou page derrière un login | Publier une page publique |
| Data safety incohérent | Déclaration qui ne correspond pas au code | Auditer les SDK et les données |
| Suppression de compte absente | Comptes créés sans chemin de suppression | Ajouter in-app + URL |
| Login de test invalide | Compte expiré ou mot de passe changé | Fournir un compte stable |
| Permissions non justifiées | Permission sensible sans usage clair | Retirer ou expliquer |
| Captures trompeuses | Interface qui n'existe pas | Captures réelles |
| Crash au démarrage | Build release non testé | Tester le build release |
| Contenu copié | Nom, logo, texte d'un autre | Original ou licence |
| Paiement hors Play Billing | Abonnement numérique in-app | Play Billing ou retirer |
| Ads intrusives | Plein écran à répétition | Respecter les formats |
| Données d'enfants | Public cible mal déclaré | Déclarer 13+ |

## 10. Calendrier dans le cycle 1

```
26 oct → 8 nov    Écrans et bugs           jalons 1
9 nov  → 15 nov   Compte Play + build      leçons 16–20
16 nov → 22 nov   Fiche + conformité       leçons 21–24
23 nov → 27 nov   Test fermé lancé         leçon 25
27 nov → 11 déc   14 jours de test         hors cycle
11 déc            Demande production       action de 10 min
18 déc            Décision Google (≈)      release 10–20 %
janv → févr       Production Orane.d       cycle 2 (2 soirs)
mars → avril      Croissance Orane.d       cycle 4 (rétention, ASO)
```

## 11. Ce qui peut attendre

- Les tests A/B de la fiche : après 100 installations.
- La monétisation : après la rétention.
- iOS : après la production Android.
- Les tablettes : après la première version stable.
- Le multi-langue : après le premier mois.
