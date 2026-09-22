# Checkpoint 008 verification and backups

Engineering snapshot only; the pre-CAD gate is unpassed. No Fusion action, geometry, save or CAD export occurred this checkpoint.

The preceding007 archive passed local ZIP CRC and all stored SHA256 checks before revision. Checkpoint 008 packaging verifies ZIP CRC, every archived file hash, UTF-8, relative Markdown links and historical BOM arithmetic. validation/file-manifest.json excludes its own hash to avoid self-reference. The external backups/checkpoint-008-manifest.json links the full ZIP, SHA256, Git blob identity and source commit.

Remote verification compares content identifiers and reads the manifest and report back. Full remote ZIP redownload/extraction is not verified when the connector returns metadata without content. The external manifest records the actual completed checks. Interim engineering archives remain in the private backups folder; versioned release assets for future native CAD remain a later requirement.

New calculations: pinned extruder junction/movement checks, finite lookahead, five width-audited slices, PA integration/material conservation,25 µs/10 µs convergence on the original path, an independent58-point-per-window quadrature oracle, and spatial/motor screening on the new path. These are numerical checks, not physical printer validation. The1 ms PA window and high-frequency motion peaks remain discretization-sensitive.

No parts purchased, printer connected/configured, reset credit redeemed or messages sent to others. All new G-code is marked analysis only.

Final geometry screen identified unsupported closed roof loops. A sixth bridge-aware slice preserves100% bridge density/flow and replaces those roof loops with open crossing paths. The screen is only a model-volume test, not complete shell coverage. The corrected slice is the next dynamics/coverage audit target.
