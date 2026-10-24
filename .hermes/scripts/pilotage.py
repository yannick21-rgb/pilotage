#!/usr/bin/env python3
"""
pilotage.py — le poste de commande de Jhpy.

Une seule source de vérité : les notes Obsidian du dossier `Pilotage/`.
Ce script les lit et produit :

    1. /home/jhpy/dashboard.html   (4 écrans, lecture seule, hors ligne)
    2. un briefing Telegram de 5 lignes (--brief)

Commandes :
    python3 pilotage.py                 régénère le dashboard
    python3 pilotage.py --brief         affiche le briefing (5 lignes)
    python3 pilotage.py --check         vérifie que les notes sont cohérentes
    python3 pilotage.py --json          affiche l'état complet en JSON
    python3 pilotage.py --log "..."     ajoute une ligne au journal
    python3 pilotage.py --open          ouvre le dashboard

Le format des notes est décrit dans `Pilotage/00 — Index.md`.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

HOME = Path.home()
PILOTAGE_DIR = HOME / "Obsidian-Vault" / "Pilotage"
DASHBOARD = HOME / "dashboard.html"

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


# --------------------------------------------------------------------------
# Lecture des notes
# --------------------------------------------------------------------------

def read_note(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError as exc:
                raise SystemExit(f"Frontmatter invalide dans {path} : {exc}")
            body = parts[2]
    return meta, body


def as_date(value) -> dt.date:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    return dt.date.fromisoformat(str(value)[:10])


def date_fr(value: dt.date) -> str:
    return f"{JOURS[value.weekday()]} {value.day} {MOIS[value.month - 1]} {value.year}"


def short_date_fr(value: dt.date) -> str:
    return f"{value.day} {MOIS[value.month - 1]}"


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text)
                   if unicodedata.category(c) != "Mn").lower()


# --------------------------------------------------------------------------
# Parsing
# --------------------------------------------------------------------------

def parse_cycle() -> dict:
    notes = sorted(PILOTAGE_DIR.glob("Cycle *.md"))
    if not notes:
        raise SystemExit("Aucune note « Cycle *.md » dans Obsidian-Vault/Pilotage/")

    chosen = None
    for path in notes:
        meta, body = read_note(path)
        if str(meta.get("statut", "")).lower() == "actif":
            chosen = (path, meta, body)
    if chosen is None:
        path = notes[-1]
        meta, body = read_note(path)
        chosen = (path, meta, body)

    path, meta, body = chosen
    jalons: list[dict] = []
    current: dict | None = None

    for line in body.splitlines():
        text = line.strip()
        if text.startswith("## "):
            title = text[3:].strip()
            if strip_accents(title).startswith("jalon"):
                label = re.sub(r"^Jalon\s*\d+\s*[—–-]\s*", "", title, flags=re.I)
                current = {"titre": label.strip(), "echeance": "", "actions": []}
                jalons.append(current)
            else:
                current = None
            continue

        if current is None:
            continue

        match = re.match(r"^-\s*\[( |x|X)\]\s*(.+)$", text)
        if match:
            current["actions"].append({
                "texte": match.group(2).strip(),
                "fait": match.group(1).lower() == "x",
            })
            continue

        if "chéance" in text:
            value = text.split(":", 1)[-1].strip().strip("*").strip()
            if value:
                current["echeance"] = value

    done = sum(1 for j in jalons for a in j["actions"] if a["fait"])
    total = sum(len(j["actions"]) for j in jalons)

    next_action = None
    for jalon in jalons:
        for action in jalon["actions"]:
            if not action["fait"]:
                next_action = {"texte": action["texte"], "jalon": jalon["titre"]}
                break
        if next_action:
            break

    debut = as_date(meta["debut"])
    fin = as_date(meta["fin"])
    today = dt.date.today()
    total_days = (fin - debut).days + 1
    day = (today - debut).days + 1

    if day < 1:
        phase = "preparation"
        week = 0
    elif day > total_days:
        phase = "termine"
        week = 6
    else:
        phase = "en_cours"
        week = min(6, (day - 1) // 7 + 1)

    return {
        "fichier": str(path),
        "numero": int(meta.get("numero", 1)),
        "nom": str(meta.get("nom", path.stem)),
        "objectif": str(meta.get("objectif", "")),
        "projet": str(meta.get("projet", "")),
        "statut": str(meta.get("statut", "")),
        "debut": debut.isoformat(),
        "fin": fin.isoformat(),
        "total_jours": total_days,
        "jour": day,
        "semaine": week,
        "phase": phase,
        "jalons": jalons,
        "actions_faites": done,
        "actions_total": total,
        "avancement": round(100 * done / total) if total else 0,
        "prochaine_action": next_action,
    }


def parse_projects() -> dict:
    path = PILOTAGE_DIR / "Projets.md"
    if not path.exists():
        raise SystemExit("Note manquante : Obsidian-Vault/Pilotage/Projets.md")
    meta, body = read_note(path)

    groups: dict[str, list[dict]] = {}
    current: str | None = None

    for line in body.splitlines():
        text = line.strip()
        if text.startswith("## "):
            current = text[3:].strip()
            groups.setdefault(current, [])
            continue
        if current is None or not text.startswith("|"):
            continue

        cells = [c.strip() for c in text.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if strip_accents(cells[0]) in ("projet", "") or set(cells[0]) <= set("-: "):
            continue

        groups[current].append({
            "nom": cells[0],
            "role": cells[1] if len(cells) > 1 else "",
            "prochaine": cells[2] if len(cells) > 2 else "",
            "depot": cells[3] if len(cells) > 3 else "",
        })

    return {"maj": str(meta.get("maj", "")), "groupes": groups}


def parse_journal() -> list[dict]:
    path = PILOTAGE_DIR / "Journal.md"
    if not path.exists():
        return []
    _, body = read_note(path)
    entries = []
    for line in body.splitlines():
        match = re.match(r"^-\s*(\d{4}-\d{2}-\d{2})\s*[—–-]\s*(.+)$", line.strip())
        if match:
            entries.append({"date": match.group(1), "texte": match.group(2).strip()})
    entries.sort(key=lambda e: e["date"], reverse=True)
    return entries


def compute_streak(entries: list[dict]) -> int:
    if not entries:
        return 0
    dates = {e["date"] for e in entries}
    cursor = dt.date.today()
    if cursor.isoformat() not in dates:
        cursor -= dt.timedelta(days=1)
    streak = 0
    while cursor.isoformat() in dates:
        streak += 1
        cursor -= dt.timedelta(days=1)
    return streak


def parse_proofs() -> list[dict]:
    path = PILOTAGE_DIR / "Preuves.md"
    if not path.exists():
        return []
    _, body = read_note(path)
    proofs = []
    for line in body.splitlines():
        text = line.strip()
        if not text.startswith("|"):
            continue
        cells = [c.strip() for c in text.strip("|").split("|")]
        if len(cells) < 4:
            continue
        if strip_accents(cells[0]) in ("date", "") or set(cells[0]) <= set("-: "):
            continue
        proofs.append({
            "date": cells[0],
            "titre": cells[1],
            "lien": cells[2],
            "statut": cells[3],
            "fait": "fait" in strip_accents(cells[3]),
        })
    proofs.sort(key=lambda p: p["date"])
    return proofs


def parse_objectives() -> list[dict]:
    path = PILOTAGE_DIR / "Objectifs.md"
    if not path.exists():
        return []
    _, body = read_note(path)
    goals = []
    for line in body.splitlines():
        text = line.strip()
        if not text.startswith("|"):
            continue
        cells = [c.strip() for c in text.strip("|").split("|")]
        if len(cells) < 5:
            continue
        if strip_accents(cells[0]) in ("objectif", "") or set(cells[0]) <= set("-: "):
            continue
        goals.append({
            "objectif": cells[0],
            "horizon": cells[1],
            "preuve": cells[2],
            "cycle": cells[3],
            "statut": cells[4],
        })
    return goals


def parse_parcours() -> dict:
    path = PILOTAGE_DIR / "Parcours — App mobile.md"
    if not path.exists():
        return {"sessions": [], "total": 0, "faites": 0, "cases": 0,
                "numeros_coches": [], "pct": 0, "prochaine": None,
                "lecon": None, "termine": False}

    _, body = read_note(path)
    sessions = []
    progress: dict[int, bool] = {}

    for line in body.splitlines():
        text = line.strip()

        # Liste de progression : - [x] 12. TypeScript
        match = re.match(r"^-\s*\[( |x|X)\]\s*(\d+)\.", text)
        if match:
            progress[int(match.group(2))] = match.group(1).lower() == "x"
            continue

        if not text.startswith("|"):
            continue
        cells = [c.strip() for c in text.strip("|").split("|")]
        if len(cells) < 6:
            continue
        if not re.fullmatch(r"\d+", cells[0]):
            continue
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[1]):
            continue
        sessions.append({
            "numero": int(cells[0]),
            "date": cells[1],
            "theme": cells[2].replace("`", ""),
            "concept": cells[3].replace("`", ""),
            "exercice": cells[4].replace("`", ""),
            "preuve": cells[5].replace("`", ""),
        })
    sessions.sort(key=lambda s: s["date"])

    today = dt.date.today().isoformat()
    for session in sessions:
        session["fait"] = progress.get(session["numero"], False)
        if session["fait"]:
            session["statut"] = "fait"
        elif session["date"] == today:
            session["statut"] = "aujourdhui"
        elif session["date"] < today:
            session["statut"] = "retard"
        else:
            session["statut"] = "a_venir"

    faites = sum(1 for s in sessions if s["fait"])
    prochaine = next((s for s in sessions if not s["fait"]), None)

    return {
        "sessions": sessions,
        "total": len(sessions),
        "faites": faites,
        "cases": len(progress),
        "numeros_coches": sorted(progress),
        "pct": round(100 * faites / len(sessions)) if sessions else 0,
        "prochaine": dict(prochaine) if prochaine else None,
        "lecon": dict(prochaine) if prochaine else None,
        "termine": prochaine is None and bool(sessions),
    }


def parse_checklist() -> dict:
    path = PILOTAGE_DIR / "Checklist — Play Store.md"
    if not path.exists():
        return {"items": [], "faites": 0, "total": 0, "prochaine": None,
                "par_section": []}

    _, body = read_note(path)
    items = []
    section = ""
    for line in body.splitlines():
        text = line.strip()
        if text.startswith("## "):
            section = re.sub(r"^\d+\.\s*", "", text[3:].strip())
            continue
        match = re.match(r"^-\s*\[( |x|X)\]\s*(.+)$", text)
        if match:
            items.append({
                "section": section,
                "texte": match.group(2).strip(),
                "fait": match.group(1).lower() == "x",
            })

    faites = sum(1 for i in items if i["fait"])
    sections: dict[str, list[dict]] = {}
    for item in items:
        sections.setdefault(item["section"], []).append(item)

    current = next((name for name, entries in sections.items()
                    if any(not i["fait"] for i in entries)), None)
    current_items = sections.get(current, []) if current else []

    return {
        "items": items,
        "faites": faites,
        "total": len(items),
        "prochaine": next((i for i in items if not i["fait"]), None),
        "section_courante": current,
        "section_faites": sum(1 for i in current_items if i["fait"]),
        "section_total": len(current_items),
        "sections_total": len(sections),
        "sections_faites": sum(1 for entries in sections.values()
                               if all(i["fait"] for i in entries)),
        "par_section": [
            {"nom": name,
             "faites": sum(1 for i in entries if i["fait"]),
             "total": len(entries)}
            for name, entries in sections.items()
        ],
    }



# --------------------------------------------------------------------------
# État complet
# --------------------------------------------------------------------------

def build_state() -> dict:
    cycle = parse_cycle()
    projects = parse_projects()
    journal = parse_journal()
    proofs = parse_proofs()
    objectives = parse_objectives()
    parcours = parse_parcours()
    checklist = parse_checklist()

    next_proof = next((p for p in proofs if not p["fait"]), None)
    proofs_done = sum(1 for p in proofs if p["fait"])

    return {
        "genere": dt.datetime.now().isoformat(timespec="seconds"),
        "aujourdhui": dt.date.today().isoformat(),
        "cycle": cycle,
        "objectifs": objectives,
        "parcours": parcours,
        "checklist": checklist,
        "projets": projects,
        "journal": journal,
        "streak": compute_streak(journal),
        "preuves": proofs,
        "preuves_faites": proofs_done,
        "preuves_total": len(proofs),
        "prochaine_preuve": next_proof,
    }


# --------------------------------------------------------------------------
# Rendu HTML
# --------------------------------------------------------------------------

def e(value) -> str:
    return html.escape(str(value), quote=True)


def pill(text: str, kind: str = "") -> str:
    return f'<span class="pill {kind}">{e(text)}</span>'


def inline(text: str) -> str:
    """Échappe le texte puis transforme `code` en <code>code</code>."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", e(text))


