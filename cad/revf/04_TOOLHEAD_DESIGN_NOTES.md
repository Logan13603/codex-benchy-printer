# RevF Bowden toolhead — CAD checkpoint, 2026-10-21

Status: detailed engineering geometry; **not released for manufacture**. The CadQuery builder has been executed. The matching native Fusion builder has not been executed or verified end to end. This checkpoint makes no sub-minute printing claim.

## Current physical layout

- The extruder motor is fixed to the machine, not carried on the toolhead. The toolhead has a metal tube-through PC4-M6 fitting and a modeled 4 OD / 2 ID PTFE entry. The fitting is still a provisional purchased interface. Verify its actual thread length, tube stop and pullout force before manufacture.
- The nozzle datum remains `(0, -38, 225)` mm. The official maker Goliath STEP is translated by `(0, -38, 250.750000685)` mm; its actual top is approximately Z294.25. The aluminum platform datum is Z294.26.
- A 36 × 54 × 3 mm aluminum spine mounts to the MGN7H carriage with four M2 clearance holes on a 13 × 12 mm pattern. The 32 × 30 × 6 mm aluminum platform has the measured four-hole hotend pattern at X±5.657 / Y−38±5.657, and a center M6×1 tapped fitting interface. Confirm the hotend thread designation and usable blind depth against the purchased hotend.
- Four M2.5×10 hotend screws use controlled 1.0 mm shims above the 6 mm plate: nominal thread engagement is 3.0 mm, leaving approximately 0.375 mm nominal blind-hole tip clearance. This small remaining clearance must be checked on actual parts.
- The cold-end fan is a separate 25 × 25 × 10 mm proxy, on a removable printed cradle and shroud. Its 20 mm hole pitch, electrical rating, cooling performance and mass are assumptions. The fan has corner nut/driver clearances. Part-cooling CPAP air does not replace cold-end cooling.
- A removable two-piece wire saddle separates heater and sensor/fan bundles. Platform screw heads and their drivers have Ø7 clearance openings through the saddle. Saddle screws are X±15 / Z294; the spine is wide enough to retain edge distance.
- A 0.5 mm aluminum rear guard protects the heater-wire area and reduces direct radiation toward rear hardware. It is not a substitute for the hotend maker's insulation or silicone sock.

## CPAP duct geometry and attachment

The 22 mm inlet ID / 25 mm spigot OD remains provisional because the user's actual hose and blower have not been identified. The inlet is centered at X0 / Y−14, above and behind the Bowden filament axis. A coaxial inlet would collide with the filament tube.

The two branches are mirrored. Each uses nominal 12 × 10 mm clear trunks centered at X±42 / Y−62 between Z247 and Z301. Their forward location was chosen to clear the moving-idler envelope. The fork/trunk mating plane is Z301. Flanges are 41 × 20.2 × 2 mm, with four M2.5 holes on a 35 × 14.2 mm pattern. Their actual rear envelope is Y−51.9, rather than the trunk wall's Y−55.8; hardware clearance must use the full envelope.

The lower ducts return through `(X±38, Y−55, Z237)` and `(X±27, Y−40, Z231)` to opposed 16 × 3 mm outlets centered at `(X±12, Y−38, Z228.8)`. Jets aim inward and down by 17 degrees. The geometric lower outer lip is approximately Z226.22, above the Z225 nozzle/first-layer datum. The jet centerline reaches the nozzle's XY position near Z225.13.

All six duct shell parts are separate solids, with open median seams that follow Y as a function of Z. Internal supports can therefore be accessed. Thin neutral-cure sealant is required at the mating seams; its compatibility with the selected printed material and actual hotend temperature must be checked. The fork has inlet and arm seam fasteners; each lower branch has three seam fasteners, a four-screw flange and a separate M3 mounting nut pocket. The M3 boss pocket does not intentionally penetrate the air wall.

The printed U bridge is a real load path. Its rear crossbar attaches to two tapped spine holes at Z306. Arms pass outboard at X±52, with their lower face at Z302.5. Front legs descend to bosses at Z295; their lower face is Z291.5. Short feet connect the outboard legs to the duct bosses at X±42. M3×12 screws enter from the rear with driver access below the overhead arms. The bridge's rear envelope is Y−21, giving only 2 mm nominal separation from the portal at Y−19; this remains a travel-audit item.

## Executed checks and mass limits

The full toolhead self-audit includes all 93 named parts, including screws, washers, shims, spacers and nuts. Every exported part is one valid solid. The final self-interference screen found **zero unexpected overlaps above 0.05 mm³**, after explicitly listing the intended simplified threaded mates. A cylindrical screw major diameter intersecting a tap-drill/minor bore is recorded as a thread mate; unrelated hardware collisions are not exempted.

The modeled/assumed mass is **200.704 g**, with estimated centroid **(−0.043, −40.535, 280.657) mm**. This excludes the MGN7H carriage block, the supported share of the flexible Bowden tube, CPAP hose and wiring. Purchased mass overrides are Goliath 80 g, fan 8 g and fitting 5 g; none has been physically weighed. Their geometric centroids are proxies for mixed-material assemblies. Do not use these values as measured mass properties or a certified balance result. Rerun the full machine mass/force-plane calculation with the latest geometry.

Minimum specified clear section area is 48 mm² per outlet; the straight trunks are 120 mm² each. The audit JSON also reports endpoint projected areas along each piecewise centerline segment. Those values are a geometric flow screen, not a pressure-flow solution. At a total measured flow of 3–6 L/s, the nominal outlet mean velocity would be 31.25–62.5 m/s. Neither that flow nor the pressure needed to produce it has been established for the owned blower/hose.

## Manufacturing release blockers

1. **Thin loft walls.** Offsetting each rectangular profile by 1.2 mm does not produce a 1.2 mm normal wall along an oblique loft. A surface-spacing sample of the isolated ruled loft segments found approximately 0.547 / 0.472 mm at the upper fork, 1.200 mm in the straight trunks, and 0.821 / 0.624 / 1.097 mm in the lower transitions. These are sampled local spacings, not an exhaustive global thickness result; flanges/tabs may add material at some sampled locations. Proper shell/thickening or larger local profile offsets, followed by a new clearance and thickness audit, is required before printing these parts for use.
2. **Travel integration.** The full machine has fixed-return belt and cap/clamp keepouts beyond the moving-idler envelope. The earlier 80 mm X workspace failed the independent assembly audit. The root project is assessing X±25 / Y−20…+45 with the Benchy rotated 90 degrees. Do not assume that workspace passes until its final report says so. This checkpoint's toolhead self-audit is not a full machine travel audit.
3. **Purchased interfaces.** Verify the PC4-M6 tube-through fitting, 2510 fan, hotend thread/depth, hose cuff and heater/sensor routing against actual selected components. The current purchased proxies are not sufficient to release these interfaces.
4. **Thermal and pressure tests.** Measure duct temperatures during a hot soak with the real cold-end fan and CPAP conditions. Leak-test the seams; measure blower pressure/flow with the actual hose and nozzle duct. Verify heatbreak cooling and avoid directing cooling air onto uninsulated heater surfaces.
5. **Native CAD completion.** Execute and audit native Fusion features, sketch constraints, section correspondence, recomputation, joints and component organization. The native helper repair is in progress in the root project. No native success is inferred from successful STEP exports.

No geometry changes should be made from these notes without a new source hash, regenerated exports and a repeated full-machine travel/mass check. The standalone JSON manifest lists current files; older standalone exports with superseded names are not current assembly members.
