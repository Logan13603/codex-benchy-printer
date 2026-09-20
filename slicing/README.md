# Analytical slicing evidence

All G-code/3MF files here are deliberately aggressive analysis inputs. They are not commissioning or record-attempt profiles and must not be sent to a printer. No final configuration exists.

Original model provenance is in provenance.json. Frozen rules are in RULES.md. Installed slicer: OrcaSlicer 2.3.2. Run reslice.py for the three nominal-width trials and optimistic_trial.py for combined infill/no retraction. These runners use the versioned flattened inputs, not mutable inherited profiles. Run engineering/path_model.py from the project to regenerate timing results. Python 3 standard library suffices for numerical models; OrcaSlicer must be installed at the documented Windows path or the runner edited for its location.

Generated widths fail the <=0.5mm audit. Profile values alone are not proof of competition compliance. No thinning/deleting of the original mesh was performed. A zero-retraction trial assumes extrusion control that is not validated.