def action_row(action: dict) -> str:
    cls = "done" if action["fait"] else ""
    mark = "✓" if action["fait"] else ""
    return (f'<li class="action {cls}"><span class="tick">{mark}</span>'
            f'<span>{inline(action["texte"])}</span></li>')


def jalon_card(jalon: dict, index: int) -> str:
    done = sum(1 for a in jalon["actions"] if a["fait"])
    total = len(jalon["actions"])
    pct = round(100 * done / total) if total else 0
    echeance = f'<span class="meta">échéance : {e(jalon["echeance"])}</span>' if jalon["echeance"] else ""
    actions = "".join(action_row(a) for a in jalon["actions"])
    return f"""
    <article class="card jalon">
      <div class="card-head">
        <span class="num">{index + 1}</span>
        <div>
          <h3>{e(jalon["titre"])}</h3>
          {echeance}
        </div>
        <span class="pill {'p-ok' if pct == 100 else 'p-must' if pct == 0 else 'p-main'}">{done}/{total}</span>
      </div>
      <div class="bar"><i style="width:{pct}%"></i></div>
      <ul class="actions">{actions}</ul>
    </article>"""


def goal_card(goal: dict) -> str:
    statut = strip_accents(goal["statut"])
    if "fait" in statut:
        kind = "p-ok"
    elif "bloc" in statut:
        kind = "p-bad"
    elif "cours" in statut:
        kind = "p-main"
    else:
        kind = "p-purple"
    return f"""
    <article class="goal">
      <div class="goal-top"><h3>{e(goal["objectif"])}</h3>{pill(goal["statut"], kind)}</div>
      <div class="goal-horizon">{e(goal["horizon"])}</div>
      <div class="goal-proof"><span class="meta">Preuve</span>{inline(goal["preuve"])}</div>
      <div class="goal-cycle">{pill(goal["cycle"], "p-dim")}</div>
    </article>"""


