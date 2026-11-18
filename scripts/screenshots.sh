#!/usr/bin/env bash
# Takes the ModDB screenshots: runs the Gallery tests on the test box at a desktop size and
# copies the PNGs back into screenshots/moddb/. Both runs need the vanilla questbook;
# the second also stages the Expanded Foods questbook and loads ~/questline-addon-mods.
# That directory must contain Expanded Foods and its gameplay dependencies, not an old
# Questline build or duplicate questbooks. Other optional questbooks are not needed here.
#
#   bash scripts/screenshots.sh [user@host] [--force]
#
# Shot.Take copies the newest new file from a screenshots folder every slot on the box
# shares, so a second client taking pictures at the same time can swap them. This refuses
# to run while another client is up, unless --force.
set -euo pipefail

host="dizzyd@vsclient.home"
force=0
for arg in "$@"; do
    case "$arg" in
        --force) force=1 ;;
        *) host="$arg" ;;
    esac
done

repo="$(cd "$(dirname "$0")/.." && pwd)"
vstestkit="${VSTESTKIT:-$repo/../vstestkit}"
out="$repo/screenshots/moddb"
width=1600 height=900

clients="$(ssh "$host" 'cd vstestkit-questline 2>/dev/null || cd vstestkit; bash scripts/slots' | sed -n 's/^clients \([0-9]*\)\/.*/\1/p')"
if [ "${clients:-0}" != "0" ] && [ "$force" = "0" ]; then
    echo "$clients other client(s) running on $host; their screenshots could swap with these." >&2
    echo "Wait for them, or pass --force." >&2
    exit 1
fi

# sync-linux.sh copies the project's parent tree to mods/<repo-name>; the questbook ships inside questline/.
# Pin the slot: a checkout named questline-framework must still use vstestkit-questline.
(cd "$vstestkit" && bash scripts/sync-linux.sh "$host" --slot questline --mod "$repo/questline")
printf -v remote_repo '%q' "mods/$(basename "$repo")"

# The testkit's client window is 960x600; this slot's copy is resized for the pictures (the
# next sync puts it back).
run='set -e
    cd vstestkit-questline
    repo='$remote_repo'
    sed -i -e "s/\"screenWidth\": [0-9]*/\"screenWidth\": '$width'/" -e "s/\"screenHeight\": [0-9]*/\"screenHeight\": '$height'/" templates/clientsettings.json
    export VSTK_SCREEN_WIDTH='$width' VSTK_SCREEN_HEIGHT='$height

# Keep whatever shots were taken even if one fails, then report the failure
status=0
ssh "$host" "rm -f ~/.cairn/games/*/questline-gallery-*.png
    $run
    status=0
    bash scripts/run.sh \"\$repo/tests\" --mod \"\$repo/questline\" --client --filter Gallery || status=\$?
    bash scripts/run.sh \"\$repo/tests\" --mod \"\$repo/questline\" --mods \"\$HOME/questline-addon-mods\" --client --filter ExpandedFoodsKitchen || status=\$?
    exit \$status" || status=$?

mkdir -p "$out"
rm -f "$out"/questline-gallery-*.png
scp -q "$host:.cairn/games/*/questline-gallery-*.png" "$out/" || true
ssh "$host" 'rm -f ~/.cairn/games/*/questline-gallery-*.png'

ls -1 "$out"
exit "$status"
