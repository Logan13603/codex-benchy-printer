# Checkpoint 007 verification and backups

Complete engineering snapshot; no manufacturing release. The budget cap is removed and the performance gate remains unpassed. Fusion contains only a blank unsaved Hybrid Design conversion; no CAD geometry, cloud version, native archive or STEP exists.

validation/file-manifest.json lists per-file SHA256 hashes excluding itself. The external backups/checkpoint-007-manifest.json links the complete ZIP SHA256, Git blob identity and source commit. Packaging checks ZIP CRC, all archived hashes, Markdown links, UTF-8 and historical BOM arithmetic. Earlier archives remain preserved.

Remote verification compares Git content identifiers and reads back the manifest. Full remote ZIP redownload/extraction is not verified when the connector returns metadata without content. The external manifest records exactly what succeeded. Interim engineering ZIPs remain in the private backups directory because no release-asset tool is available; native CAD release assets are still a future requirement.

New numerical checks: stroke-volume conservation and analytic distance bounds; cable Hessian, force/moment and power balance; three independent LP minimax comparisons; re-sliced width/volume audits; multi-head volume conservation. These do not validate actual firmware, physical quality, motor dynamics, cooling, collision avoidance or seam strength.

No parts purchased, printer configured, reset credit redeemed or messages sent to others. Repeated Fusion focus/input guards prevented reference geometry creation; the only completed change is conversion of the blank unsaved document to Hybrid Design.