def project_card(project: dict) -> str:
    role = project["role"].strip()
    role_class = {"ship": "p-main", "learn": "p-purple", "argent": "p-teal", "sécurité": "p-bad"}.get(role.lower(), "p-dim")
    depot = project["depot"].strip()
    link = ""
    if depot and depot != "—":
        url = f"https://github.com/yannick21-rgb/{depot}"
        link = f'<a class="repo" href="{e(url)}">{e(depot)} ↗</a>'
    return f"""
    <article class="card project">
      <div class="head">
        <h3>{e(project["nom"])}</h3>
        {pill(role or "—", role_class)}
      </div>
      <p class="next">{inline(project["prochaine"])}</p>
      {link}
    </article>"""


def project_rows(projects: list[dict]) -> str:
    rows = ""
    for p in projects:
        depot = p["depot"].strip()
        link = (f'<a class="repo" href="https://github.com/yannick21-rgb/{e(depot)}">{e(depot)} ↗</a>'
                if depot and depot != "—" else '<span class="meta">—</span>')
        rows += (f'<tr><td><b>{e(p["nom"])}</b></td><td>{e(p["role"] or "—")}</td>'
                 f'<td>{inline(p["prochaine"] or "—")}</td><td>{link}</td></tr>')
    return rows


def proof_row(proof: dict) -> str:
    statut = pill("fait", "p-ok") if proof["fait"] else pill("attendu", "p-must")
    lien = proof["lien"].strip()
    if lien and lien != "—":
        link = f'<a class="repo" href="{e(lien)}">ouvrir ↗</a>'
    else:
        link = '<span class="meta">—</span>'
    return (f'<tr><td class="mono">{e(proof["date"])}</td><td>{inline(proof["titre"])}</td>'
            f'<td>{link}</td><td>{statut}</td></tr>')


