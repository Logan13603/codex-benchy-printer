# Frozen project checklist — revision A, 2026-09-20

Primary source: [Annex Engineering challenge announcement](https://www.youtube.com/watch?v=7zkKcFtLAks), rules in the publisher's video description, retrieved directly from YouTube on 2026-09-20. The earlier checkpoint mistakenly identified JdVZZ4i2dS8 as the announcement: that is a Josh Murrah printer run. It is not the rules source.

| Check | Frozen requirement | Current evidence |
|---|---|---|
| Model | Original single-part CreativeTools mesh, scale 1:1, normal upright orientation | File hash and bounds in provenance.json |
| Filament | Plain PLA selected; allowed families also include PLA+, PETG, ASA, ABS/ABS+. No filled, metallic or silk material | Formulation and spool not frozen |
| Nozzle and width | Each <=0.50 mm | Orca generated-width audit fails; Cura no-gap/simplified have zero definite numerical violations; physical/local coverage audit remains open |
| Layer height | <=0.25 mm | 192 layers, 48 mm height; base profiles 0.25 mm |
| Infill exception | Combining pairs of infill layers is permitted | Separate optimistic trial; verify effective toolpath height |
| Shells | Two walls; three top and three bottom layers | Profile values verified; local small-feature coverage not certified |
| Infill | 10% | Profile value verified |
| Geometry | Complete, reasonably dimensionally accurate boat | Mesh preserved; physical output absent |
| Drive | Stepper motors | Proposed candidates use steppers |
| Evidence | Continuous full-print recording with visible time reference; share profile and entry video | No physical run |

Timing for project calculations: first deposition begins to final deposition ends, including all intervening travel, retraction, Z changes and dwell. Start from a preheated, homed machine. The source does not precisely define the timing endpoints; this is a declared project convention, not claimed organizer adjudication. A physical attempt should also record startup separately and preserve the complete uninterrupted video so alternative timing can be checked.

Latest Discord-only changes were not verified. This freeze records the public primary announcement; it does not claim acceptance by current organizers. Do not upload an entry without explicit user instruction.

The original 60.001 x 31.004 x 48 mm mesh needs more than a strict 60 mm X usable range when aligned to X. An analytical 80 x 80 x 60 mm workspace was used; any selected machine must include skirt-free printing margin and actual tool/nozzle clearances. No model scaling is allowed to make it fit.
