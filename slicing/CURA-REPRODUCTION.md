# Reproduce the independent Cura trial

These files are analysis evidence. Do not print them. No usable printer start sequence, heater protection configuration or homing setup is included.

The official Windows release is [Ultimaker Cura 4.13.1](https://github.com/Ultimaker/Cura/releases/tag/4.13.1). Installer SHA256: `8de0c18a61a29cac9cbcd5b6d1db1de925f3ea36d67d50e0aabef81d66a91538`, 205,747,736 bytes. Authenticode was valid locally. The engine reports Cura_SteamEngine 4.13.1. The older release is used as an independent pre-Arachne fixed-width comparison, not a recommendation to replace an installed slicer.

Extract the official installer to a separate working folder with an archive utility. Keep CuraEngine.exe with its bundled DLLs. Do not modify a user's installed application. Engine binary and definition hashes are in each trial's provenance.json. The runner verifies them before slicing; it does not download or install software.

From the project root, with Python available:

```text
python slicing/reslice_cura.py --engine <extracted-folder>/CuraEngine.exe --trial cura-4.13.1-simplified --out <new-output-folder>
python engineering/audit_cura.py
python engineering/cura_study.py
```

Audit/study commands read the archived trials; compare a fresh output hash with the recorded hash before substituting a regenerated file. The output directory must not already exist. Reproduction on this host produced byte-identical G-code. Other hosts have not been tested.

The CLI does not evaluate all Cura GUI setting expressions. The archived flat settings therefore explicitly set role widths, layer heights, wall counts, solid layers, density, flow multipliers and speed/acceleration assumptions on both machine and extruder contexts. The original STL is unchanged. Optional inter-wall gap fill is disabled, thin-outline printing retained. The simplified trial changes only maximum resolution (0.25 mm), maximum deviation (0.05 mm) and travel resolution (0.25 mm) from the no-gap baseline.

No-gap and simplified settings retain two walls, three top/bottom layers, 10% line infill, 0.5 mm widths and 0.25 mm layers with paired infill. This is a profile-setting statement; local feature coverage and physical quality still need verification. Missing `;WIDTH:` metadata is represented as null in the common summary, not a zero-width extrusion.

Header time, volume and bounds are CLI placeholders. Use the independent G-code audits. The timing study substitutes artificial comparison limits for G-code feed commands; it is not the slicer's own time estimate.
