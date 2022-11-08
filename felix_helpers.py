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

def select_additional_layer(layer):
    desc1 = ps.ActionDescriptor()
    ref1 = ps.ActionReference()
    ref1.putIdentifier(sID("layer"), layer.id)
    desc1.PutReference(sID("target"),  ref1)
    desc1.PutEnumerated(sID("selectionModifier"), sID("selectionModifierType"), sID("addToSelection"))
    app.ExecuteAction(sID("select"), desc1, NO_DIALOG)

def auto_align_layers():
    desc1 = ps.ActionDescriptor()
    ref1 = ps.ActionReference()
    ref1.PutEnumerated(sID("layer"), sID("ordinal"), sID("targetEnum"))
    desc1.PutReference(sID("target"),  ref1)
    desc1.PutEnumerated(sID("using"), sID("alignDistributeSelector"), sID("ADSContent"))
    desc1.PutBoolean(sID("alignToCanvas"), False)
    desc1.PutEnumerated(sID("apply"), sID("projection"), sID("sceneCollage"))
    desc1.PutBoolean(sID("vignette"), False)
    desc1.PutBoolean(sID("radialDistort"), False)
    app.ExecuteAction(sID("align"), desc1, NO_DIALOG)

def match_color(layer, luminance: int = 100, color_intensity: int = 100, fade: int = 0, neutralize: bool = False):
    """
    Match color of the current layer to the color of target layer.
    """
    desc1 = ps.ActionDescriptor()
    ref1 = ps.ActionReference()
    desc1.PutInteger(sID("lightness"),  100)
    desc1.PutInteger(sID("colorRange"),  100)
    desc1.PutInteger(sID("fade"),  0)
    desc1.PutBoolean(sID("neutralizeColor"), neutralize)
    desc1.PutBoolean(sID("selection"), True)
    ref1.putIdentifier(sID("layer"), layer.id)
    desc1.PutReference(sID("source"),  ref1)
    app.ExecuteAction(sID("matchColor"), desc1, NO_DIALOG)

def subtract_selection(layer):
    """
    Subtracts the pixels of a given layer from the current selection.
    @param layer: Layer object
    """
    desc1 = ps.ActionDescriptor()
    ref1 = ps.ActionReference()
    ref2 = ps.ActionReference()
    ref1.PutEnumerated(sID("channel"), sID("channel"), sID("transparencyEnum"))
    ref1.putIdentifier(sID("layer"),  layer.id)
    desc1.PutReference(sID("target"),  ref1)
    ref2.PutProperty(sID("channel"), sID("selection"))
    desc1.PutReference(sID("from"),  ref2)
    app.ExecuteAction(sID("subtract"), desc1, NO_DIALOG)

def add_selection(layer):
    """
    Adds the pixels of a given layer from the current selection.
    @param layer: Layer object
    """
    desc1 = ps.ActionDescriptor()
    ref1 = ps.ActionReference()
    ref2 = ps.ActionReference()
    ref1.PutEnumerated(sID("channel"), sID("channel"), sID("transparencyEnum"))
    ref1.putIdentifier(sID("layer"),  layer.id)
    desc1.PutReference(sID("target"),  ref1)
    ref2.PutProperty(sID("channel"), sID("selection"))
    desc1.PutReference(sID("from"),  ref2)
    app.ExecuteAction(sID("add"), desc1, NO_DIALOG)

def content_aware_fill_current_selection():
    desc1 = ps.ActionDescriptor()
    desc1.putEnumerated(cID("Usng"), cID("FlCn"), sID("contentAware"))
    desc1.putUnitDouble(cID("Opct"), cID("#Prc"), 100)
    desc1.putEnumerated(cID("Md  "), cID("BlnM"), cID("Nrml"))
    app.executeAction(cID("Fl  "), desc1, NO_DIALOG)

def duplicate_layer_into_new_document():
    desc1 = ps.ActionDescriptor()
    ref1 = ps.ActionReference()
    ref2 = ps.ActionReference()
    ref1.PutClass(sID("document"))
    desc1.PutReference(sID("target"),  ref1)
    desc1.PutString(sID("name"),  """duplicatedLayer""")
    ref2.PutEnumerated(sID("layer"), sID("ordinal"), sID("targetEnum"))
    desc1.PutReference(sID("using"),  ref2)
    desc1.PutInteger(sID("version"),  5)
    app.ExecuteAction(sID("make"), desc1, NO_DIALOG)

def trim_canvas_on_transparency():
    desc1 = ps.ActionDescriptor()
    desc1.PutEnumerated(sID("trimBasedOn"), sID("trimBasedOn"), sID("transparency"))
    desc1.PutBoolean(sID("top"), True)
    desc1.PutBoolean(sID("bottom"), True)
    desc1.PutBoolean(sID("left"), True)
    desc1.PutBoolean(sID("right"), True)
    app.ExecuteAction(sID("trim"), desc1, NO_DIALOG)
