# Transmission comparison — checkpoint 004

This is a pre-CAD screen, not a selected drive or a nominal prediction. Run `python engineering/architecture_path_screen.py` from an extracted package. It uses the same `slicing/cura-4.13.1-simplified/analysis.gcode` for all four architectures. [Results](architecture-path-results.json).

The owned belt width is 9 mm; pitch, teeth, bore and usable lengths are unknown. The study assumes 2 mm pitch with 16, 20, 24 or 32 teeth. Motor inertia is 8.45×10⁻⁶ kg m² from the LDO drawing. Motor test data use 24 V, 2.5 A and full steps; the candidate controller has not been shown to reproduce those conditions.

For pitch radius r = teeth × 0.002 / (2π), motor inertia contributes equivalent mass J/r². Each motor also receives a **0.015 kg assumed pulley/idler equivalent mass**, included as a sensitivity allowance for 9 mm hardware. This is not a measured pulley inertia. A 30% torque reserve and 2 N drag per actuator are assumed.

For a segment unit vector u, Cartesian motor-speed ratios are (uX,uY). Force coefficients, in N per m/s², are ((mX+J/r²+extra)uX, (mY+J/r²+extra)uY). Head/bed masses are 0.140/0.090 kg. The crossed gantry uses 0.235 kg per axis plus 0.030 kg synchronization equivalent mass.

CoreXY has motor coordinates A=X+Y and B=X−Y. With mX=0.140 kg and mY=0.325 kg:

`cA = (mX*uX + mY*uY)/2 + (J/r²+extra)*(uX+uY)`

`cB = (mX*uX - mY*uY)/2 + (J/r²+extra)*(uX-uY)`

Motor force is c × acceleration. Both motors supply force on pure-axis moves; an energy-identity check confirms that two rotor inertias are accompanied by two available forces. Diagonal moves raise one motor's speed by √2.

The delta approximation uses 160 mm rods and 85 mm effective lateral rod offset. At the workspace center k=85/sqrt(160²−85²)=0.627; each tower ratio is k times the horizontal projection onto that tower's radial direction. The head-plus-rod mass is 0.158 kg, each carriage 0.026 kg. The symmetric horizontal force solution is mHead*(J*u)/(1.5*k²); actuator inertia and static gravity are added. **Away-from-center geometry, changing Jacobian and velocity-squared acceleration are omitted. This approximation must not be used to choose or configure a delta.**

Each segment's speed is capped at a 2,000 mm/s tool speed and the published 2,100 RPM motor-curve endpoint. Torque is the lowest published/interpolated value from zero to that segment's allowed motor speed, with the first measured point used below 60 RPM. No high-RPM extrapolation occurs. Acceleration is limited by each actuator's remaining force, up to a common 100,000 mm/s² study ceiling. This method is conservative where a segment never reaches its allowed speed, but omitted compliance and dynamics prevent interpreting the total as a guaranteed upper or lower bound.

The 16 pulley/architecture combinations are compared at hypothetical 75 and 200 mm³/s flow caps and 100 mm/s square-corner velocity. The latter is unvalidated. Additional 20T cases vary translating mass to 75–125% and drag to 1–4 N per motor. These ranges describe scenario sensitivity, not confidence intervals. Belt forces, frame flex, hose drag and extrusion dynamics must be measured before a design can claim margin.

The fastest screened combinations at 200 mm³/s are Cartesian 32T 228.52 s; CoreXY 24T 280.83 s; crossed 16T 290.35 s; delta-center 32T 199.38 s. None passes the time gate. Architecture-specific delivered BOMs are not frozen; the two-XY-motor cost reference must not be treated as a delta quote.
