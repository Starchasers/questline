#!/usr/bin/env python3
"""Add or update questbook text in every locale file, in English.

    python3 tools/questbook/addlang.py texts.json

`texts.json` maps language keys to English text. The questbook is maintained in English
only; the other locale files get the same English text so that keys stay in step with
en.json (tools/lang/check.py reports them as "still English"). Keys that upstream
translated are refused: add a new key instead of changing a translated one.
"""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
LANG = ROOT / "questline/assets/questline/lang"
UPSTREAM = "9a2fd4e2b2e24046de08c7a86aff335294558939"


def main():
    texts = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    upstream = json.loads(subprocess.check_output(
        ["git", "show", f"{UPSTREAM}:questline/assets/questline/lang/en.json"], cwd=ROOT))
    taken = sorted(set(texts) & set(upstream))
    if taken:
        sys.exit(f"upstream keys cannot be changed: {', '.join(taken)}")
    for path in sorted(LANG.glob("*.json")):
        # Edit the text in place: reserialising would reformat files other tools wrote.
        text = path.read_text(encoding="utf-8")
        current = json.loads(text)
        added = []
        for key, value in texts.items():
            line = f"    {json.dumps(key)}: {json.dumps(value, ensure_ascii=False)}"
            if key in current:
                pattern = re.compile(r"^[ \t]*" + re.escape(json.dumps(key)) + r":.*?(,?)$", re.M)
                text, count = pattern.subn(lambda m: line + m.group(1), text, count=1)
                if count != 1:
                    sys.exit(f"cannot find {key} in {path.name}")
            else:
                added.append(line)
        if added:
            body = text.rstrip()
            if not body.endswith("}"):
                sys.exit(f"unexpected end of {path.name}")
            text = body[:-1].rstrip() + ",\n" + ",\n".join(added) + "\n}\n"
        if json.loads(text) != {**current, **texts}:
            sys.exit(f"edit of {path.name} did not produce the expected keys")
        path.write_text(text, encoding="utf-8")
    print(f"{len(texts)} keys written to {len(list(LANG.glob('*.json')))} locale files")


if __name__ == "__main__":
    main()
