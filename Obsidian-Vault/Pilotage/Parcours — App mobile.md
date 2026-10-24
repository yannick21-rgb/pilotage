---
type: parcours
maj: 2026-10-23
total: 30
debut: 2026-10-26
fin: 2026-12-04
---

# Parcours — App mobile

> De l'idée au Play Store. **Une leçon par jour, 45 min, appliquée à Orane.d.**
> La carte complète ci-dessous est le territoire. Le tableau des 30 jours est la route.
> La leçon du jour s'affiche sur le dashboard et dans le briefing.

## Comment ça marche

- **45 min par soir** : 20 min de lecture, 25 min d'exercice dans Orane.d.
- **Une leçon = une notion + un exercice + une preuve.** Pas de cours sans application.
- **Si tu rates un soir** : tu ne rattrapes pas, tu continues. Le tableau est une route, pas une dette.
- **Le dimanche** : la revue remplace la leçon. Tu publies la preuve de la semaine.
- **La leçon ne remplace pas l'action du cycle.** Elle la rend possible. Si l'exercice déborde, il devient l'action du lendemain.

## De zéro à publié — les 8 étapes

| Étape | Ce que tu produis | Critère pour passer à la suite |
|---|---|---|
| 1. Cadrer | Une phrase problème + 5 interviews | 3 personnes confirment le problème |
| 2. Définir le MVP | 3 écrans + 1 parcours critique | Maquette cliquable, scope écrit |
| 3. Poser les fondations | Expo + TypeScript + navigation + thème | L'app navigue entre 3 écrans |
| 4. Brancher les données | Supabase + auth + RLS | 2 comptes ne voient pas les mêmes données |
| 5. Construire le parcours | 1 action utile + états vide/chargement/erreur | Utilisable sans bug bloquant |
| 6. Tester | Unitaires + E2E + 5 testeurs | 0 bug bloquant, 3 retours traités |
| 7. Builder | AAB signé + fiche + conformité | Build installé sur un appareil réel |
| 8. Publier | Test fermé 12 × 14 jours + production | App en ligne sur le Play Store |

> Orane.d est déjà aux étapes 5–6. Le parcours de 30 jours te fait monter jusqu'à l'étape 8.
> Pour un futur projet, tu reprends le tableau au début : les étapes 1–4 prennent 2 à 3 semaines.

## Budget et comptes

| Poste | Coût | Quand |
|---|---|---|
| Google Play Console | 25 $ une fois | Avant le premier envoi |
| Expo / EAS | gratuit, puis ~0–30 $/mois | Si tu builds beaucoup |
| Supabase | gratuit, puis ~25 $/mois | Quand la prod dépasse le quota |
| Sentry | gratuit au début | Dès le test fermé |
| PostHog | gratuit au début | Dès le test fermé |
| Domaine (privacy policy) | ~10 $/an | Avant la fiche Play |
| Total démarrage | ~35 $ | Cycle 1 |

Comptes à créer : Google, Play Console, Expo, Supabase, GitHub, Sentry, PostHog.
Un compte Google dédié à l'app, pas ton compte personnel.

## Les documents à produire

- **Note de cadrage** : problème, utilisateur, promesse, critère de succès. Une page.
- **MVP** : 3 écrans, 1 parcours, ce qui est exclu. Une page.
- **Privacy policy** : données, finalité, durée, tiers, suppression, contact. Publique.
- **Conditions d'utilisation** : règles, responsabilité, résiliation. Publique.
- **Fiche Play** : nom, descriptions, captures, bannière.
- **Release notes** : ce qui change, pour les testeurs puis les utilisateurs.
- **Runbook** : comment builder, signer, publier, revenir en arrière.
- **Post-mortem** : ce qui a cassé, pourquoi, ce qui change.

## La carte complète — ce que tu dois savoir

### 0. Le métier

- Ce qu'est une app : un client mobile + un backend + une fiche sur un store.
- Le cycle de vie : idée → cadrage → MVP → build → test → publication → maintenance.
- Les rôles : produit, design, développement, QA, release, support. En solo, tu es les six.
- Ce que « fini » veut dire : installable, utilisable, stable, conforme, publié.
- Les coûts : $25 Play, serveur (Supabase gratuit au début), outils, temps.
- Les risques : périmètre qui gonfle, perfectionnisme, API qui casse, rejet du store.
- Android d'abord : plus simple à tester, Play Store accessible, un seul parcours à maîtriser.
- Pourquoi iOS attend : 99 $/an, Mac obligatoire pour builder, review plus stricte.

