from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Sequence


SCHEMA = "notation-collision-report/v1"
TEXT_SUFFIXES = {".json", ".md", ".tex"}
REQUIRED_SYMBOL_FIELDS = {
    "canonical",
    "canonical_sources",
    "concept",
    "domain_codomain",
    "forbidden_uses",
    "legacy_aliases",
    "scope",
    "status",
    "type",
}
ALLOWED_STATUSES = {"DEFINITION", "ESTABLISHED", "HYPOTHESIS", "OPEN"}
LEGACY_DECLARATION_FIELDS = {"canonical", "end_line", "path", "scope", "start_line", "token", "type"}
_LINE_CACHE: dict[tuple[str, int], str] = {}


def load_registry(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("registry must be UTF-8 without BOM")
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("registry root must be an object")
    return value


def validate_registry(registry: dict[str, object], root: Path | None = None) -> list[str]:
    errors: list[str] = []
    for key in (
        "schema_version", "contract_id", "target_digest", "expected_symbols",
        "required_active_roots", "active_roots", "active_exclusions",
        "active_line_ranges", "immutable_roots", "immutable_exclusions",
        "legacy_declarations", "symbols",
    ):
        if key not in registry:
            errors.append(f"missing top-level field: {key}")
    if registry.get("schema_version") != "notation-registry/v1":
        errors.append("schema_version must equal notation-registry/v1")
    for key in ("contract_id", "target_digest"):
        value = registry.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{key} must be a nonempty string")
    digest = registry.get("target_digest")
    contract_id = registry.get("contract_id")
    if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        errors.append("target_digest must be 64 lowercase hexadecimal characters")
    elif contract_id != f"contract-sha256-{digest}":
        errors.append("contract_id must bind target_digest")
    active = registry.get("active_roots")
    active_exclusions = registry.get("active_exclusions")
    immutable = registry.get("immutable_roots")
    immutable_exclusions = registry.get("immutable_exclusions")
    required_roots = registry.get("required_active_roots")
    expected_symbols = registry.get("expected_symbols")
    legacy_declarations = registry.get("legacy_declarations")
    symbols = registry.get("symbols")
    active_line_ranges = registry.get("active_line_ranges")
    for name, value in (("active_roots", active), ("immutable_roots", immutable)):
        if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
            errors.append(f"{name} must be a nonempty string list")
        elif value != sorted(set(value)):
            errors.append(f"{name} must be sorted and unique")
    for name, value in (
        ("active_exclusions", active_exclusions),
        ("immutable_exclusions", immutable_exclusions),
        ("required_active_roots", required_roots),
        ("expected_symbols", expected_symbols),
    ):
        if not isinstance(value, list) or not all(isinstance(x, str) and x for x in value):
            errors.append(f"{name} must be a string list")
        elif value != sorted(set(value)):
            errors.append(f"{name} must be sorted and unique")
    if not isinstance(required_roots, list) or not required_roots:
        errors.append("required_active_roots must be nonempty")
    if isinstance(required_roots, list) and isinstance(active, list):
        for spec in required_roots:
            if spec not in active:
                errors.append(f"required active root is not declared active: {spec}")
            if root is not None and (not (root / spec).exists() or not _expand(root, [spec])):
                errors.append(f"required active root has no scannable source: {spec}")
    if root is not None and isinstance(active_exclusions, list):
        for spec in active_exclusions:
            if not (root / spec).exists():
                errors.append(f"active exclusion does not exist: {spec}")
    if not isinstance(active_line_ranges, dict):
        errors.append("active_line_ranges must be an object")
    else:
        for path, line_range in active_line_ranges.items():
            valid_path = isinstance(path, str) and bool(path)
            valid_range = (
                isinstance(line_range, list)
                and len(line_range) == 2
                and isinstance(line_range[0], int)
                and not isinstance(line_range[0], bool)
                and line_range[0] >= 1
                and (
                    line_range[1] is None
                    or (
                        isinstance(line_range[1], int)
                        and not isinstance(line_range[1], bool)
                        and line_range[1] >= line_range[0]
                    )
                )
            )
            if not valid_path or not valid_range:
                errors.append(f"invalid active line range: {path!r}")
            elif root is not None and not (root / path).is_file():
                errors.append(f"active line range path does not exist: {path}")
    if not isinstance(legacy_declarations, list):
        errors.append("legacy_declarations must be a list")
    if not isinstance(symbols, list) or not symbols:
        errors.append("symbols must be a nonempty list")
        return sorted(errors)

    canonicals: list[str] = []
    canonical_types: dict[str, set[str]] = {}
    canonical_type_pairs: set[tuple[str, str]] = set()
    aliases: dict[tuple[str, str], set[str]] = {}
    alias_records: set[tuple[str, str, str, str]] = set()
    for index, symbol in enumerate(symbols):
        if not isinstance(symbol, dict):
            errors.append(f"symbols[{index}] must be an object")
            continue
        missing = REQUIRED_SYMBOL_FIELDS - symbol.keys()
        unexpected = symbol.keys() - REQUIRED_SYMBOL_FIELDS
        if missing:
            errors.append(f"symbols[{index}] missing fields: {','.join(sorted(missing))}")
        if unexpected:
            errors.append(f"symbols[{index}] unexpected fields: {','.join(sorted(unexpected))}")
        if missing or unexpected:
            continue
        canonical = symbol["canonical"]
        type_name = symbol["type"]
        for field in ("canonical", "concept", "type", "domain_codomain", "scope", "status"):
            value = symbol[field]
            if not isinstance(value, str) or not value.strip():
                errors.append(f"symbols[{index}].{field} must be a nonempty string")
        if not isinstance(canonical, str) or not canonical.strip():
            continue
        if not isinstance(type_name, str) or not type_name.strip():
            continue
        if symbol["status"] not in ALLOWED_STATUSES:
            errors.append(f"{canonical}.status is not allowed: {symbol['status']!r}")
        canonicals.append(canonical)
        canonical_types.setdefault(canonical, set()).add(type_name)
        pair = (canonical, type_name)
        if pair in canonical_type_pairs:
            errors.append(f"duplicate canonical/type entry: {canonical!r} / {type_name!r}")
        canonical_type_pairs.add(pair)
        for list_field in ("canonical_sources", "forbidden_uses"):
            value = symbol[list_field]
            if not isinstance(value, list) or not value or not all(isinstance(x, str) and x.strip() for x in value):
                errors.append(f"{canonical}.{list_field} must be a nonempty string list")
            elif len(value) != len(set(value)):
                errors.append(f"{canonical}.{list_field} must be unique")
            elif list_field == "canonical_sources" and root is not None:
                for source in value:
                    if not (root / source).is_file():
                        errors.append(f"{canonical}.canonical source does not exist: {source}")
        legacy = symbol["legacy_aliases"]
        if not isinstance(legacy, list):
            errors.append(f"{canonical}.legacy_aliases must be a list")
            continue
        for alias_index, alias in enumerate(legacy):
            if not isinstance(alias, dict) or set(alias) != {"alias", "scope", "type"}:
                errors.append(f"{canonical}.legacy_aliases[{alias_index}] must contain alias, scope, type")
                continue
            if not all(isinstance(alias[k], str) and alias[k] for k in ("alias", "scope", "type")):
                errors.append(f"{canonical}.legacy_aliases[{alias_index}] fields must be nonempty strings")
                continue
            aliases.setdefault((alias["alias"], alias["scope"]), set()).add(canonical)
            alias_records.add((canonical, alias["alias"], alias["scope"], alias["type"]))

    if canonicals != sorted(canonicals):
        errors.append("symbols must be sorted by canonical")
    if not isinstance(expected_symbols, list) or not expected_symbols:
        errors.append("expected_symbols must be a nonempty string list")
    elif canonicals != expected_symbols:
        errors.append("symbols must exactly match expected_symbols manifest")
    for canonical, types in canonical_types.items():
        if len(types) > 1:
            errors.append(f"canonical token has multiple types: {canonical!r}")
    for (alias, scope), targets in aliases.items():
        if len(targets) > 1:
            errors.append(f"alias maps to multiple canonicals in one scope: {alias!r} / {scope!r}")
    if isinstance(legacy_declarations, list):
        for index, declaration in enumerate(legacy_declarations):
            if not isinstance(declaration, dict) or set(declaration) != LEGACY_DECLARATION_FIELDS:
                errors.append(f"legacy_declarations[{index}] must contain exactly the required fields")
                continue
            if not all(isinstance(declaration[key], str) and declaration[key].strip() for key in ("canonical", "path", "scope", "token", "type")):
                errors.append(f"legacy_declarations[{index}] string fields must be nonempty")
                continue
            start = declaration["start_line"]
            end = declaration["end_line"]
            if not isinstance(start, int) or isinstance(start, bool) or start < 1:
                errors.append(f"legacy_declarations[{index}].start_line must be a positive integer")
                continue
            if not isinstance(end, int) or isinstance(end, bool) or end < start:
                errors.append(f"legacy_declarations[{index}].end_line must be an integer at least start_line")
                continue
            record = (declaration["canonical"], declaration["token"], declaration["scope"], declaration["type"])
            if record not in alias_records:
                errors.append(f"legacy_declarations[{index}] does not match a typed registry alias")
            if root is not None:
                declared_path = root / declaration["path"]
                if not declared_path.is_file():
                    errors.append(f"legacy_declarations[{index}] path does not exist: {declaration['path']}")
                else:
                    line_count = len(declared_path.read_text(encoding="utf-8").splitlines())
                    if end > line_count:
                        errors.append(f"legacy_declarations[{index}] range exceeds file length")
    return sorted(set(errors))


def _relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _expand(root: Path, specs: list[str]) -> list[Path]:
    found: set[Path] = set()
    for spec in specs:
        candidate = root / spec
        if any(ch in spec for ch in "*?["):
            paths = root.glob(spec)
        elif candidate.is_dir():
            paths = candidate.rglob("*")
        else:
            paths = (candidate,)
        for path in paths:
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                found.add(path.resolve())
    return sorted(found, key=lambda p: _relative(p, root))


def _excluded(relative: str, exclusions: list[str]) -> bool:
    return any(relative == item or relative.startswith(item.rstrip("/") + "/") for item in exclusions)


def _record(path: str, line: int, token: str, detail: str) -> dict[str, object]:
    return {"detail": detail, "line": line, "path": path, "token": token}


def _context_text(path: str, line: int, radius: int = 2) -> str:
    return "\n".join(_LINE_CACHE.get((path, number), "") for number in range(max(1, line - radius), line + radius + 1))


def _registered_symbol(registry: dict[str, object], canonical: str) -> dict[str, object] | None:
    for symbol in registry.get("symbols", []):
        if isinstance(symbol, dict) and symbol.get("canonical") == canonical:
            return symbol
    return None


def _registered_alias(registry: dict[str, object], token: str) -> bool:
    for symbol in registry.get("symbols", []):
        if not isinstance(symbol, dict):
            continue
        for alias in symbol.get("legacy_aliases", []):
            if isinstance(alias, dict) and alias.get("alias") == token:
                return True
    return False


def _matching_legacy_declaration(registry: dict[str, object], path: str, line: int, token: str) -> bool:
    for declaration in registry.get("legacy_declarations", []):
        if not isinstance(declaration, dict):
            continue
        if (
            declaration.get("path") == path
            and declaration.get("token") == token
            and isinstance(declaration.get("start_line"), int)
            and isinstance(declaration.get("end_line"), int)
            and declaration["start_line"] <= line <= declaration["end_line"]
        ):
            return True
    return False


def classify_occurrence(path: str, line: int, token: str, registry: dict[str, object]) -> str:
    text = _LINE_CACHE.get((path, line), "")
    lower = text.lower()
    context_lower = _context_text(path, line).lower()
    negative = any(word in lower for word in (" never ", " not", "neither", "forbid", "reject", "fail on", "fails closed", "collision", "distinct from"))
    if token in {"P_A", "Q_A"}:
        if negative:
            return "canonical"
        if _registered_alias(registry, token) and any(word in lower for word in ("historical", "legacy", "frozen")):
            return "documented_legacy"
        return "unclassified_collision"
    if token in {"Q_q", "Q_m"}:
        if negative:
            return "canonical"
        if _registered_alias(registry, token) and any(word in lower for word in ("historical", "legacy", "frozen", "root", "pair", "previous", "certified", "migrate")):
            return "documented_legacy"
        return "unclassified_collision"
    if token == "P (principal bundle)":
        if negative:
            return "canonical"
        if _registered_alias(registry, "P") and _matching_legacy_declaration(registry, path, line, "P"):
            return "documented_legacy"
        return "unclassified_collision"
    if token == "P,Q (local dummy measures)":
        return "documented_legacy"
    if token == "C_t":
        if negative:
            return "canonical"
        if _registered_alias(registry, token) and _matching_legacy_declaration(registry, path, line, token):
            return "documented_legacy"
        return "unclassified_collision"
    if token == "\\varpi_i":
        if negative:
            return "canonical"
        if "geometric" in lower:
            return "canonical"
        if any(word in lower for word in ("occupancy", "receiver mass", "sampling weight", "attention weight")):
            return "unclassified_collision"
        if any(word in lower for word in ("projection", "bundle", "vertical", "tangent")) or "t\\varpi_i" in lower or "\\varpi_i:" in lower or "\\varpi_i\\circ" in lower:
            return "canonical"
        return "unclassified_collision"
    if token == "m_i":
        sample = any(word in lower for word in ("sample", "coordinate", "presentation", "latent")) or "m_i\\in\\mathsf m_i" in lower
        law = bool(re.search(r"m_i.{0,60}(law|distribution|section|recognition|\\mathcal\s*p)|(law|distribution|section|recognition|\\mathcal\s*p).{0,60}m_i", lower))
        if negative and law:
            return "canonical"
        if law:
            if _matching_legacy_declaration(registry, path, line, token):
                return "documented_legacy"
            if _registered_alias(registry, token) and any(word in context_lower for word in ("alias", "occurrence", "migration")):
                return "canonical"
            return "unclassified_collision"
        if sample:
            return "canonical"
        return "canonical"
    if token == "C_A":
        symbol = _registered_symbol(registry, "C_A")
        forbidden = [] if symbol is None else [str(value).lower() for value in symbol.get("forbidden_uses", [])]
        incorrect = any(value in context_lower for value in forbidden)
        typed = any(word in context_lower for word in ("kernel", "channel", "normalized", "\\rightsquigarrow", "pushforward", "equivarian", "intertwine", "compatibility", "independence", "retains", "outside", "fibers of", "apply the same", "use the same"))
        applied = bool(re.search(r"\(?C_A\)?\s*(?:_\\#|\\?circ|\[|\()", _context_text(path, line)))
        if (negative or " only" in lower) and incorrect:
            return "canonical"
        if incorrect:
            return "unclassified_collision"
        if symbol is None or not (typed or applied):
            return "unclassified_collision"
        return "canonical"
    return "canonical"


def _hazards(text: str) -> list[str]:
    tokens: list[str] = []
    for token in ("Q_q", "Q_m", "C_t", "\\varpi_i"):
        if token in text:
            tokens.append(token)
    for token in ("P_A", "Q_A"):
        if re.search(rf"(?<!\\mathbb )(?<!mathbb )\b{token}\b", text):
            tokens.append(token)
    if re.search(
        r"\\pi\s*:\s*P\b|\\mathcal E_[bm x]+\s*=\s*P\\times_|"
        r"principal (?:bundle|connection).{0,50}(?<!\\mathbb )(?<!\\mathcal )(?<!\\mathscr )(?<!\\bar )\bP\b|(?<!\\mathbb )(?<!\\mathcal )(?<!\\mathscr )(?<!\\bar )\bP\b.{0,50}principal (?:bundle|connection)|"
        r"\\operatorname\{Aut\}_G\(P\)|\\Omega\^1\(P[,)]|\\operatorname\{Ad\}\(P\)|"
        r"\bP\|_\{|global triviality of .?P.?|bundles? associated to the same .?P.?|"
        r"\bP\s*=\s*\\mathcal C[^\n]{0,40}\\times\s*G|using one [`$\\(]*P",
        text,
        re.IGNORECASE,
    ):
        tokens.append("P (principal bundle)")
    if re.search(r"\bP\b.{0,20}\bQ\b.{0,45}(local dummy|probability measures)|(?:local dummy|probability measures).{0,45}\bP\b.{0,20}\bQ\b", text, re.IGNORECASE):
        tokens.append("P,Q (local dummy measures)")
    if re.search(r"(?<![A-Za-z])m_i(?![A-Za-z])", text) and (re.search(r"m_i.{0,60}(law|distribution|section|recognition|\\mathcal\s*P)|(law|distribution|section|recognition|\\mathcal\s*P).{0,60}m_i", text, re.IGNORECASE) or any(word in text.lower() for word in ("sample", "coordinate", "presentation", "latent")) or "m_i\\in\\mathsf M_i" in text):
        tokens.append("m_i")
    if re.search(r"(?<!\\mathcal )(?<![A-Za-z])C_A(?![A-Za-z])", text):
        tokens.append("C_A")
    return sorted(set(tokens))


def scan_active_sources(root: Path, registry: dict[str, object]) -> list[dict[str, object]]:
    global _LINE_CACHE
    _LINE_CACHE = {}
    active_specs = list(registry.get("active_roots", []))
    immutable_specs = list(registry.get("immutable_roots", []))
    active_exclusions = list(registry.get("active_exclusions", []))
    exclusions = list(registry.get("immutable_exclusions", []))
    active_line_ranges = registry.get("active_line_ranges", {})
    active_files = [p for p in _expand(root, active_specs) if not _excluded(_relative(p, root), active_exclusions)]
    immutable_files = [p for p in _expand(root, immutable_specs) if not _excluded(_relative(p, root), exclusions)]
    active_set = set(active_files)
    occurrences: list[dict[str, object]] = []
    canonical_tokens = [
        str(symbol["canonical"])
        for symbol in registry.get("symbols", [])
        if isinstance(symbol, dict) and isinstance(symbol.get("canonical"), str) and ("\\" in str(symbol["canonical"]) or str(symbol["canonical"]) in {"C_A", "c_t", "q_A^b", "q_A^m"})
    ]
    for path, immutable in [(p, False) for p in active_files] + [(p, True) for p in immutable_files if p not in active_set]:
        relative = _relative(path, root)
        raw = path.read_bytes()
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            if not immutable:
                occurrences.append(_record(relative, 0, "UTF-8", f"decode failure: {exc}"))
                occurrences[-1]["classification"] = "unclassified_collision"
            continue
        lines = content.splitlines()
        for number, text in enumerate(lines, start=1):
            _LINE_CACHE[(relative, number)] = text
        for number, text in enumerate(lines, start=1):
            line_range = active_line_ranges.get(relative) if isinstance(active_line_ranges, dict) else None
            outside_active_range = (
                not immutable
                and isinstance(line_range, list)
                and len(line_range) == 2
                and (number < line_range[0] or (line_range[1] is not None and number > line_range[1]))
            )
            if immutable or outside_active_range:
                for token in _hazards(text):
                    detail = "immutable released or audit occurrence" if immutable else "immutable pre-Phase-0 occurrence"
                    item = _record(relative, number, token, detail)
                    item["classification"] = "immutable_evidence"
                    occurrences.append(item)
                continue
            seen: set[str] = set()
            for token in _hazards(text):
                classification = classify_occurrence(relative, number, token, registry)
                item = _record(relative, number, token, "active collision rule")
                item["classification"] = classification
                occurrences.append(item)
                seen.add(token)
            for token in canonical_tokens:
                if token not in seen and token in text:
                    item = _record(relative, number, token, "registered canonical token")
                    item["classification"] = "canonical"
                    occurrences.append(item)
    unique = {(str(x["classification"]), str(x["path"]), int(x["line"]), str(x["token"]), str(x["detail"])): x for x in occurrences}
    return [unique[key] for key in sorted(unique)]


def _report(root: Path, registry_path: Path, registry: dict[str, object], occurrences: list[dict[str, object]], errors: list[str]) -> dict[str, object]:
    buckets = {name: [] for name in ("canonical", "documented_legacy", "immutable_evidence", "unclassified_collision")}
    for item in occurrences:
        buckets[str(item["classification"])].append({k: item[k] for k in ("detail", "line", "path", "token")})
    return {
        "schema_version": SCHEMA,
        "contract_id": registry.get("contract_id"),
        "target_digest": registry.get("target_digest"),
        "root": ".",
        "registry": _relative(registry_path, root),
        "registry_sha256": hashlib.sha256(registry_path.read_bytes()).hexdigest(),
        "registry_errors": sorted(errors),
        "source_coverage": _source_coverage(root, registry),
        **buckets,
        "counts": {name: len(items) for name, items in buckets.items()},
        "status": "PASS" if not errors and not buckets["unclassified_collision"] else "FAIL",
    }


def _source_coverage(root: Path, registry: dict[str, object]) -> dict[str, object]:
    exclusions = list(registry.get("active_exclusions", []))
    active_files = [p for p in _expand(root, list(registry.get("active_roots", []))) if not _excluded(_relative(p, root), exclusions)]
    required: list[dict[str, object]] = []
    for spec in registry.get("required_active_roots", []):
        files = [p for p in _expand(root, [str(spec)]) if not _excluded(_relative(p, root), exclusions)]
        required.append({"file_count": len(files), "root": str(spec), "status": "PASS" if files else "FAIL"})
    return {
        "active_file_count": len(active_files),
        "active_files": [_relative(path, root) for path in active_files],
        "required_roots": required,
        "status": "PASS" if required and all(item["status"] == "PASS" for item in required) else "FAIL",
    }


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _base_registry() -> dict[str, object]:
    symbols = [
        {"canonical":"C_A","concept":"coarse channel","type":"normalized Markov kernel","domain_codomain":"Kern(X,Y)","scope":"test","status":"DEFINITION","canonical_sources":["fixture.md"],"legacy_aliases":[],"forbidden_uses":["Galerkin operator","aggregation matrix","deterministic moving map"]},
        {"canonical":"\\mathscr P_G","concept":"principal bundle","type":"principal G-bundle","domain_codomain":"P_G -> C","scope":"test","status":"DEFINITION","canonical_sources":["fixture.md"],"legacy_aliases":[{"alias":"P","scope":"legacy principal-bundle passages","type":"principal G-bundle"}],"forbidden_uses":["probability measure"]},
        {"canonical":"q_i^{m;o,X}","concept":"model-law section","type":"normalized law-valued local section","domain_codomain":"C_i -> E_m","scope":"test","status":"DEFINITION","canonical_sources":["fixture.md"],"legacy_aliases":[{"alias":"m_i","scope":"frozen pointwise-RG explicitly law-valued passage","type":"model-law section"}],"forbidden_uses":["model sample"]},
    ]
    return {
        "schema_version":"notation-registry/v1",
        "contract_id":"contract-sha256-" + "0" * 64,
        "target_digest":"0" * 64,
        "expected_symbols":["C_A","\\mathscr P_G","q_i^{m;o,X}"],
        "required_active_roots":["fixture.md"],
        "active_roots":["fixture.md"],
        "active_exclusions":[],
        "active_line_ranges":{},
        "immutable_roots":["immutable"],
        "immutable_exclusions":[],
        "legacy_declarations":[],
        "symbols":symbols,
    }


def _self_test() -> int:
    failures: list[str] = []
    valid = _base_registry()
    if validate_registry(valid):
        failures.append("valid registry rejected")
    duplicate = json.loads(json.dumps(valid))
    second = json.loads(json.dumps(duplicate["symbols"][0]))
    duplicate["symbols"][0]["legacy_aliases"] = [{"alias":"Z","scope":"same","type":"one"}]
    second["canonical"] = "D_A"
    second["legacy_aliases"] = [{"alias":"Z","scope":"same","type":"two"}]
    duplicate["symbols"].append(second)
    duplicate["symbols"] = sorted(duplicate["symbols"], key=lambda x: x["canonical"])
    duplicate["expected_symbols"] = [symbol["canonical"] for symbol in duplicate["symbols"]]
    if not any("alias maps to multiple" in error for error in validate_registry(duplicate)):
        failures.append("duplicate alias accepted")
    cases = {
        "occupancy": ("Receiver occupancy is \\varpi_i.", True),
        "bare_parent": ("The global generative law is P_A.", True),
        "law_sample": ("The model law m_i is a normalized distribution.", True),
        "law_mathcal_p": ("m_i(r_*)\\in\\mathcal P(\\mathsf Z_i^m).", True),
        "dual_channel": ("C_A is a Markov kernel.\nC_A is an aggregation matrix.", True),
        "untyped_channel": ("Use C_A here.", True),
        "typed_channel": ("C_A is a normalized Markov kernel.", False),
        "active_principal_p": ("The principal bundle has total space P.", True),
        "typed_sample": ("A model sample m_i\\in\\mathsf M_i is a coordinate.", False),
        "active_associated_p": ("\\mathcal E_b=P\\times_{\\rho}\\mathcal B_b is an associated bundle.", True),
        "local_dummy": ("Let P and Q be local dummy probability measures in this lemma.", False),
    }
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "immutable").mkdir()
        (root / "immutable" / "history.md").write_text("The principal bundle has total space P.\n", encoding="utf-8")
        (root / "fixture.md").write_text("C_A is a normalized Markov kernel.\n", encoding="utf-8")
        root_errors = validate_registry(valid, root)
        if root_errors:
            failures.append(f"valid rooted registry rejected: {root_errors}")
        coverage = _source_coverage(root, valid)
        if coverage["status"] != "PASS" or coverage["required_roots"][0]["file_count"] != 1:
            failures.append("required-root coverage did not pass for fixture")
        missing_root = json.loads(json.dumps(valid))
        missing_root["active_roots"] = ["fixture.md", "missing.md"]
        missing_root["required_active_roots"] = ["missing.md"]
        if not any("required active root has no scannable source" in error for error in validate_registry(missing_root, root)):
            failures.append("missing required root accepted")
        missing_source = json.loads(json.dumps(valid))
        missing_source["symbols"][0]["canonical_sources"] = ["missing.md"]
        if not any("canonical source does not exist" in error for error in validate_registry(missing_source, root)):
            failures.append("missing canonical source accepted")
        missing_manifest = json.loads(json.dumps(valid))
        missing_manifest["expected_symbols"] = missing_manifest["expected_symbols"][:-1]
        if not any("expected_symbols manifest" in error for error in validate_registry(missing_manifest, root)):
            failures.append("incomplete expected-symbol manifest accepted")
        invalid_field = json.loads(json.dumps(valid))
        invalid_field["symbols"][0]["status"] = "PROBABLY"
        if not any("status is not allowed" in error for error in validate_registry(invalid_field, root)):
            failures.append("invalid symbol field value accepted")
        for name, (text, should_fail) in cases.items():
            (root / "fixture.md").write_text(text + "\n", encoding="utf-8")
            occurrences = scan_active_sources(root, valid)
            collisions = [x for x in occurrences if x["classification"] == "unclassified_collision"]
            if bool(collisions) != should_fail:
                failures.append(f"{name}: expected collision={should_fail}, got {bool(collisions)}")
            immutable = [x for x in occurrences if x["classification"] == "immutable_evidence"]
            if not immutable:
                failures.append(f"{name}: immutable occurrence not accepted")
        principal_legacy = json.loads(json.dumps(valid))
        principal_legacy["legacy_declarations"] = [{"canonical":"\\mathscr P_G","end_line":1,"path":"fixture.md","scope":"legacy principal-bundle passages","start_line":1,"token":"P","type":"principal G-bundle"}]
        (root / "fixture.md").write_text("The principal bundle has total space P.\n", encoding="utf-8")
        legacy_occurrences = scan_active_sources(root, principal_legacy)
        if any(item["classification"] == "unclassified_collision" for item in legacy_occurrences):
            failures.append("path/range-scoped principal legacy declaration rejected")
        if not any(item["classification"] == "documented_legacy" and item["token"] == "P (principal bundle)" for item in legacy_occurrences):
            failures.append("path/range-scoped principal legacy declaration not classified")
        model_legacy = json.loads(json.dumps(valid))
        model_legacy["legacy_declarations"] = [{"canonical":"q_i^{m;o,X}","end_line":1,"path":"fixture.md","scope":"frozen pointwise-RG explicitly law-valued passage","start_line":1,"token":"m_i","type":"model-law section"}]
        (root / "fixture.md").write_text("m_i(r_*)\\in\\mathcal P(\\mathsf Z_i^m).\n", encoding="utf-8")
        model_occurrences = scan_active_sources(root, model_legacy)
        if not any(item["classification"] == "documented_legacy" and item["token"] == "m_i" for item in model_occurrences):
            failures.append("path/range-scoped law-valued m_i declaration not classified")
    if failures:
        for failure in failures:
            print(f"SELF-TEST FAIL: {failure}", file=sys.stderr)
        return 1
    print("notation scanner self-test: PASS")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail-closed Phase-0 notation collision scanner")
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return _self_test()
    if args.registry is None or args.output is None:
        parser.error("--registry and --output are required unless --self-test is used")
    root = args.root.resolve()
    registry_path = args.registry if args.registry.is_absolute() else root / args.registry
    output_path = args.output if args.output.is_absolute() else root / args.output
    try:
        registry = load_registry(registry_path)
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"registry load failed: {exc}", file=sys.stderr)
        return 2
    errors = validate_registry(registry, root)
    occurrences = [] if errors else scan_active_sources(root, registry)
    report = _report(root, registry_path, registry, occurrences, errors)
    _write_json(output_path, report)
    if report["status"] != "PASS":
        print(f"notation collision scan: FAIL ({report['counts']['unclassified_collision']} unclassified)", file=sys.stderr)
        return 1
    print(f"notation collision scan: PASS ({report['counts']['documented_legacy']} documented legacy; {report['counts']['immutable_evidence']} immutable)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
