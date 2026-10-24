Orane.d app: /home/jhpy/FinanceTracker (package.json name "orane.d"). Expo + React Native + Supabase, start with `npx expo start --lan` (tunnel/ngrok unstable → ETXTBSY). Linux Mint GNOME, DISPLAY=:1 for GUI apps.
§
Project conventions: Conventional Commits in French (feat/fix/refactor), functional components (const + arrow), named exports only, StyleSheet.create, i18n via LanguageManager t(), lucide-react-native icons, custom UI from src/view/components/ui.
§
New project: ~/video-poster/ — automation pipeline Google Flow → pipevideo (montage) → treg (upload YouTube + TikTok). Files: pipeline.py, poster.py, README.md.
§
treg CLI installed at ~/.treg/ (token in ~/.treg/config.json). MCP treg configured in ~/.hermes/config.yaml (mcp_servers.treg → https://treg.to/mcp/). Team: jhpy. Endpoint YouTube: youtube.youtube.video.upload. Endpoint TikTok: tiktok.tiktok.video.publish.init.
§
PIPEVIDEO_API_KEY not yet set. YouTube and TikTok OAuth not yet connected in treg.
§
Toujours déléguer le rendu vidéo à OpenCode — ne jamais lancer npm run render directement.
§
Emploi du temps: cours 8h-18h du lundi au samedi, pause 12h-14h. Fenêtres libres: soirs après 18h + pause déjeuner.
§
PC de Jean Yannick: Linux Mint 22.3 Cinnamon, session Wayland (cinnamon-wayland). `sudo` exige un mot de passe (non fournissable par l'agent) — utiliser `pkexec` avec `export WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000` pour toute action root.
§
OpenCode 1 (CLI) : /home/jhpy/.opencode/bin/opencode (pas sur PATH), installé via opencode.ai/install. OpenCode 2 (Desktop/Electron) : /opt/OpenCode/ai.opencode.desktop, .deb 'opencode' 2.1.2, MAJ via opencode.ai/update/api/latest/desktop/opencode/. DB : ~/.local/share/opencode/opencode.db. Si « Background service failed to start » / « database is locked » : tuer le process orphelin `opencode-cli serve --service`. Sur ce PC (Intel HD 4000/llvmpipe) l'app plante parfois (« GPU process isn't usable »).§
Pilotage (depuis 2026-10-23) : source unique = ~/Obsidian-Vault/Pilotage/ (00 — Index, Objectifs, Parcours — App mobile, Checklist — Play Store, Cycle 1 — Orane.d, Projets, Journal, Preuves, Revue hebdo, Carte — OS & Mobile). Objectifs : Play Store + SaaS payant d'ici avril 2027 (Orane.d C1, Scribe C3), OS long terme (nand2tetris C2). Règle Play 2026 : targetSdk 36 + 12 testeurs opt-in 14 jours avant production. Générateur : ~/.hermes/scripts/pilotage.py → ~/dashboard.html (5 écrans : Aujourd'hui/Progression/Cycle/Projets/Preuves + leçon du jour + avancement checklist Play + 30 leçons cochables regroupées par semaine et 8 barres de sections Play). Progression = cases `- [ ] N. Thème` dans la section `## Ma progression` de Parcours — App mobile.md ; CLI `--done N` / `--undone N` pour cocher et régénérer ; briefing 7 lignes. Cycle 1 (26/10→06/12) = Orane.d en test fermé Play Store + 5 étudiants ; Scribe gelé ; nand2tetris 1 soir/sem ; NIA 1 h/sem. 10 dépôts archivés sur GitHub (Content-Creator, pharmanet, portfolio, recrutement-LCU, Reloge, Site-halloween-, start-up, TexTos, Wget-manager-new, yannickhoundonou). Briefing matin = assistant-briefing.sh → pilotage.py --brief (plus de LLM, zéro token). Règles : un seul objectif par cycle, 3 actifs max, une preuve par semaine, jamais « en pause » (gelé ou archivé).
