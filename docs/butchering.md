# Butchering journey

Install framework `questline_0.15.0.zip`, `questlinevanilla_0.14.0.zip`, **Butchering 1.14.3 or newer**, and `questlinebutchering_0.14.0.zip`. The archive basename is not Butchery: the verified modid is `butchering`. Minimum-version metadata is not a claim that untested future versions are verified.

## Directed quest map

Arrows are actual prerequisites. All new action milestones use explicit manual checkboxes: possession does not prove that a corpse was skinned or bled. Each added milestone pays one cookie only.

```text
Vanilla make-knife
  -> Prepare before hunting
  -> Build a skinning hook
  -> Set up the table
  -> Bring home a corpse
  -> Skin with a knife
      -> Catch the blood (optional; not on main spine)
      -> From hide to leather [Leatherwork chapter]
  -> Let it bleed out
  -> Process on the table
      -> Save the useful food
      -> Clean the offal (optional species-dependent branch)
      -> Dry the sinew (optional species-dependent branch)
      -> Use the bones (optional species-dependent branch)
      -> Plan the next trip (optional tools/transport)
```

The vanilla `first-hunt` ID, position, prerequisite and chicken-kill task stay intact. Its replacement adds route guidance and a cookie-only reward; existing progress remains keyed to the same ID. It does **not** pretend a kill proves processing. All other vanilla quests and their asset bytes are unchanged. The addon adds fourteen IDs in total, including the Leatherwork bridge. The content is not a new global default book.

## Crossmod entry points

- **Leatherwork:** a raw hide from the hook feeds the existing hide → soaking → scraping → prepared hide → leather journey. Weak and strong tannin remain parallel preparation, not products of skinning. Its old IDs and tasks are unchanged.
- **Immersive Woodworking:** the verified configuration enables tanning bark; its recipes replace vanilla log tannin inputs. The addon does not require Woodworking, so the page qualifies this advice by installation/configuration.
- **Tailor's Delight:** optional hide-bundle route and changed leather goods. Does not imply the bundle or finished backpack is required by Butchering.
- **Expanded Foods/Chef's Tricks:** optional uses for blood, fat, offal and sinew-derived materials. Oiled hide is a pelt route, not tanned leather.
- **Immersive Corpse Drop:** not an animal harvesting prerequisite. Player graves are not the corpse-hook mechanic.
- Existing husbandry and cleaver quests remain intact. A knife is mandatory for hook skinning; a cleaver is an optional table upgrade, not an iron-age gate.

## Evidence and verification boundary

Primary source: historical **Pszczoly 1.2.0** export, game 1.22.7; Butchering 1.14.3 archive and DLL, its bundled handbook/recipes, and exported `ButcheringConfigV3.json`. See [research](evidence/butchering-research.md) and [SHA-256 ledger](evidence/butchering-sources.json). The old srMi9 URL was not treated as proof of an available current download; a locally cached archive was identified through evpack metadata. All ledger hashes were independently checked against its bytes.

Configured facts include enabled bones and reduced field-harvest yields, disabled bone pickaxe, class-gated recipes and tanning-bark-enabled Woodworking. No separate dressing interaction is invented. Yield-dependent extras cannot block the core journey. Bleeding uses elapsed game time, not a stopwatch achievement.

Automated verification covers content contracts, exact preservation of historical extraction assets, localization ownership and icon codes, production composition with each mod absent/present, deterministic packaging, framework reward/task/tracker regressions, and Release builds. There is **no live full-pack/Testkit gameplay or rendered UI receipt**. Interaction instructions are grounded in archived source/assets and DLL inspection, not a claim of native playtesting. English text is owned by this addon; other locales fall back to English pending human translation.
