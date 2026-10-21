# Restore the Rev F 008 and 009 CAD checkpoints

These backups preserve exact copies of the native Fusion and STEP files. Each original was compressed losslessly with gzip and, where necessary, divided into numbered binary parts so the available GitHub connector could upload it safely. The numbered parts are not individually openable CAD files.

Download the private repository as a ZIP using GitHub's **Code → Download ZIP**, or use a checkout that includes this entire folder. Extract it before running the recovery tool. Python 3 and its standard library are sufficient; no GitHub token or extra package is needed.

From this folder run:

```text
python restore.py
```

The recovered files appear in `restored-native` beside the recovery tool:

- `CBP-RevF-009-Bowden-Gantry.f3d`
- `CBP-RevF-009-Bowden-Gantry.step`
- `CBP-RevF-008-Frame.f3d`
- `CBP-RevF-008-Frame.step`

To recover only the current native Fusion checkpoint:

```text
python restore.py --file CBP-RevF-009-Bowden-Gantry.f3d
```

The tool checks every part's byte count, SHA256 and Git blob identity, checks the joined gzip stream, then checks the recovered original's byte count and SHA256 before publishing it. Missing or changed parts stop recovery. It will not overwrite a different existing output file; a file that already matches is reported as verified.

Import/open the recovered `.f3d` in Fusion to recover its saved native feature history and components. The `.step` is an independent geometry interchange backup. Reopening the recovered Fusion archive is a separate validation step from proving its bytes match the exported archive.

The manifest describes the original sizes and hashes, compressed stream sizes/hashes, ordered part names and the Git identities returned by GitHub. The branch commit that first references this directory is the durable remote checkpoint. Blob creation alone is not a complete remote backup; unreferenced objects can be removed by GitHub. Check the task's checkpoint/remote attestation before relying on a reported backup completion.

These files preserve development CAD checkpoints. They are not a manufacturing release or a validated sub-minute printer. Keep future complete native archives as release assets when a reliable release-upload path is available; retain this recovery directory for the historical checkpoint.