### 1. Idée et validation

- Le problème avant la solution. Une phrase : « [utilisateur] galère à [tâche] parce que [cause] ».
- 5 interviews de 15 min. Questions sur le passé, pas sur ton idée.
- Les signaux qui comptent : ils utilisent déjà un tableur, ils ont payé pour autre chose, ils demandent quand c'est prêt.
- Concurrence : qui résout déjà ça, pourquoi tu fais différemment, en une phrase.
- MVP : la plus petite chose qui résout le problème principal. Pas la plus petite chose facile à coder.
- Critère de succès mesurable : « 5 étudiants l'utilisent 7 jours de suite », pas « les gens aiment ».
- Modèle économique : gratuit, freemium, abonnement, pub. À décider avant la fiche Play.
- Page d'attente / liste d'emails : le premier test de demande.
- Go / no-go : si personne ne veut tester, tu changes d'idée avant de coder 3 mois.

### 2. Produit et périmètre

- User stories : « en tant que…, je veux…, pour… ».
- Parcours critique : inscription → première action utile → retour le lendemain. Tout le reste est secondaire.
- Priorisation : MoSCoW (must, should, could, won't) ou RICE.
- Scope freeze : ce qui n'est pas dans le cycle est « pas maintenant », pas « en pause ».
- Définition de « fait » : code + test + preuve + documentation.
- Roadmap par cycles de 6 semaines, pas par mois.
- Métriques : activation (1re action), rétention J1/J7, engagement, crash.
- Boucle de feedback : testeur → bug → correctif → remerciement.
- Le backlog est un cimetière si personne ne le trie. Une revue par semaine.

### 3. UX / UI mobile

- Mobile-first : une tâche par écran, une action principale par écran.
- Navigation : tabs pour les zones, stack pour les détails, modal pour les formulaires courts.
- Deep links : ouvrir l'app sur un écran précis depuis un lien.
- Hiérarchie visuelle : titre, sous-titre, contenu, action. Une seule couleur d'accent.
- Espacement : échelle de 4 ou 8 px. Jamais de valeurs au hasard.
- Typographie : 2 polices maximum, 5 tailles maximum, hauteur de ligne 1,4–1,6.
- Contraste : 4,5:1 pour le texte normal, 3:1 pour le grand texte.
- États : vide, chargement, erreur, succès, hors ligne. Les oublier = app qui semble cassée.
- Formulaires : label visible, validation inline, bon clavier (`numeric`, `email`), autofill.
- Accessibilité : cible tactile 44×44, labels sur les icônes, support du texte agrandi.
- Onboarding : la promesse en 3 écrans, les permissions au moment où elles servent.
- Design system : couleurs, espacement, typo, rayons, ombres dans un seul fichier de tokens.
- Composants : bouton, champ, carte, badge, écran vide. Réutiliser, ne pas recopier.
- Dark mode : dès le début, c'est plus dur après.
- Localisation : français d'abord, anglais ensuite. Dates et monnaie formatées par locale.
- Microcopy : les messages d'erreur disent quoi faire, pas « une erreur est survenue ».
- Prototype : Figma ou Penpot (libre) avant de coder un écran complexe.

### 4. React Native et Expo

- React : composants, props, state, rendu, listes, événements.
- Le rendu : une fonction qui transforme l'état en interface. Les effets sont pour le monde extérieur.
- État dérivé : si une valeur se calcule à partir d'une autre, calcule-la au rendu, pas dans un `useEffect`.
- Hooks : `useState`, `useEffect`, `useMemo`, `useCallback`, `useRef`, hooks personnalisés.
- RN : `View`, `Text`, `Image`, `ScrollView`, `FlatList`, `Pressable`, `StyleSheet`, `Flexbox`.
- Expo : SDK, `app.json` / `app.config.ts`, dev client, `expo start`, `expo install`.
- Expo Router : routes par fichiers, `_layout`, groupes, paramètres, guards d'authentification.
- State global : Context pour le thème et la session, Zustand si l'état devient large. Redux seulement si tu sais pourquoi.
- Data fetching : TanStack Query (cache, retry, invalidation, optimistic update).
- Formulaires : `react-hook-form` + `zod`.
- Animations : Reanimated, transitions de navigation, respect de « réduire les animations ».
- Gestes : Gesture Handler, swipe, drag, bottom sheet.
- Notifications : `expo-notifications`, permission Android 13+, FCM.
- Images et polices : `expo-image`, `expo-font`, splash, icône adaptative.
- Performance : FlashList, `memo`, éviter les re-rendus, Hermes, taille du bundle.
- Debug : Metro, React DevTools, logs, onglet réseau, `expo-doctor`.
- OTA : `expo-updates` met à jour le JS, pas le natif. Ne pas en abuser.
- Modules natifs : plus tard, seulement si Expo ne sait pas faire.

### 5. TypeScript

- Types primitifs, `interface`, `type`, unions, littéraux.
- Generics : `Array<T>`, `Promise<T>`, `Record<K, V>`.
- Utility types : `Partial`, `Pick`, `Omit`, `ReturnType`.
- Narrowing : `typeof`, `in`, `instanceof`, type guards.
- `strict: true`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`.
- Typer les props, les réponses API, les événements, les routes.
- `zod` pour valider au runtime ce que TypeScript ne voit pas.
- Les pièges : `any`, `as`, optional chaining qui cache un bug, types trop larges.
- `tsc --noEmit` dans la CI. Zéro erreur.

### 6. Données et backend

- Client-serveur : requête, réponse, statut HTTP, JSON, erreurs.
- Supabase : Auth, Postgres, Storage, Edge Functions, Realtime.
- Schéma relationnel : tables, clés primaires, clés étrangères, contraintes.
- SQL de base : `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `JOIN`, `GROUP BY`, agrégats.
- Index : sur les colonnes filtrées et triées. `user_id` et `date` en premier.
- Migrations : versionnées, rejouables, jamais éditées à la main en prod.
- RLS : activée sur toutes les tables, politiques par opération, `auth.uid()`.
- Tester RLS avec **deux** comptes : l'un ne doit jamais voir les données de l'autre.
- Auth : email/mot de passe, OTP, OAuth, session, refresh, logout, suppression de compte.
- Stockage local : AsyncStorage pour le cache, SecureStore pour les tokens, SQLite pour le volume.
- Offline-first : lire le cache d'abord, écrire en file d'attente, gérer les conflits.
- Pagination : curseur plutôt que `offset` quand la liste grandit.
- Temps réel : seulement si l'UX en a besoin. Sinon, polling contrôlé.
- Sauvegardes : export, restauration, test de restauration.
- Quotas et limites : lire les limites du plan gratuit avant de promettre.

### 7. Réseau, erreurs, résilience

- États réseau : en ligne, hors ligne, lent, instable.
- Timeouts, retries avec backoff, idempotence des écritures.
- Erreurs HTTP : 400 validation, 401 session, 403 droits, 404 absent, 429 limite, 5xx serveur.
- Messages utilisateur : ce qui s'est passé, ce qu'il peut faire, ce que tu fais.
- Error boundaries : une erreur d'écran ne tue pas toute l'app.
- Logs structurés : niveau, contexte, identifiant de requête. Pas de données personnelles.
- Mode dégradé : consultation seule quand le réseau manque.
- Tester la coupure : mode avion, réseau lent, serveur éteint.

### 8. Sécurité et confidentialité

- Ne jamais mettre la clé `service_role` dans l'app. La clé `anon` est publique, protégée par RLS.
- Secrets : variables d'environnement, EAS secrets, jamais dans Git.
- RLS par défaut : deny. Chaque accès est une politique explicite.
- Validation côté serveur, pas seulement côté client.
- Rate limiting et quotas sur les endpoints sensibles.
- Tokens dans SecureStore, pas AsyncStorage.
- HTTPS partout. Certificate pinning plus tard, si nécessaire.
- Minimisation : ne collecte que ce qui sert.
- Durée de conservation et suppression réelle des données.
- RGPD / consentement : analytics et pubs seulement après accord si utilisateur UE.
- Privacy policy publique + Data safety + suppression de compte in-app et web.
- OWASP Mobile Top 10 : stockage insecure, mauvaise auth, fuite de données, injection.
- `npm audit` et mises à jour des dépendances.

### 9. Tests et qualité

- Pyramide : beaucoup d'unitaires, quelques tests de composants, peu d'E2E.
- Jest : logique pure, calculs, validations, transformations.
- React Native Testing Library : rendu, interactions, accessibilité.
- Maestro (ou Detox) : parcours critique sur un appareil réel.
- Ce qu'il faut tester : calculs d'argent, formulaires, auth, création de données, écran vide.
- Matrice manuelle : ton téléphone, un Android récent, un Android ancien, petite taille d'écran.
- Bug report : étapes, attendu, observé, capture, version, appareil.
- Revue de code : même solo, relire sa PR une fois avant de merger.
- ESLint + Prettier : zéro warning avant le build.
- CI : lint + types + tests sur chaque push. EAS Build sur tag.
- Definition of done : code, test, preuve, doc, pas de TODO caché.

### 10. Build, signature, release

- AAB pour le Play Store, APK pour installer à la main.
- `applicationId` définitif avant la première publication. Il ne change plus.
- `versionCode` : entier qui augmente à chaque envoi. `versionName` : ce que voit l'utilisateur.
- `targetSdkVersion` 36 (Android 16) obligatoire depuis le 31 août 2026.
- `minSdkVersion` : décide quels téléphones peuvent installer. 24 = Android 7.
- Signature : keystore, upload key, Play App Signing. Perdre la clé = perdre les mises à jour.
- EAS Build : profils `development`, `preview`, `production`. Un profil = un usage.
- Variables par environnement : Supabase dev, Supabase prod, Sentry, analytics.
- R8 / ProGuard : réduire et obfusquer. Tester le build release, pas seulement le dev.
- 64-bit : obligatoire. Vérifier les libs natives.
- Permissions : déclarer seulement celles utilisées. Justifier les sensibles.
- Icône adaptative, splash, nom affiché.
- Build reproductible : même commit + mêmes secrets = même build.
- Release notes : ce qui change, en français, pour les testeurs.
- Hotfix : petite version, rollback possible, communication.

### 11. Play Store et conformité

- Compte développeur : 25 $ une fois, vérification d'identité, profil public.
- Les tracks : interne (rapide), fermé (liste d'emails), ouvert (public), production.
- Compte personnel créé après le 13 novembre 2023 : **12 testeurs opt-in pendant 14 jours** avant de demander la production.
- Demande d'accès production : formulaire + revue (souvent ≤ 7 jours).
- Fiche : nom 30 caractères, description courte 80, description longue 4000.
- Icône 512×512 PNG 32 bits, feature graphic 1024×500 JPEG/PNG sans alpha, 4 à 8 captures.
- Privacy policy : URL publique, accessible sans app.
- Data safety : types de données, finalité, partage, chiffrement, suppression.
- Content rating : questionnaire IARC. Répondre honnêtement.
- Suppression de compte : chemin dans l'app **et** URL web publique.
- App access : si l'app demande un login, fournir un compte de test à Google.
- Déclarations : pubs, actualités, gouvernement, santé, fonctions financières, public cible.
- Pays de distribution, prix, contenu.
- Review : délai variable, rejet possible, appel possible.
- Staged rollout : 5–20 %, surveiller les vitals, augmenter ou arrêter.
- Android vitals : crash rate, ANR, démarrage lent. Seuils à ne pas dépasser.
- Politiques : spam, permissions, données, propriété intellectuelle, paiements.

### 12. Distribution, ASO, analytics, monétisation

- ASO : titre avec le mot-clé principal, description courte qui donne envie, captures qui montrent l'usage.
- Les 3 premières captures font 80 % du travail. La première montre le résultat, pas l'écran de login.
- Mots-clés : ce que les gens tapent, pas ce que tu aimes dire.
- Reviews : répondre à tout, surtout aux 1–3 étoiles. Une réponse calme désarme.
- Analytics : 5 à 10 events maximum au début. Nommer au passé (`goal_created`).
- Funnel : install → signup → première action → retour J1 → J7.
- Rétention : la seule métrique qui dit si l'app sert à quelque chose.
- Crash / ANR : Sentry + Android vitals, alertes.
- A/B test : store listing experiments (icône, captures, description courte).
- Canaux : campus, groupes WhatsApp/Telegram, bouche-à-oreille, réseaux.
- Monétisation : gratuit, freemium, abonnement, IAP, pub.
- Play Billing obligatoire pour le numérique in-app. Stripe/Chariow pour le SaaS hors app.
- Prix : teste, mesure, ajuste. Un prix trop bas attire les mauvais clients.
- Support : email, FAQ, délai de réponse annoncé.

### 13. Maintenance et itération

- Rythme de release : toutes les 2 à 4 semaines, pas tous les jours.
- Triage : bug, amélioration, idée. Le backlog se vide ou meurt.
- Mises à jour SDK : une fois par trimestre, avant que Google l'impose.
- `targetSdk` augmente chaque année. Prévois-le dans un cycle.
- Sauvegardes et incidents : savoir restaurer avant d'en avoir besoin.
- Post-mortem : ce qui a cassé, pourquoi, ce qui change.
- Documentation : README, `STATE.md`, runbook de release.
- Dépréciation : supprimer une fonctionnalité est une décision produit, pas un oubli.

## Ce que tu n'apprends pas maintenant

- Kotlin et Swift natifs : utiles plus tard, pas pour livrer Orane.d.
- La New Architecture de React Native en détail : Expo s'en occupe.
- Microservices, Kubernetes, monorepo : surdimensionné pour une app solo.
- Machine learning, jeux, 3D : un autre métier.
- Le perfectionnement du design system : un thème propre suffit pour le cycle 1.

## Les 30 jours — cycle 1

| # | Date | Thème | Concept | Exercice Orane.d | Preuve |
|---|---|---|---|---|---|
| 1 | 2026-10-26 | TypeScript | `strict`, unions, typer les props et les modèles | Activer `strict`, typer `Objectif` et `Transaction`, corriger les erreurs | `tsc --noEmit` passe |
| 2 | 2026-10-27 | React | état dérivé vs `useEffect` | Remplacer un `useEffect` de total par un calcul au rendu | commit + test manuel |
| 3 | 2026-10-28 | Expo Router | routes, layouts, paramètres, deep link | Cartographier `app/`, ajouter un lien `oraned://objectifs` | capture du deep link |
| 4 | 2026-10-29 | State | état local vs global, hook personnalisé | Sortir l'état du formulaire dans `useObjectifForm` | commit |
| 5 | 2026-10-30 | Formulaires | `react-hook-form` + `zod`, erreurs inline | Valider montant > 0, date future, nom 3–40 caractères | 3 captures d'erreur |
| 6 | 2026-11-02 | Auth | session, refresh, guards, logout | Protéger le groupe `(app)`, gérer la déconnexion | 2 comptes testés |
| 7 | 2026-11-03 | Postgres | clés, contraintes, index, migrations | Ajouter l'index `transactions(user_id, date)` | migration versionnée |
| 8 | 2026-11-04 | RLS | politiques par opération, `auth.uid()` | Écrire 4 politiques sur `objectifs`, tester avec 2 comptes | capture des 2 vues |
| 9 | 2026-11-05 | Data fetching | cache, invalidation, optimistic update | Liste des objectifs + invalidation après création | commit |
| 10 | 2026-11-06 | Offline | persistance du cache, mode avion | Ouvrir l'app sans réseau et voir les dernières données | capture mode avion |
| 11 | 2026-11-09 | Onboarding | promesse, permissions au bon moment | 3 écrans, notifications demandées après la 1re action | capture |
| 12 | 2026-11-10 | États | vide, chargement, erreur, succès | Les 4 états de l'écran Rapports | 4 captures |
| 13 | 2026-11-11 | Design system | tokens, échelle d'espacement, typo | Créer `theme.ts`, remplacer les valeurs en dur sur 2 écrans | commit |
| 14 | 2026-11-12 | Accessibilité | labels, contraste, cible 44 px, texte agrandi | Audit des 2 écrans, corriger 5 points | liste avant/après |
| 15 | 2026-11-13 | i18n | `t()`, dates, monnaie, locale | Externaliser 30 chaînes, formater en `fr-BJ` | commit |
| 16 | 2026-11-16 | Tests unitaires | Jest, cas limites, arrondis | Tester le calcul de solde : vide, négatif, arrondi | tests verts |
| 17 | 2026-11-17 | Tests composants | RNTL, interactions, accessibilité | Tester le formulaire d'objectif : validation + submit | tests verts |
| 18 | 2026-11-18 | E2E | Maestro, parcours critique | Scénario inscription → créer un objectif → le voir | rapport ou vidéo |
| 19 | 2026-11-19 | Compte Play | 25 $, vérification d'identité, profil | Créer le compte, lancer la vérification, noter le délai | capture compte vérifié |
| 20 | 2026-11-20 | Build | EAS, AAB, signature, targetSdk 36 | `eas build -p android --profile production` | lien du build |
| 21 | 2026-11-23 | Environnements | dev/prod, `EXPO_PUBLIC_`, EAS secrets | Séparer Supabase dev et prod, rebuild | 2 builds distincts |
| 22 | 2026-11-24 | Versioning | `versionCode`, `versionName`, changelog | Passer en 1.0.0 / code 1, tag Git | tag + release notes |
| 23 | 2026-11-25 | Fiche Play | nom 30, short 80, full 4000, assets | Rédiger les textes, exporter icône, bannière, 4–8 captures | fiche prête |
| 24 | 2026-11-26 | Conformité | privacy, Data safety, rating, suppression | Remplir les 5 formulaires, fournir un compte de test | tout vert |
| 25 | 2026-11-27 | Test fermé | 12 testeurs, 14 jours, track fermé | Créer la liste de 12 emails, lancer le rollout | 12 opt-in |
| 26 | 2026-11-30 | Triage | bug vs feature, P0/P1/P2 | Classer les retours, corriger 3 P0/P1 | issues + commits |
| 27 | 2026-12-01 | Crashs | Sentry, symboles, Android vitals | Brancher Sentry, provoquer une erreur test | événement visible |
| 28 | 2026-12-02 | Analytics | events, funnel, rétention | Instrumenter 5 events clés | dashboard |
| 29 | 2026-12-03 | ASO | titre, mots-clés, captures, note | 2 variantes de description courte + 1re capture | avant/après |
| 30 | 2026-12-04 | Bilan | rétro, décision, demande production | Écrire la rétro, préparer la demande (à J+14, le 11/12) | note + soumission |

## Ma progression

> Coche une leçon quand sa preuve existe. La page **Progression** du dashboard et le briefing lisent cette liste.
> En terminal : `python3 ~/.hermes/scripts/pilotage.py --done 3` (ou `--undone 3`).

- [ ] 1. TypeScript
- [ ] 2. React
- [ ] 3. Expo Router
- [ ] 4. State
- [ ] 5. Formulaires
- [ ] 6. Auth
- [ ] 7. Postgres
- [ ] 8. RLS
- [ ] 9. Data fetching
- [ ] 10. Offline
- [ ] 11. Onboarding
- [ ] 12. États
- [ ] 13. Design system
- [ ] 14. Accessibilité
- [ ] 15. i18n
- [ ] 16. Tests unitaires
- [ ] 17. Tests composants
- [ ] 18. E2E
- [ ] 19. Compte Play
- [ ] 20. Build
- [ ] 21. Environnements
- [ ] 22. Versioning
- [ ] 23. Fiche Play
- [ ] 24. Conformité
- [ ] 25. Test fermé
- [ ] 26. Triage
- [ ] 27. Crashs
- [ ] 28. Analytics
- [ ] 29. ASO
- [ ] 30. Bilan

## Après le cycle 1

- **Cycle 2 — nand2tetris** : le parcours mobile continue en autonomie, 2 soirs/semaine. Objectif : publier Orane.d en production dès que l'accès est accordé.
- **Cycle 3 — Scribe** : le parcours se rejoue sur un produit différent. Les modules 1, 2, 11 et 12 deviennent prioritaires (validation, périmètre, Play, monétisation).
- **Cycle 4 — Orane.d croissance** : modules 9, 10, 11, 13. Rétention, ASO, itération, nouvelles fonctionnalités.
- **Ensuite** : iOS si un client le demande. Le prochain parcours sera « SaaS web », pas « app mobile ».

## Ressources

- Docs Expo : https://docs.expo.dev
- React Native : https://reactnative.dev/docs/getting-started
- TypeScript Handbook : https://www.typescriptlang.org/docs/handbook
- Supabase Docs : https://supabase.com/docs
- Play Console Help : https://support.google.com/googleplay/android-developer
- Target API : https://developer.android.com/google/play/requirements/target-sdk
- Tests Play (12 testeurs) : https://support.google.com/googleplay/android-developer/answer/14151465
- Data safety : https://support.google.com/googleplay/android-developer/answer/10787469
- Suppression de compte : https://support.google.com/googleplay/android-developer/answer/13327111
- Maestro : https://maestro.mobile.dev
- Sentry React Native : https://docs.sentry.io/platforms/react-native
