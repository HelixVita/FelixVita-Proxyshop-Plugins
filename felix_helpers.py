"""
PHOTOSHOP HELPER FUNCTIONS
"""
import os
import photoshop.api as ps
from PIL import ImageColor

def rgb_hex(hex):
    """
    Creates a SolidColor object with the given hex value.
    @param hex: Hexadecimal color value.
    @return: SolidColor object.
    """
    hex = hex.lower()
    if not hex.startswith('#'): hex = '#' + hex
    color = ps.SolidColor()
    r, g, b = ImageColor.getrgb(hex)
    color.rgb.red = r
    color.rgb.green = g
    color.rgb.blue = b
    return color

# QOL Definitions
cwd = os.getcwd()
app = ps.Application()
sID = app.stringIDToTypeID
cID = app.charIDToTypeID
NO_DIALOG = ps.DialogModes.DisplayNoDialogs

# Ensure scaling with pixels, font size with points
app.preferences.rulerUnits = ps.Units.Pixels
app.preferences.typeUnits = ps.Units.Points


def convert_to_layers():
    """Converts a smart object into layers."""
    app.ExecuteAction(sID("placedLayerConvertToLayers"),None, NO_DIALOG)


def place_embedded(file_path):
    """
    The equivalent of "File > Place Embedded" in Photoshop.
    @param file_path: Path to the file to be placed.
    """
    desc1 = ps.ActionDescriptor()
    desc1.PutPath(sID("target"), file_path)
    app.ExecuteAction(sID("placeEvent"), desc1, NO_DIALOG)
    return app.activeDocument.activeLayer


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
