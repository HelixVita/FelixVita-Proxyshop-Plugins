"""
PHOTOSHOP HELPER FUNCTIONS
"""
import os
import photoshop.api as ps

# QOL Definitions
cwd = os.getcwd()
app = ps.Application()
sID = app.stringIDToTypeID
cID = app.charIDToTypeID
NO_DIALOG = ps.DialogModes.DisplayNoDialogs

# Ensure scaling with pixels, font size with points
app.preferences.rulerUnits = ps.Units.Pixels
app.preferences.typeUnits = ps.Units.Points


def hide_style_inner_glow(layer):
    current = app.activeDocument.activeLayer
    app.activeDocument.activeLayer = layer
    desc1 = ps.ActionDescriptor()
    list14 = ps.ActionList()
    ref1 = ps.ActionReference()
    ref1.PutIndex(sID("innerGlow"),  1)
    ref1.PutEnumerated(sID("layer"), sID("ordinal"), sID("targetEnum"))
    list14.PutReference(ref1)
    desc1.PutList(sID("target"),  list14)
    app.ExecuteAction(sID("hide"), desc1, NO_DIALOG)
    app.activeDocument.activeLayer = current
