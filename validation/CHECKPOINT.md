# Checkpoint 004 verification and backups

Feasibility gate remains unpassed. Numerical validation is detailed in NUMERICAL-VERIFICATION.md. All CAD, hardware, wiring and physical-performance acceptance checks remain pending because no design is released.

Checkpoint 004 is a complete snapshot, superseding the checkpoint 002 + 003-delta restore chain. `validation/file-manifest.json` lists SHA256 hashes of the snapshot files, excluding itself. The external `backups/checkpoint-004-manifest.json` links the complete ZIP, its SHA256 and Git blob, the source Git commit, and the absence of a Fusion version. Archive creation checks every file hash and ZIP CRC locally.

The remote publishing step compares returned Git blob identifiers with locally calculated Git content identifiers and reads back the manifest. This verifies remote content identity. **Full remote ZIP redownload and extraction are not verified**: the connector's large-file fetch has returned no binary content. Do not call this an independently demonstrated remote restore. A later resume should repeat the identifier checks and perform a full download/restore if a supported route becomes available.

The GitHub connector has file/tree/commit tools but no release-asset creation tool in this session. Interim engineering ZIPs are stored under the private repository's backups directory. Native CAD release assets remain a future requirement when CAD exists; no F3D or STEP is being represented as backed up now. Earlier checkpoints and rejected trials are preserved, not overwritten.

No Fusion changes in this checkpoint. Last verified cloud folder: Default Project / Codex Benchy Printer; last inspected design blank and unsaved. No paid services, parts orders, resets or external messages were used.