def render_dashboard(state: dict) -> str:
    cycle = state["cycle"]
    today = dt.date.fromisoformat(state["aujourdhui"])
    journal = state["journal"][:4]

    if cycle["phase"] == "preparation":
        jrs = (dt.date.fromisoformat(cycle["debut"]) - today).days
        phase_label = f"préparation · J-{jrs}"
        phase_class = "p-warn"
    elif cycle["phase"] == "termine":
        phase_label = "cycle terminé"
        phase_class = "p-purple"
    else:
        phase_label = f"jour {cycle['jour']}/{cycle['total_jours']} · semaine {cycle['semaine']}/6"
        phase_class = "p-main"

    next_action = cycle["prochaine_action"]
    if next_action:
        next_html = f"""
        <div class="hero-label">La seule action maintenant</div>
        <h2 class="hero-action">{inline(next_action["texte"])}</h2>
        <div class="hero-meta">{pill(cycle["projet"], "p-main")} <span class="meta">dans « {e(next_action["jalon"])} »</span></div>"""
    else:
        next_html = f"""
        <div class="hero-label">Cycle terminé</div>
        <h2 class="hero-action">Faire la rétro et choisir le cycle 2</h2>
        <div class="hero-meta">{pill(cycle["projet"], "p-purple")}</div>"""

    next_proof = state["prochaine_preuve"]
    if next_proof:
        proof_html = f'<b>{e(next_proof["titre"])}</b><br><span class="meta">prévue le {e(next_proof["date"])}</span>'
    else:
        proof_html = '<b>Toutes les preuves du cycle sont faites.</b><br><span class="meta">Il reste la démo finale.</span>'

    journal_html = ""
    for entry in journal:
        journal_html += f'<li><span class="mono">{e(entry["date"])}</span> {e(entry["texte"])}</li>'
    if not journal_html:
        journal_html = '<li class="meta">Rien encore. Une ligne ce soir suffit.</li>'

    jalons_html = "".join(jalon_card(j, i) for i, j in enumerate(cycle["jalons"]))
    groups = state["projets"]["groupes"]
    actifs = groups.get("Actifs", [])
    geles = groups.get("Gelés", [])
    archives = groups.get("Archivés", [])
    outils = groups.get("Outils", [])

    actifs_html = "".join(project_card(p) for p in actifs)

    proofs_html = "".join(proof_row(p) for p in state["preuves"])
    proof_pct = round(100 * state["preuves_faites"] / state["preuves_total"]) if state["preuves_total"] else 0

    goals = state["objectifs"]
    goals_html = "".join(goal_card(g) for g in goals)
    cap_goal = next((g for g in goals if f"cycle {cycle['numero']}" in strip_accents(g["cycle"])), None)
    cap_pill = (pill(f"cap : {cap_goal['objectif'].split(' — ')[0]}", "p-teal")
                if cap_goal else "")

    parcours = state["parcours"]
    lesson = parcours["lecon"]
    lesson_block = ""
    if lesson:
        statut_txt = {
            "aujourdhui": "aujourd'hui",
            "retard": "en retard",
            "a_venir": "à venir",
        }.get(lesson["statut"], "à venir")
        lesson_kind = {
            "aujourdhui": "p-teal",
            "retard": "p-warn",
        }.get(lesson["statut"], "p-dim")
        lesson_block = f"""
    <div class="sec-title"><h2>La leçon du jour</h2><span class="line"></span><span class="meta">{parcours["faites"]}/{parcours["total"]} terminées · 45 min</span></div>
    <article class="lesson">
      <div class="lesson-main">
        <div class="lesson-head">
          <span class="meta">Leçon {lesson["numero"]}/{parcours["total"]} · {e(short_date_fr(dt.date.fromisoformat(lesson["date"])))}</span>
          {pill(statut_txt, lesson_kind)}
        </div>
        <h3>{e(lesson["theme"])}</h3>
        <p>{e(lesson["concept"])}</p>
        <div class="bar"><i style="width:{parcours["pct"]}%"></i></div>
      </div>
      <div class="lesson-right">
        <span class="meta">À appliquer dans Orane.d</span>
        <p>{e(lesson["exercice"])}</p>
        <span class="pill p-dim">preuve : {e(lesson["preuve"])}</span>
      </div>
    </article>"""
    elif parcours["termine"]:
        lesson_block = f"""
    <div class="sec-title"><h2>Parcours</h2><span class="line"></span><span class="meta">{parcours["total"]}/{parcours["total"]} terminées</span></div>
    <div class="box"><b>Les 30 leçons sont faites.</b> Le parcours est terminé. La suite : cycle 2, nand2tetris et la demande de production Play Store.</div>"""

    checklist = state["checklist"]
    checklist_block = ""
    if checklist["total"]:
        if checklist["section_courante"]:
            section_pct = round(100 * checklist["section_faites"] / max(1, checklist["section_total"]))
            section_titre = checklist["section_courante"]
            section_score = f"{checklist['section_faites']}/{checklist['section_total']}"
            next_check = checklist["prochaine"]["texte"] if checklist["prochaine"] else "tout est coché"
        else:
            section_pct = 100
            section_titre = "Checklist terminée"
            section_score = "100 %"
            next_check = "tout est coché"
        checklist_block = f"""
    <div class="sec-title"><h2>Play Store</h2><span class="line"></span><span class="meta">la partie non-code</span></div>
    <div class="objective small">
      <span class="meta">Section en cours</span>
      <h2>{e(section_titre)} · {section_score}</h2>
      <div class="bar big"><i style="width:{section_pct}%"></i></div>
      <p class="meta">Prochain : {e(next_check)}</p>
      <p class="meta">Global : {checklist["faites"]}/{checklist["total"]} points · {checklist["sections_faites"]}/{checklist["sections_total"]} sections</p>
    </div>"""

    # Onglet Progression : les 30 leçons groupées par semaine + les 8 sections Play Store.
    debut = dt.date.fromisoformat(cycle["debut"])
    groups: dict[int, list[dict]] = {}
    for session in parcours["sessions"]:
        jour = dt.date.fromisoformat(session["date"])
        semaine = max(1, min(6, ((jour - debut).days // 7) + 1))
        groups.setdefault(semaine, []).append(session)

    prochaine_num = parcours["prochaine"]["numero"] if parcours["prochaine"] else None
    weeks_html = ""
    for semaine in sorted(groups):
        entries = groups[semaine]
        faites_semaine = sum(1 for s in entries if s["fait"])
        bornes = (f"{short_date_fr(dt.date.fromisoformat(entries[0]['date']))} → "
                  f"{short_date_fr(dt.date.fromisoformat(entries[-1]['date']))}")
        ouvert = " open" if any(s["numero"] == prochaine_num for s in entries) else ""
        items_html = ""
        for session in entries:
            if session["numero"] == prochaine_num:
                marque = pill("prochaine", "p-teal")
            elif session["statut"] == "retard":
                marque = pill("en retard", "p-warn")
            elif session["fait"]:
                marque = pill("fait", "p-ok")
            else:
                marque = ""
            coche = "✓" if session["fait"] else ""
            classes = "item done" if session["fait"] else (
                "item next" if session["numero"] == prochaine_num else "item")
            items_html += f"""
        <div class="{classes}">
          <span class="tick">{coche}</span>
          <div class="item-body">
            <div class="item-title"><b>{session["numero"]} · {e(session["theme"])}</b><span class="meta">{e(short_date_fr(dt.date.fromisoformat(session["date"])))}</span>{marque}</div>
            <p>{e(session["concept"])}</p>
            <p class="proof">Exercice : {e(session["exercice"])}<br>Preuve : {e(session["preuve"])}</p>
          </div>
        </div>"""
        weeks_html += f"""
      <details class="week"{ouvert}>
        <summary><b>Semaine {semaine}</b><span class="meta">{faites_semaine}/{len(entries)} · {bornes}</span></summary>
        <div class="week-body">{items_html}
        </div>
      </details>"""

    sections_html = ""
    for section in checklist["par_section"]:
        pct_section = round(100 * section["faites"] / max(1, section["total"]))
        sections_html += f"""
      <div class="section-row">
        <div class="section-head"><b>{e(section["nom"])}</b><span class="meta">{section["faites"]}/{section["total"]}</span></div>
        <div class="bar"><i style="width:{pct_section}%"></i></div>
      </div>"""

    if parcours["prochaine"]:
        prochaine_txt = (f"prochaine : leçon {parcours['prochaine']['numero']} · "
                         f"{short_date_fr(dt.date.fromisoformat(parcours['prochaine']['date']))}")
    else:
        prochaine_txt = "parcours terminé"

    progression_html = f"""
  <section id="tab-progression" class="hidden">
    <div class="objective">
      <span class="meta">Parcours — App mobile · 6 semaines</span>
      <h2>{parcours["faites"]}/{parcours["total"]} leçons terminées · {parcours["pct"]}%</h2>
      <div class="bar big"><i style="width:{parcours["pct"]}%"></i></div>
      <div class="objective-meta">
        <span>{checklist["faites"]}/{checklist["total"]} points Play Store</span>
        <span>{state["preuves_faites"]}/{state["preuves_total"]} preuves</span>
        <span>{prochaine_txt}</span>
      </div>
    </div>

    <div class="sec-title"><h2>Les 30 leçons</h2><span class="line"></span><span class="meta">coche dans Obsidian, puis régénère</span></div>
    <div class="weeks">{weeks_html}
    </div>

    <div class="sec-title"><h2>Play Store</h2><span class="line"></span><span class="meta">les 8 sections de la checklist</span></div>
    <div class="sections">{sections_html}
    </div>

    <div class="box">
      <b>La progression se coche, elle ne se date pas.</b> Une leçon est terminée quand sa preuve existe. Si tu prends du retard, la leçon reste la prochaine — tu ne sautes pas.
    </div>
  </section>
"""

    semaine_note = ""
    if cycle["phase"] == "preparation":
        semaine_note = (f"Le cycle démarre le <b>{e(date_fr(dt.date.fromisoformat(cycle['debut'])))}</b>. "
                        "Cette semaine sert à fermer proprement ce qui traîne.")
    elif cycle["phase"] == "termine":
        semaine_note = "Le cycle est fini. Décision : passage en production ou deuxième cycle de correction."
    else:
        semaine_note = (f"Semaine <b>{cycle['semaine']}/6</b> du cycle. "
                        "La preuve de la semaine est due dimanche.")

    if cycle["phase"] == "preparation":
        cycle_kpi = f"J-{(dt.date.fromisoformat(cycle['debut']) - today).days}"
        cycle_hint = "avant le départ"
        week_pill = "avant-cycle"
    elif cycle["phase"] == "termine":
        cycle_kpi = "fini"
        cycle_hint = "à clôturer"
        week_pill = "cycle fini"
    else:
        cycle_kpi = f"{cycle['jour']}/{cycle['total_jours']}"
        cycle_hint = "jours écoulés"
        week_pill = f"semaine {cycle['semaine']}/6"

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pilotage — Jhpy</title>
<style>{CSS}</style>
</head>
<body>
<header class="top">
  <div class="brand">
    <h1>Pilotage <span>· Jhpy</span></h1>
    <div class="sub">{e(date_fr(today))} · Cycle {cycle["numero"]} · {e(cycle["nom"])}</div>
  </div>
  <div class="head-right">
    {pill(phase_label, phase_class)}
    {pill(f"streak {state['streak']} j", "p-teal" if state["streak"] >= 2 else "p-dim")}
  </div>
</header>

<nav class="tabs">
  <button class="on" data-tab="aujourdhui">Aujourd'hui</button>
  <button data-tab="progression">Progression</button>
  <button data-tab="cycle">Cycle</button>
  <button data-tab="projets">Projets</button>
  <button data-tab="preuves">Preuves</button>
</nav>

<main>
  <section id="tab-aujourdhui">
    <div class="hero">
      {next_html}
      <div class="bar big"><i style="width:{cycle["avancement"]}%"></i></div>
      <div class="hero-bottom">
        <span><b>{cycle["actions_faites"]}/{cycle["actions_total"]}</b> actions</span>
        <span><b>{state["preuves_faites"]}/{state["preuves_total"]}</b> preuves</span>
        <span><b>{parcours["faites"]}/{parcours["total"]}</b> leçons</span>
        <span class="meta">{e(cycle["objectif"])}</span>
      </div>
    </div>

    <div class="kpis">
      <div class="kpi"><div class="lbl">Avancement</div><div class="val">{cycle["avancement"]}%</div><div class="hint">{cycle["actions_faites"]} / {cycle["actions_total"]} actions</div></div>
      <div class="kpi"><div class="lbl">Preuves</div><div class="val">{state["preuves_faites"]}/{state["preuves_total"]}</div><div class="hint">choses montrables</div></div>
      <div class="kpi"><div class="lbl">Leçons</div><div class="val">{parcours["faites"]}/{parcours["total"]}</div><div class="hint">parcours app mobile</div></div>
      <div class="kpi"><div class="lbl">Streak</div><div class="val">{state["streak"]} j</div><div class="hint">jours au journal</div></div>
      <div class="kpi"><div class="lbl">Cycle</div><div class="val">{cycle_kpi}</div><div class="hint">{cycle_hint}</div></div>
    </div>

    <div class="sec-title"><h2>Le cap</h2><span class="line"></span><span class="meta">pourquoi tu fais ça</span></div>
    <div class="goals">{goals_html}</div>

    {lesson_block}

    <div class="cols">
      <article class="card">
        <div class="card-head"><h3>Cette semaine</h3>{pill(week_pill, "p-dim")}</div>
        <p class="week-note">{semaine_note}</p>
        <div class="week-proof"><span class="meta">Preuve attendue</span>{proof_html}</div>
        <div class="slots">
          <span>{pill("mardi · nand2tetris", "p-purple")}</span>
          <span>{pill("jeudi · NIA", "p-teal")}</span>
          <span>{pill("dimanche · revue", "p-dim")}</span>
        </div>
      </article>

      <article class="card">
        <div class="card-head"><h3>Journal</h3><span class="meta">3 lignes par soir</span></div>
        <ul class="journal">{journal_html}</ul>
      </article>
    </div>

    <div class="box">
      <b>La règle :</b> une action, un commit, une ligne. Une semaine sans preuve est une semaine ratée, même avec 20 commits.
    </div>
  </section>

  {progression_html}

  <section id="tab-cycle" class="hidden">
    <div class="objective">
      <span class="meta">Objectif du cycle {cycle["numero"]}</span>
      <h2>{e(cycle["objectif"])}</h2>
      <div class="objective-meta">
        <span>{e(short_date_fr(dt.date.fromisoformat(cycle["debut"])))} → {e(short_date_fr(dt.date.fromisoformat(cycle["fin"])))}</span>
        <span>{cycle["actions_faites"]}/{cycle["actions_total"]} actions · {cycle["avancement"]}%</span>
        {cap_pill}
      </div>
      <div class="bar big"><i style="width:{cycle["avancement"]}%"></i></div>
    </div>
    <div class="grid3">{jalons_html}</div>
    {checklist_block}
    <div class="box">
      <b>Périmètre variable, date fixe.</b> Si tu es en retard au jalon 2, tu réduis le contenu — tu ne décales pas la fin du cycle.
    </div>
  </section>

  <section id="tab-projets" class="hidden">
    <div class="sec-title"><h2>Actifs</h2><span class="line"></span><span class="meta">3 maximum</span></div>
    <div class="grid3">{actifs_html}</div>

    <div class="sec-title"><h2>Gelés</h2><span class="line"></span><span class="meta">on n'y touche pas avant la fin du cycle</span></div>
    <table class="tbl">
      <thead><tr><th>Projet</th><th>Rôle</th><th>Prochaine action</th><th>Dépôt</th></tr></thead>
      <tbody>{project_rows(geles)}</tbody>
    </table>

    <div class="sec-title"><h2>Outils</h2><span class="line"></span></div>
    <table class="tbl">
      <thead><tr><th>Projet</th><th>Rôle</th><th>Prochaine action</th><th>Dépôt</th></tr></thead>
      <tbody>{project_rows(outils)}</tbody>
    </table>

    <div class="sec-title"><h2>Archivés</h2><span class="line"></span><span class="meta">{len(archives)} dépôts · réversible</span></div>
    <table class="tbl muted">
      <thead><tr><th>Projet</th><th>Rôle</th><th>Prochaine action</th><th>Dépôt</th></tr></thead>
      <tbody>{project_rows(archives)}</tbody>
    </table>
  </section>

  <section id="tab-preuves" class="hidden">
    <div class="objective small">
      <span class="meta">Ce qui existe et qu'on peut montrer</span>
      <h2>{state["preuves_faites"]} preuves faites sur {state["preuves_total"]}</h2>
      <div class="bar big"><i style="width:{proof_pct}%"></i></div>
    </div>
    <table class="tbl">
      <thead><tr><th>Date</th><th>Preuve</th><th>Lien</th><th>Statut</th></tr></thead>
      <tbody>{proofs_html}</tbody>
    </table>
    <div class="box">
      <b>La preuve est la seule mesure qui compte.</b> Un commit invisible ne compte pas. Une capture, une vidéo, un lien, un testeur qui a installé l'app : oui.
    </div>
  </section>
</main>

<footer>
  Source : <span class="mono">Obsidian-Vault/Pilotage/</span> · généré le {e(state["genere"].replace("T", " à "))}
  · <span class="mono">python3 ~/.hermes/scripts/pilotage.py</span>
</footer>

<script>{JS}</script>
</body>
</html>
"""


CSS = """
:root{
  --bg:#0b0e13; --panel:#131820; --panel2:#1a212c; --line:#273041;
  --txt:#e6edf3; --dim:#8b949e; --accent:#4f9cf9; --teal:#2dd4bf;
  --warn:#f0b34a; --bad:#f26868; --ok:#4ade80; --purple:#a78bfa; --pink:#f472b6;
  --ease-out:cubic-bezier(.23,1,.32,1); --ease-in-out:cubic-bezier(.77,0,.175,1);
}
@keyframes fade-up{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@media(prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
  --r:14px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:14px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1100px;margin:0 auto}
header.top{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;max-width:1100px;margin:0 auto;padding:22px 20px 10px}
.brand h1{font-size:1.3rem;letter-spacing:-.02em;font-weight:700}
.brand h1 span{color:var(--dim);font-weight:500}
.brand .sub{font-size:.76rem;color:var(--dim);margin-top:3px}
.head-right{display:flex;gap:8px;flex-wrap:wrap}
.pill{display:inline-block;font-size:.68rem;font-weight:600;padding:3px 9px;border-radius:99px;border:1px solid var(--line);background:var(--panel2);color:var(--dim);white-space:nowrap}
.p-main{background:rgba(79,156,249,.14);border-color:rgba(79,156,249,.35);color:#8fc0fb}
.p-teal{background:rgba(45,212,191,.12);border-color:rgba(45,212,191,.35);color:#5eead4}
.p-purple{background:rgba(167,139,250,.13);border-color:rgba(167,139,250,.35);color:#c4b5fd}
.p-ok{background:rgba(74,222,128,.12);border-color:rgba(74,222,128,.35);color:#86efac}
.p-must{background:rgba(242,104,104,.12);border-color:rgba(242,104,104,.35);color:#fca5a5}
.p-warn{background:rgba(240,179,74,.12);border-color:rgba(240,179,74,.35);color:#fcd34d}
.p-dim{background:var(--panel2);border-color:var(--line);color:var(--dim)}
nav.tabs{display:flex;gap:6px;max-width:1100px;margin:14px auto 20px;padding:0 20px;flex-wrap:wrap}
nav.tabs button{font:inherit;font-size:.78rem;font-weight:600;padding:8px 14px;border-radius:9px;border:1px solid var(--line);background:var(--panel);color:var(--dim);cursor:pointer;transition:color .18s var(--ease-out),background .18s var(--ease-out),border-color .18s var(--ease-out),transform .12s var(--ease-out)}
nav.tabs button:hover{color:var(--txt);border-color:#3a465c}
nav.tabs button:active{transform:scale(.97)}
nav.tabs button.on{background:var(--accent);border-color:var(--accent);color:#fff}
main{max-width:1100px;margin:0 auto;padding:0 20px 60px}
.hidden{display:none}
.hero{background:linear-gradient(160deg,#16202e,#121821 60%);border:1px solid var(--line);border-radius:var(--r);padding:26px 26px 20px;margin-bottom:16px;animation:fade-up .32s var(--ease-out) both}
.hero-label{font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:var(--accent);font-weight:700}
.hero-action{font-size:1.65rem;line-height:1.25;letter-spacing:-.02em;margin:10px 0 12px;max-width:820px}
.hero-meta{display:flex;align-items:center;gap:9px;flex-wrap:wrap;margin-bottom:18px}
.hero-bottom{display:flex;gap:20px;flex-wrap:wrap;align-items:baseline;font-size:.78rem;color:var(--dim);margin-top:9px}
.hero-bottom b{color:var(--txt)}
.bar{height:7px;background:#0a0d12;border-radius:99px;overflow:hidden;border:1px solid #1e2735;margin:10px 0}
.bar.big{height:9px;margin:0}
.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--accent),var(--teal));border-radius:99px;transition:width .4s var(--ease-out)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-bottom:16px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;animation:fade-up .32s var(--ease-out) both}
.kpi .lbl{font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:var(--dim)}
.kpi .val{font-size:1.55rem;font-weight:700;letter-spacing:-.02em;margin:4px 0 0}
.kpi .hint{font-size:.68rem;color:var(--dim)}
.goals{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}
.goal{background:linear-gradient(160deg,#141b25,#111720);border:1px solid var(--line);border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:7px;animation:fade-up .32s var(--ease-out) both}
.goal-top{display:flex;justify-content:space-between;align-items:flex-start;gap:6px}
.goal h3{font-size:.84rem;letter-spacing:-.01em;line-height:1.3}
.goal-horizon{font-size:.68rem;color:var(--teal);font-weight:650}
.goal-proof{font-size:.72rem;color:var(--dim);line-height:1.45}
.goal-proof .meta{display:block;font-size:.56rem;text-transform:uppercase;letter-spacing:.08em;color:#5b6675;margin-bottom:2px}
.goal-cycle{margin-top:auto}
.lesson{display:grid;grid-template-columns:1.15fr .85fr;gap:18px;background:linear-gradient(160deg,#131c28,#111720);border:1px solid var(--line);border-left:3px solid var(--teal);border-radius:12px;padding:16px 18px;margin-bottom:16px;animation:fade-up .32s var(--ease-out) both}
.lesson-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px}
.lesson h3{font-size:1rem;letter-spacing:-.01em;margin:2px 0 4px}
.lesson p{font-size:.8rem;color:var(--dim);line-height:1.55}
.lesson-right{border-left:1px solid var(--line);padding-left:18px;display:flex;flex-direction:column;gap:6px}
.lesson-right .pill{align-self:flex-start;margin-top:auto;white-space:normal}
@media (max-width:860px){
  .lesson{grid-template-columns:1fr}
  .lesson-right{border-left:0;border-top:1px solid var(--line);padding-left:0;padding-top:12px}
}
.cols{display:grid;grid-template-columns:1.1fr .9fr;gap:12px;margin-bottom:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;animation:fade-up .32s var(--ease-out) both}
.card-head{display:flex;align-items:flex-start;gap:10px;justify-content:space-between;margin-bottom:8px}
.card-head h3{font-size:.95rem;font-weight:650;letter-spacing:-.01em}
.card .meta{font-size:.72rem;color:var(--dim)}
.week-note{font-size:.8rem;color:var(--dim);margin:6px 0 12px}
.week-note b{color:var(--txt)}
.week-proof{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:12px;font-size:.82rem}
.week-proof .meta{display:block;text-transform:uppercase;letter-spacing:.08em;font-size:.62rem;margin-bottom:5px}
.slots{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px}
.journal{list-style:none;display:flex;flex-direction:column;gap:9px}
.journal li{font-size:.78rem;color:#c9d1d9;padding-left:10px;border-left:2px solid #223047}
.journal .mono{display:block;font-size:.64rem;color:var(--dim);margin-bottom:1px}
.box{background:var(--panel2);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:12px 14px;font-size:.78rem;color:var(--dim);margin-top:16px}
.box b{color:var(--txt)}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.jalon .num{width:26px;height:26px;border-radius:8px;background:var(--panel2);border:1px solid var(--line);display:grid;place-items:center;font-size:.75rem;font-weight:700;color:var(--accent);flex:none}
.jalon h3{font-size:.86rem}
.actions{list-style:none;display:flex;flex-direction:column;gap:6px;margin-top:10px}
.action{display:flex;gap:8px;font-size:.78rem;color:#c9d1d9;align-items:flex-start}
.action .tick{width:16px;height:16px;border-radius:5px;border:1px solid #33405a;flex:none;display:grid;place-items:center;font-size:.6rem;margin-top:1px;color:transparent}
.action.done{color:var(--dim);text-decoration:line-through}
.action.done .tick{background:rgba(74,222,128,.15);border-color:rgba(74,222,128,.5);color:#86efac}
.objective{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:22px 24px;margin-bottom:16px}
.objective.small{padding:16px 18px}
.objective .meta{font-size:.66rem;text-transform:uppercase;letter-spacing:.1em;color:var(--dim)}
.objective h2{font-size:1.35rem;line-height:1.3;letter-spacing:-.02em;margin:7px 0 10px}
.objective.small h2{font-size:1.05rem}
.objective-meta{display:flex;gap:18px;flex-wrap:wrap;font-size:.74rem;color:var(--dim);margin-bottom:4px}
.sec-title{display:flex;align-items:center;gap:12px;margin:24px 0 12px}
.sec-title h2{font-size:1rem;letter-spacing:-.01em;white-space:nowrap}
.sec-title .line{flex:1;height:1px;background:var(--line)}
.weeks{display:flex;flex-direction:column;gap:10px;margin-bottom:16px}
details.week{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
details.week summary{cursor:pointer;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px;font-size:.8rem;font-weight:600;list-style:none}
details.week summary::-webkit-details-marker{display:none}
details.week summary:hover{background:var(--panel2)}
details.week summary .meta{font-weight:400}
.week-body{padding:0 16px 12px}
.item{display:flex;gap:12px;padding:10px 0;border-top:1px solid #1e2735}
.item:first-child{border-top:0}
.tick{width:20px;height:20px;border-radius:50%;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-size:.65rem;color:var(--dim);flex:0 0 auto;margin-top:2px}
.item.done .tick{background:rgba(74,222,128,.15);border-color:rgba(74,222,128,.45);color:#86efac}
.item.done .item-title b{text-decoration:line-through;color:var(--dim)}
.item-body{min-width:0;flex:1}
.item-title{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.item-title b{font-size:.8rem}
.item-title .meta{font-size:.66rem}
.item p{font-size:.74rem;color:var(--dim);line-height:1.5;margin-top:2px}
.item p.proof{font-size:.66rem;color:#5b6675}
.item.next{background:rgba(45,212,191,.05);border-left:2px solid var(--teal);padding-left:10px;margin-left:-12px}
.sections{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:16px}
.section-row{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.section-head{display:flex;justify-content:space-between;gap:8px;font-size:.76rem}
.section-row .bar{margin:8px 0 0}
@media(max-width:860px){.sections{grid-template-columns:1fr}}
.project .head{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:8px}
.project h3{font-size:.95rem}
.project .next{font-size:.8rem;color:#c9d1d9;margin-bottom:10px}
.repo{font-size:.72rem;color:var(--accent);text-decoration:none}
.repo:hover{text-decoration:underline}
.tbl{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:.78rem}
.tbl th{text-align:left;font-size:.64rem;text-transform:uppercase;letter-spacing:.08em;color:var(--dim);padding:10px 14px;background:var(--panel2);border-bottom:1px solid var(--line)}
.tbl td{padding:10px 14px;border-bottom:1px solid #1b2331;color:#c9d1d9;vertical-align:top}
.tbl tr:last-child td{border-bottom:none}
.tbl tr:hover td{background:#161d28}
.tbl.muted td{color:#7d8794}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.72rem}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;background:#0a0d12;border:1px solid #1e2735;border-radius:4px;padding:1px 4px;color:#9fb3c8}
footer{max-width:1100px;margin:0 auto;padding:20px;font-size:.68rem;color:#5b6675;border-top:1px solid #1b2331}
@media (max-width:860px){
  .kpis{grid-template-columns:repeat(2,1fr)}
  .goals{grid-template-columns:repeat(2,1fr)}
  .cols,.grid3{grid-template-columns:1fr}
  .hero-action{font-size:1.3rem}
}
"""

JS = """
document.querySelectorAll("nav.tabs button").forEach(function (b) {
  b.addEventListener("click", function () {
    document.querySelectorAll("nav.tabs button").forEach(function (x) { x.classList.remove("on"); });
    b.classList.add("on");
    document.querySelectorAll("main > section").forEach(function (s) {
      s.classList.toggle("hidden", s.id !== "tab-" + b.dataset.tab);
    });
  });
});
"""


# --------------------------------------------------------------------------
# Briefing + CLI
# --------------------------------------------------------------------------

def goal_short(goal: dict) -> str:
    name = goal["objectif"].split(" — ")[0]
    match = re.search(r"(\d+)", goal["cycle"])
    when = f"C{match.group(1)}" if match else "continu"
    return f"{name} ({when})"


def render_brief(state: dict) -> str:
    cycle = state["cycle"]
    today = dt.date.fromisoformat(state["aujourdhui"])

    if cycle["phase"] == "preparation":
        jours = (dt.date.fromisoformat(cycle["debut"]) - today).days
        entete = f"préparation (J-{jours})"
    elif cycle["phase"] == "termine":
        entete = "cycle terminé"
    else:
        entete = f"jour {cycle['jour']}/{cycle['total_jours']} · semaine {cycle['semaine']}/6"

    action = cycle["prochaine_action"]
    action_txt = action["texte"] if action else "faire la rétro et choisir le cycle 2"

    proof = state["prochaine_preuve"]
    proof_txt = f"{proof['titre']} ({proof['date']})" if proof else "toutes les preuves sont faites"

    lesson = state["parcours"]["lecon"]
    if lesson:
        label = {
            "aujourdhui": "Ce soir",
            "retard": "En retard",
            "a_venir": "À venir",
        }.get(lesson["statut"], "À venir")
        lesson_txt = (f"{label} · leçon {lesson['numero']}/{state['parcours']['total']} · "
                      f"{lesson['theme']} — {lesson['concept']}")
        if len(lesson_txt) > 95:
            lesson_txt = lesson_txt[:92].rstrip() + "…"
        lesson_line = f"📚 {lesson_txt}"
    else:
        lesson_line = "📚 Parcours terminé"

    return "\n".join([
        f"🎯 Cycle {cycle['numero']} · {cycle['nom']} — {entete}",
        f"🧭 Cap : {' · '.join(goal_short(g) for g in state['objectifs']) or 'à définir'}",
        lesson_line,
        f"Objectif : {cycle['objectif']}",
        f"▶ Prochaine action : {action_txt}",
        f"📊 {cycle['actions_faites']}/{cycle['actions_total']} actions · "
        f"{state['preuves_faites']}/{state['preuves_total']} preuves · streak {state['streak']} j",
        f"📦 Preuve attendue : {proof_txt}",
    ])


def cmd_check(state: dict) -> int:
    problems = []
    cycle = state["cycle"]

    if cycle["actions_total"] == 0:
        problems.append(f"Aucune action trouvée dans {cycle['fichier']}")
    if not cycle["prochaine_action"] and cycle["phase"] != "termine":
        problems.append("Aucune prochaine action : toutes les actions sont cochées alors que le cycle court encore")
    if cycle["jour"] > cycle["total_jours"]:
        problems.append("Les dates du cycle sont dépassées : mettre le statut à « termine » et créer le cycle suivant")

    actifs = state["projets"]["groupes"].get("Actifs", [])
    if len(actifs) > 3:
        problems.append(f"{len(actifs)} projets actifs : la limite est 3")

    for p in actifs:
        if not p["prochaine"] or p["prochaine"] == "—":
            problems.append(f"Le projet actif « {p['nom']} » n'a pas de prochaine action")

    print(f"Cycle {cycle['numero']} — {cycle['nom']} : {cycle['actions_faites']}/{cycle['actions_total']} actions, "
          f"{len(cycle['jalons'])} jalons, phase {cycle['phase']}")
    print(f"Projets : {len(actifs)} actifs, {len(state['projets']['groupes'].get('Gelés', []))} gelés, "
          f"{len(state['projets']['groupes'].get('Archivés', []))} archivés")
    print(f"Journal : {len(state['journal'])} entrées, streak {state['streak']} j")
    print(f"Preuves : {state['preuves_faites']}/{state['preuves_total']} faites")

    parcours = state["parcours"]
    if parcours["total"]:
        lecon = parcours["lecon"]
        print(f"Parcours : {parcours['total']} leçons, {parcours['faites']} terminées, "
              f"prochaine {lecon['numero'] if lecon else '—'}")
        if parcours["sessions"] and parcours["sessions"][0]["date"] != cycle["debut"]:
            problems.append("Parcours : la première leçon ne commence pas au début du cycle")
        if parcours["total"] != 30:
            problems.append(f"Parcours : {parcours['total']} leçons au lieu de 30")
        if parcours.get("cases", 0) != parcours["total"]:
            problems.append(f"Parcours : {parcours.get('cases', 0)} cases de progression "
                            f"pour {parcours['total']} leçons (section « Ma progression »)")
        if set(parcours.get("numeros_coches", [])) != {s["numero"] for s in parcours["sessions"]}:
            problems.append("Parcours : les numéros de « Ma progression » ne correspondent pas au tableau")
        for session in parcours["sessions"]:
            if dt.date.fromisoformat(session["date"]).weekday() >= 5:
                problems.append(f"Parcours : leçon {session['numero']} tombe un week-end ({session['date']})")
    else:
        problems.append("Parcours — App mobile.md absent ou vide")

    if state["checklist"]["total"]:
        checklist = state["checklist"]
        print(f"Play Store : {checklist['faites']}/{checklist['total']} points, "
              f"section {checklist['section_courante'] or 'terminée'} "
              f"{checklist['section_faites']}/{checklist['section_total']}")
    else:
        problems.append("Checklist — Play Store.md absente ou vide")

    if problems:
        print("\nProblèmes :")
        for problem in problems:
            print("  - " + problem)
        return 1
    print("\nTout est cohérent.")
    return 0


def cmd_mark(numero: int, done: bool) -> int:
    path = PILOTAGE_DIR / "Parcours — App mobile.md"
    if not path.exists():
        print("Note manquante : " + str(path))
        return 1
    lines = path.read_text(encoding="utf-8").splitlines()
    pattern = re.compile(r"^(\s*-\s*\[)( |x|X)(\]\s*" + str(numero) + r"\.)")
    marker = "x" if done else " "
    for index, line in enumerate(lines):
        if pattern.match(line):
            lines[index] = pattern.sub(lambda m: m.group(1) + marker + m.group(3),
                                       line, count=1)
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"Leçon {numero} : {'terminée' if done else 'à refaire'}.")
            return 0
    print(f"Leçon {numero} introuvable dans « Ma progression ».")
    return 1


def cmd_log(arg: str) -> int:
    path = PILOTAGE_DIR / "Journal.md"
    today = dt.date.today().isoformat()
    parts = [p.strip() for p in arg.split("|") if p.strip()]
    if len(parts) >= 2:
        projet = parts[0]
        reste = " | ".join(parts[1:])
        line = f"- {today} — {projet} — {reste}"
    else:
        line = f"- {today} — {arg.strip()}"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print("Journal : " + line)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Pilotage — dashboard + briefing")
    parser.add_argument("--brief", action="store_true", help="affiche le briefing de 7 lignes")
    parser.add_argument("--check", action="store_true", help="vérifie la cohérence des notes")
    parser.add_argument("--json", action="store_true", help="affiche l'état en JSON")
    parser.add_argument("--log", metavar="TEXTE", help="ajoute une ligne au journal du jour")
    parser.add_argument("--done", type=int, metavar="N", help="marque la leçon N comme terminée")
    parser.add_argument("--undone", type=int, metavar="N", help="remet la leçon N à faire")
    parser.add_argument("--open", action="store_true", help="ouvre le dashboard")
    args = parser.parse_args()

    if not PILOTAGE_DIR.exists():
        raise SystemExit(f"Dossier introuvable : {PILOTAGE_DIR}")

    if args.done is not None:
        code = cmd_mark(args.done, True)
        if code:
            return code
    if args.undone is not None:
        code = cmd_mark(args.undone, False)
        if code:
            return code

    if args.log:
        return cmd_log(args.log)

    state = build_state()

    if args.json:
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0

    if args.check:
        return cmd_check(state)

    if args.brief:
        print(render_brief(state))
        return 0

    DASHBOARD.write_text(render_dashboard(state), encoding="utf-8")
    print(f"Dashboard régénéré : {DASHBOARD}")

    if args.open:
        import subprocess
        subprocess.Popen(["xdg-open", str(DASHBOARD)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
