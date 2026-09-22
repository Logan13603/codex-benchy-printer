# Checkpoint 006 verification and backups

Revision C removes the hard budget cap and preserves new timing and motor requirements. It does not pass the performance gate. No CAD, cloud version, native archive, STEP, hardware or physical-performance result exists.

Checkpoint 006 is a complete engineering snapshot. validation/file-manifest.json lists per-file SHA256 hashes excluding itself. The external backups/checkpoint-006-manifest.json links the ZIP SHA256, Git blob identity and complete source commit. Earlier snapshots are preserved. The packaging step checks ZIP CRC, all archived hashes, Markdown links, UTF-8 and historical BOM arithmetic.

Remote verification compares returned Git content identifiers and reads back the manifest. **Full remote ZIP redownload and extraction are not verified**; the connector previously returned metadata without binary content for large files. Do not describe identifier verification as a demonstrated downloaded restore. The external manifest records exactly what succeeded during publication.

The connector has no release-asset creation tool in this session. Interim engineering ZIPs remain in the private repository backups directory. Native CAD release assets are a future requirement when CAD exists. No CAD has been represented as backed up.

Fusion remained blank and unsaved; attempted layout command search did not create geometry. The design-type conversion dialog was inspected and canceled; no geometry or cloud save was completed. No purchases, reset credits or messages to others occurred.
