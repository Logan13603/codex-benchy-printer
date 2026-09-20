# Revised budget � checkpoint 003, 2026-09-20

**New requirement: at most $400 of additional delivered spending.** The owned Pi, CPAP blower, hose, SD card, cord, and 9mm belts/pulleys have zero acquisition cost. They remain part of the machine's mass and capability. No new hardware is being ordered.

The revised version of the same reference design is **$505.40 estimated delivered**, not yet $400. The prior $643.90 figure was for buying everything and is superseded for this user's incremental budget. Shipping remains a $25 allowance and estimated tax is 8.5% of new items plus shipping. Neither is a checkout quote.

| Inventory credit | Reduction before tax |
|---|---:|
| CPAP kit reference replaced by owned blower/system | $69.99 |
| Owned hose | $14.66 |
| Owned Pi | $15.00 |
| SD/cord portion of host bundle | $8.00 |
| Belts/pulleys portion of transmission bundle | $12.00 |
| Provisional credit for some screws | $8.00 |
| Total credit | $127.65 |

New parts/material subtotal: $440.81; shipping $25.00; estimated tax $39.59; total $505.40. Remaining gap: $105.40. A $6 host-power/connection allowance, $6 idler/spacer allowance and $10 fastener allowance remain. The user's cord is credited to the host bundle; the AC safety/power wiring bundle is not silently removed. An existing compatible CPAP driver is a working assumption, not an identified part. If absent, price it within $400 before proceeding.

## A concrete $400 cost target to source next

This is an allocation exercise, **not sourced replacement parts or a passed gate**. Keep all unmentioned revised BOM lines and target: hotend including heater/sensor at $45 (save $54); frame material $20 (save $12); controller/drivers $30 (save $9.85); required nozzle included in hotend (save $10); printed material $8 (save $4); PSU $30 (save $5); shipping $15 (save $10). This totals $345.96 in new parts plus $15 shipping and $30.68 estimated tax = **$391.64**, leaving $8.36 contingency. Failure to source any target or an extra CPAP driver can erase that margin. A cheaper hotend without demonstrated required flow is not an acceptable performance substitution.

## 9mm transmission decision

Use the owned 9mm belts and compatible pulleys as the preferred design basis. The 6mm transmission is superseded, subject to verifying tooth pitch/profile, pulley tooth counts/bores, usable belt lengths, flanges and required idlers. Do not presume the owned pulleys are 20T or 2GT merely because the old analysis was.

For identical belt construction and free span, tensile stiffness EA/L scales with width: 9/6 = 1.5 times the 6mm value. At the same tensile force, stretch is about two-thirds. If belt compliance alone controls the mode and effective mass is unchanged, frequency increases by sqrt(1.5), about 22.5%. This is a conditional analytical ratio, not a measured resonance. Belt mass per length also rises about 50%; wider pulley/idler inertia, spacing and rail moment must be included. Width by itself does not change travel per revolution, RPM, motor rotor inertia or melt flow. The earlier 136g head/4.08kg machine estimates must be reconciled after owned-part dimensions and mass are available.

## Performance gate

The 50�55-second full-size compliant Benchy target remains unchanged. Cost credits and wider belts do not resolve the generated-width violations, missing small-nozzle flow evidence, or unvalidated timing. Fusion remains blank; detailed CAD stays conditional on the gate. Continue the existing digital investigations and source the allocation above on resume; no questions are required now.
