# Resume checkpoint 005 — revision C

**Latest instruction: no fixed budget; make the cheapest credible sub-minute printer.** Historical $400/$500 caps are superseded. Target remains a full-size rules-compliant 50–55-second Benchy; physical acceptance is three consecutive prints under 60 seconds. No questions requested. Owner has Pi, CPAP blower/hose, SD/cord, 9 mm belts/pulleys and some screws; exact identities unknown. Prefer 9 mm where technically suitable. Stop cleanly near 1% five-hour usage remaining; no reset credit authorization.

## Saved engineering state

Read engineering/FEASIBILITY.md and DESIGN-BASIS-C.md. New timing study is in expanded_study.py / expanded-path-results.json. Same simplified Cura slice reaches a hypothetical 51.74879 s at V2400, A2000000, SCV500, Q300. First layer 300 gives 54.2985 s; combined V1700/A1500000/SCV300/Q250/first300 gives 70.2851 s. Pinned Klipper planner verifies arithmetic, not hardware. Seven earlier analytical tests and the byte-identical slice remain unchanged.

Preferred direction for further engineering: hotend stationary in XY, lightweight XY moving bed, hotend/cooling lifted slowly in Z, motors fixed to frame. Detailed mechanism NOT selected. Conventional 24 V architecture results and historical costs are not current design specifications. Compare lightweight crossed-rod and planar parallel-link beds using full dynamics before detailing parts.

Primary Leadshine catalog excerpt/provenance saved under validation/sources/leadshine. Read inertia units carefully (1e-4 kg m²). 86CM120 inertia 2.94e-4 kg m². Illustrative four-motor independent axis, 60 g load, 9 Nm and 30% reserve gives ideal 1.5 million mm/s² with massless r140 mm wheels. The sine-torque load-angle example warns of millimeter-scale rim lag; not a dynamic error prediction or a selected drive. Holding torque rows are explicitly ceilings, not operating torque.

No credible minimum total cost, selected high-flow hotend or physically demonstrated drive margin exists yet. Performance gate remains unpassed; its former budget cap is removed. No parts purchased, hardware configured, physical tests or manufacturing release.

## Fusion state and exact CAD resumption

Computer use only; no Fusion MCP. Verified folder: Default Project / Codex Benchy Printer. Last full observation showed Untitled, blank, unsaved, mm/g, Part Design. No components, sketches, native archives, STEP files or cloud versions exist. This turn attempted to open command search for a reference layout; no geometry or save occurred. Fusion reported other user input in its window; UI work was left untouched. Do not claim a saved layout.

Refresh app/window identity, then inspect current state before input. Existing Windows native tool is @oai/sky through node_repl, documented in the computer-use skill. Avoid printing screenshot results as JSON/base64: forward image content blocks and bounded text only. A standalone reference envelope may be created as a concept layout if useful, clearly excluded from manufacturing parts; detailed CAD still requires the performance gate.

## Exact next engineering operation

1. Compare checkpoint-005 remote manifest with local archive SHA256 and its file-manifest hashes. Remote content identity and a full downloaded restore are separate checks.
2. Obtain primary Minuteman settings/mechanism evidence from https://www.youtube.com/watch?v=iMAWa9vfxcE . Public transcript export failed; browser transcript stalled and playback showed an ad. Do not pretend the episode was fully watched. Printables creator scan URL hit an automated security-verification page; no challenge was solved. Roetz-End GitHub is a separate DMD hotend, not confirmed as the record hotend.
3. Build full path-dependent mass, transmission-inertia, torque-speed, angular tracking and stiffness models for crossed-rod versus planar parallel-link XY bed. Include the 11.06 g growing boat, bearing/rod mass, load-angle error, belt/shaft inertia and deformation. 60 g is a target assumption, not a purchased assembly weight.
4. Establish 250–300 mm³/s capability through a <=0.5 mm nozzle with exact filament, temperature, force and cooling evidence. Four feeds reduce each feed speed, but no four-feed hotend is validated here. Revisit slicer paths if the hardware cannot support the requirement.
5. Once a candidate actually supports nominal <=55 s and sub60 uncertainty margin, freeze exact interfaces, obtain delivered cost comparison, and proceed with full parametric Fusion assembly. Do not substitute larger motors or a pretty layout for the missing performance evidence.

## Backup/runtime notes

Private repository https://github.com/Logan13603/codex-benchy-printer . Previous remote head c30579efbdf43f2570a49cc8576d6700f56b6a0b. Checkpoint 004 full source commit 5982a2554ca129f38f4784eb415ecffb41d406fd. Its local archive and all manifest hashes were verified on this turn. Checkpoint 005 external manifest records new source commit and archive identities after packaging; avoid self-referential checksums.

Bundled Python: C:/Users/logan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe. Cura 4.13.1 extracted runtime: work/cura413. Primary source full catalog and downloaded research are in work; limited motor catalog excerpt is in deliverables. Runtime executables and temporary browser material are excluded from backup. Engineering deliverables live in outputs/codex-benchy-printer.
