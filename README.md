# User guide

## This is a script that can read raw MATLAB variable and load these variables to Python and build 3D model in an open souce software FreeCAD.
---

# Step 1. Open the Macro dropdown menu in the FreeCAD GUI
# Step 2. Select the third item "Macro"
# Step 3. You will see a default folder where FreeCAD save it's own Python Scripts(Macro). Create one and paste current FreeCAD.py's content to it. You can use any filename for this macro.
# Step 4. 
- `b = Buffer(Param1,Param2)` 
*Param1* is the .mat filename, *Param2* is the full path of this .mat file.
- `b._draw_bar()`

- `b._draw_joint('non-linear')`


