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
_LINE_CACHE: dict[tuple[str, int], str] = {}


def load_registry(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("registry must be UTF-8 without BOM")
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("registry root must be an object")
    return value


def validate_registry(registry: dict[str, object]) -> list[str]:
    errors: list[str] = []
    for key in ("schema_version", "active_roots", "active_line_ranges", "immutable_roots", "symbols"):
        if key not in registry:
            errors.append(f"missing top-level field: {key}")
    active = registry.get("active_roots")
    immutable = registry.get("immutable_roots")
    symbols = registry.get("symbols")
    active_line_ranges = registry.get("active_line_ranges")
    for name, value in (("active_roots", active), ("immutable_roots", immutable)):
        if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
            errors.append(f"{name} must be a nonempty string list")
        elif value != sorted(set(value)):
            errors.append(f"{name} must be sorted and unique")
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
    if not isinstance(symbols, list) or not symbols:
        errors.append("symbols must be a nonempty list")
        return sorted(errors)

    canonicals: list[str] = []
    canonical_types: dict[str, set[str]] = {}
    canonical_type_pairs: set[tuple[str, str]] = set()
    aliases: dict[tuple[str, str], set[str]] = {}
    for index, symbol in enumerate(symbols):
        if not isinstance(symbol, dict):
            errors.append(f"symbols[{index}] must be an object")
            continue
        missing = REQUIRED_SYMBOL_FIELDS - symbol.keys()
        if missing:
            errors.append(f"symbols[{index}] missing fields: {','.join(sorted(missing))}")
            continue
        canonical = symbol["canonical"]
        type_name = symbol["type"]
        if not isinstance(canonical, str) or not canonical:
            errors.append(f"symbols[{index}].canonical must be nonempty")
            continue
        if not isinstance(type_name, str) or not type_name:
            errors.append(f"symbols[{index}].type must be nonempty")
            continue
        canonicals.append(canonical)
        canonical_types.setdefault(canonical, set()).add(type_name)
        pair = (canonical, type_name)
        if pair in canonical_type_pairs:
            errors.append(f"duplicate canonical/type entry: {canonical!r} / {type_name!r}")
        canonical_type_pairs.add(pair)
        for list_field in ("canonical_sources", "forbidden_uses"):
            value = symbol[list_field]
            if not isinstance(value, list) or not all(isinstance(x, str) and x for x in value):
                errors.append(f"{canonical}.{list_field} must be a string list")
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

    if canonicals != sorted(canonicals):
        errors.append("symbols must be sorted by canonical")
    for canonical, types in canonical_types.items():
        if len(types) > 1:
            errors.append(f"canonical token has multiple types: {canonical!r}")
    for (alias, scope), targets in aliases.items():
        if len(targets) > 1:
            errors.append(f"alias maps to multiple canonicals in one scope: {alias!r} / {scope!r}")
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


def classify_occurrence(path: str, line: int, token: str, registry: dict[str, object]) -> str:
    del registry
    text = _LINE_CACHE.get((path, line), "")
    lower = text.lower()
    negative = any(word in lower for word in (" never ", " not ", "forbid", "reject", "fail on", "collision"))
    if token in {"P_A", "Q_A"}:
        if any(word in lower for word in ("historical", "legacy", "frozen", "bare global")) or negative:
            return "documented_legacy"
        return "unclassified_collision"
    if token in {"Q_q", "Q_m"}:
        if any(word in lower for word in ("historical", "legacy", "frozen", "root", "pair", "previous", "certified", "migrate")):
            return "documented_legacy"
        return "unclassified_collision"
    if token == "P (principal bundle)":
        return "documented_legacy"
    if token == "P,Q (local dummy measures)":
        return "documented_legacy"
    if token == "C_t":
        if any(word in lower for word in ("moving", "deterministic", "legacy")) or negative:
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
        law = bool(re.search(r"m_i.{0,45}(law|distribution|section|recognition)|(law|distribution|section|recognition).{0,45}m_i", lower))
        if negative and law:
            return "canonical"
        if sample:
            return "canonical"
        if law and any(word in lower for word in ("frozen", "legacy", "historical", "explicitly law-valued")):
            return "documented_legacy"
        if law:
            return "unclassified_collision"
        return "canonical"
    if token == "C_A":
        matrix = any(word in lower for word in ("matrix", "galerkin", "linear operator"))
        kernel = any(word in lower for word in ("kernel", "channel", "\\rightsquigarrow", "pushforward"))
        if negative and matrix:
            return "canonical"
        if matrix:
            return "unclassified_collision"
        return "canonical" if kernel or "c_a" in lower else "canonical"
    return "canonical"


def _hazards(text: str) -> list[str]:
    tokens: list[str] = []
    for token in ("Q_q", "Q_m", "C_t", "\\varpi_i"):
        if token in text:
            tokens.append(token)
    for token in ("P_A", "Q_A"):
        if re.search(rf"(?<!\\mathbb )(?<!mathbb )\b{token}\b", text):
            tokens.append(token)
    if re.search(r"\\pi\s*:\s*P\b|\\mathcal E_[bm x]+\s*=\s*P\\times_|principal (?:bundle|connection).{0,30}\bP\b", text, re.IGNORECASE):
        tokens.append("P (principal bundle)")
    if re.search(r"\bP\b.{0,20}\bQ\b.{0,45}(local dummy|probability measures)|(?:local dummy|probability measures).{0,45}\bP\b.{0,20}\bQ\b", text, re.IGNORECASE):
        tokens.append("P,Q (local dummy measures)")
    if re.search(r"(?<![A-Za-z])m_i(?![A-Za-z])", text) and (re.search(r"m_i.{0,45}(law|distribution|section|recognition)|(law|distribution|section|recognition).{0,45}m_i", text, re.IGNORECASE) or any(word in text.lower() for word in ("sample", "coordinate", "presentation", "latent")) or "m_i\\in\\mathsf M_i" in text):
        tokens.append("m_i")
    if "C_A" in text:
        tokens.append("C_A")
    return sorted(set(tokens))


def scan_active_sources(root: Path, registry: dict[str, object]) -> list[dict[str, object]]:
    global _LINE_CACHE
    _LINE_CACHE = {}
    active_specs = list(registry.get("active_roots", []))
    immutable_specs = list(registry.get("immutable_roots", []))
    exclusions = list(registry.get("immutable_exclusions", []))
    active_line_ranges = registry.get("active_line_ranges", {})
    active_files = _expand(root, active_specs)
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
        for number, text in enumerate(content.splitlines(), start=1):
            _LINE_CACHE[(relative, number)] = text
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
        **buckets,
        "counts": {name: len(items) for name, items in buckets.items()},
        "status": "PASS" if not errors and not buckets["unclassified_collision"] else "FAIL",
    }


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _base_registry() -> dict[str, object]:
    symbol = {"canonical":"C_A","concept":"coarse channel","type":"normalized Markov kernel","domain_codomain":"Kern(X,Y)","scope":"test","status":"DEFINITION","canonical_sources":["fixture.md"],"legacy_aliases":[],"forbidden_uses":["matrix"]}
    return {"schema_version":"notation-registry/v1","active_roots":["fixture.md"],"active_line_ranges":{},"immutable_roots":["immutable"],"immutable_exclusions":[],"symbols":[symbol]}


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
    if not any("alias maps to multiple" in error for error in validate_registry(duplicate)):
        failures.append("duplicate alias accepted")
    cases = {
        "occupancy": ("Receiver occupancy is \\varpi_i.", True),
        "bare_parent": ("The global generative law is P_A.", True),
        "law_sample": ("The model law m_i is a normalized distribution.", True),
        "dual_channel": ("C_A is a Markov kernel.\nC_A is an aggregation matrix.", True),
        "typed_sample": ("A model sample m_i\\in\\mathsf M_i is a coordinate.", False),
        "local_dummy": ("Let P and Q be local dummy probability measures in this lemma.", False),
    }
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "immutable").mkdir()
        (root / "immutable" / "history.md").write_text("The frozen root pair is (Q_q,Q_m).\n", encoding="utf-8")
        for name, (text, should_fail) in cases.items():
            (root / "fixture.md").write_text(text + "\n", encoding="utf-8")
            occurrences = scan_active_sources(root, valid)
            collisions = [x for x in occurrences if x["classification"] == "unclassified_collision"]
            if bool(collisions) != should_fail:
                failures.append(f"{name}: expected collision={should_fail}, got {bool(collisions)}")
            immutable = [x for x in occurrences if x["classification"] == "immutable_evidence"]
            if not immutable:
                failures.append(f"{name}: immutable occurrence not accepted")
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
    errors = validate_registry(registry)
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
