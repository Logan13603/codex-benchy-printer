# CAD checkpoint 002 backup verification

**Fusion cloud:** `Codex Benchy Printer Main`, Default Project / Codex Benchy Printer, version 4, `urn:adsk.wipprod:fs.file:vf.wAwg5QGJR0iXFu87oGiFbA?version=4`. Fusion save completed; `activeDocument.isModified` was false on readback.

**Source and CAD commit:** [`50a9034e`](https://github.com/Logan13603/codex-benchy-printer/commit/50a9034e3785eba4044172318584a0b7cf93a385). It contains the CAD scripts, parameter CSV, status, and four exported native/STEP files. GitHub fetched all four binary paths from `main` and returned the blob SHA values recorded during upload; the README, CAD status and manifest were also read back. Local sizes and SHA256 hashes are in [the manifest](../cad/native/checkpoint002-manifest.json).

This verifies GitHub object identity and remote path availability. It is **not** a full remote download/rehash or successful Fusion reopen. A local generic ZIP reader cannot validate the proprietary compression method used by the Fusion archive. A Fusion import/reopen test remains required before manufacturing release.

