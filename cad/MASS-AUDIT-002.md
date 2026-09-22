# CAD mass and layout audit — development checkpoint 002

Fusion's body volumes were read from the saved model. The checked design has 18 fully constrained sketches and 16 body instances. Values below are **analytical estimates**, not assigned Fusion physical-material results. Rail and block proxy volumes intentionally omit internal raceways and must not be used as actual part weights.

| Moving item | CAD / catalog basis | Mass used |
|---|---:|---:|
| Carbon XY stage, 112 × 84 × 2 mm | 18.816 cm³ × assumed 1.60 g/cm³ | 30.11 g |
| Aluminum bed substrate, 76 × 50 × 3 mm | 11.400 cm³ × 2.70 g/cm³ | 30.78 g |
| Build-surface film, 76 × 50 × 0.25 mm | 0.950 cm³ × assumed 1.27 g/cm³ | 1.21 g |
| Y carriage, MGN7H reference | Manufacturer block mass | 15.00 g |
| Carbon X crossbridge, 140 × 10 × 10 mm solid envelope | 14.000 cm³ × assumed 1.60 g/cm³ | 22.40 g |
| Y rail, MGN7 110 mm | 0.22 kg/m × 0.110 m | 24.20 g |
| Two X carriages, MGN7H reference | 2 × 15 g | 30.00 g |

**Bare Y-travel mass lower bound:** 77.09 g (stage, bed, film and Y carriage). **Bare X-travel mass lower bound:** 153.69 g (all Y-travel items plus bridge, Y rail and both X carriages). Heater, bed wiring, belt clamps, fasteners, dust seals beyond catalog mass, rail joints and cable drag are still missing. A 2,000,000 mm/s² acceleration would require at least **154 N in Y** and **307 N in X** for these bare masses, before pulley/rotor reflected inertia and friction. This exposes the severity of the unproven timing assumption; it is not a motor-selection result.

The two static X rails total an estimated 57.2 g (2 × 130 mm × 0.22 kg/m). The 400 × 400 × 12 mm base after aperture and four holes has 1742.898 cm³ CAD volume; solid 2.70 g/cm³ aluminum would be **4.706 kg**. The 40 mm structural member geometry is a solid **envelope proxy** and should not be included as actual purchased extrusion mass. The model's current top/bottom stack is base 0–12 mm, shim 12–14 mm, X rail 14–18.8 mm, X cap 18.8–22 mm, moving bridge 22–32 mm, Y rail 32–36.8 mm, Y cap 36.8–40 mm, stage 40–42 mm, bed 42–45 mm, build surface 45–45.25 mm. Fusion Y is machine vertical.

The [HIWIN linear-guideway catalog](https://www.hiwin.com/wp-content/uploads/HIWIN-Linear-Guideway-Catalog.pdf) gives MGN7 rail width 7 mm, height 4.8 mm, 0.22 kg/m rail weight, MGN7H block overall length 30.8 mm, width 17 mm, assembly height 8 mm and block weight 0.015 kg. The selected 130/110 mm rail lengths, shim geometry, stock carbon density and carrier design are development choices; supplier cut lengths and preload are not yet frozen.

Next mass gate: model the heater, belts/clamps, wiring support and actual rail/block masses; then recompute the full X/Y inertial loads and torque-speed curve. Do not report a physical sub-minute capability from this lower-bound table.

