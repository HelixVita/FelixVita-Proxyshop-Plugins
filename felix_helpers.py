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


def color_inner_glow(layer):
    current = app.activeDocument.activeLayer
    app.activeDocument.activeLayer = layer
    desc583 = ps.ActionDescriptor()
    ref3 = ps.ActionReference()
    desc584 = ps.ActionDescriptor()
    desc585 = ps.ActionDescriptor()
    desc586 = ps.ActionDescriptor()
    desc587 = ps.ActionDescriptor()
    desc588 = ps.ActionDescriptor()
    desc589 = ps.ActionDescriptor()
    desc590 = ps.ActionDescriptor()
    ref3.PutProperty(sID("property"), sID("layerEffects"))
    ref3.PutEnumerated(sID("layer"), sID("ordinal"), sID("targetEnum"))
    desc583.PutReference(sID("target"),  ref3)
    desc584.PutUnitDouble(sID("scale"), sID("percentUnit"),  1666.666667)
    desc585.PutBoolean(sID("enabled"), True)
    desc585.PutBoolean(sID("present"), True)
    desc585.PutBoolean(sID("showInDialog"), True)
    desc585.PutEnumerated(sID("mode"), sID("blendMode"), sID("multiply"))
    desc586.PutDouble(sID("red"),  0.000000)
    desc586.PutDouble(sID("grain"),  0.000000)
    desc586.PutDouble(sID("blue"),  0.000000)
    desc585.PutObject(sID("color"), sID("RGBColor"),  desc586)
    desc585.PutUnitDouble(sID("opacity"), sID("percentUnit"),  99.000000)
    desc585.PutBoolean(sID("useGlobalAngle"), True)
    desc585.PutUnitDouble(sID("localLightingAngle"), sID("angleUnit"),  120.000000)
    desc585.PutUnitDouble(sID("distance"), sID("pixelsUnit"),  7.000000)
    desc585.PutUnitDouble(sID("chokeMatte"), sID("pixelsUnit"),  25.000000)
    desc585.PutUnitDouble(sID("blur"), sID("pixelsUnit"),  2.000000)
    desc585.PutUnitDouble(sID("noise"), sID("percentUnit"),  0.000000)
    desc585.PutBoolean(sID("antiAlias"), False)
    desc587.PutString(sID("name"),  """Linear""")
    desc585.PutObject(sID("transferSpec"), sID("shapeCurveType"),  desc587)
    desc585.PutBoolean(sID("layerConceals"), True)
    desc584.PutObject(sID("dropShadow"), sID("dropShadow"),  desc585)
    desc588.PutBoolean(sID("enabled"), True)
    desc588.PutBoolean(sID("present"), True)
    desc588.PutBoolean(sID("showInDialog"), True)
    desc588.PutEnumerated(sID("mode"), sID("blendMode"), sID("screen"))
    desc589.PutDouble(sID("red"),  254.000000)
    desc589.PutDouble(sID("grain"),  131.478599)
    desc589.PutDouble(sID("blue"),  0.003891)
    desc588.PutObject(sID("color"), sID("RGBColor"),  desc589)
    desc588.PutUnitDouble(sID("opacity"), sID("percentUnit"),  40.000000)
    desc588.PutEnumerated(sID("glowTechnique"), sID("matteTechnique"), sID("softMatte"))
    desc588.PutUnitDouble(sID("chokeMatte"), sID("pixelsUnit"),  40.000000)
    desc588.PutUnitDouble(sID("blur"), sID("pixelsUnit"),  4.000000)
    desc588.PutUnitDouble(sID("noise"), sID("percentUnit"),  0.000000)
    desc588.PutUnitDouble(sID("shadingNoise"), sID("percentUnit"),  0.000000)
    desc588.PutBoolean(sID("antiAlias"), False)
    desc590.PutString(sID("name"),  """Linear""")
    desc588.PutObject(sID("transferSpec"), sID("shapeCurveType"),  desc590)
    desc588.PutUnitDouble(sID("inputRange"), sID("percentUnit"),  50.000000)
    desc588.PutEnumerated(sID("innerGlowSource"), sID("innerGlowSourceType"), sID("edgeGlow"))
    desc584.PutObject(sID("innerGlow"), sID("innerGlow"),  desc588)
    desc583.PutObject(sID("to"), sID("layerEffects"),  desc584)
    app.ExecuteAction(sID("set"), desc583, NO_DIALOG)

def cig3(pix, r,g,b):
    desc714 = ps.ActionDescriptor()
    ref14 = ps.ActionReference()
    desc715 = ps.ActionDescriptor()
    desc716 = ps.ActionDescriptor()
    desc717 = ps.ActionDescriptor()
    desc718 = ps.ActionDescriptor()
    ref14.PutProperty(sID("property"), sID("layerEffects"))
    ref14.PutEnumerated(sID("layer"), sID("ordinal"), sID("targetEnum"))
    desc714.PutReference(sID("target"),  ref14)
    desc715.PutUnitDouble(sID("scale"), sID("percentUnit"),  1666.666667)
    desc716.PutBoolean(sID("enabled"), True)
    desc716.PutBoolean(sID("present"), True)
    desc716.PutBoolean(sID("showInDialog"), True)
    desc716.PutEnumerated(sID("mode"), sID("blendMode"), sID("screen"))
    desc717.PutDouble(sID("red"),  r*1.000000)
    desc717.PutDouble(sID("grain"),  g*1.000000)
    desc717.PutDouble(sID("blue"),  b*1.000000)
    desc716.PutObject(sID("color"), sID("RGBColor"),  desc717)
    desc716.PutUnitDouble(sID("opacity"), sID("percentUnit"),  35.000000)
    desc716.PutEnumerated(sID("glowTechnique"), sID("matteTechnique"), sID("softMatte"))
    desc716.PutUnitDouble(sID("chokeMatte"), sID("pixelsUnit"),  0.000000)
    desc716.PutUnitDouble(sID("blur"), sID("pixelsUnit"),  pix*1.000000)
    desc716.PutUnitDouble(sID("noise"), sID("percentUnit"),  0.000000)
    desc716.PutUnitDouble(sID("shadingNoise"), sID("percentUnit"),  0.000000)
    desc716.PutBoolean(sID("antiAlias"), False)
    desc718.PutString(sID("name"),  """Linear""")
    desc716.PutObject(sID("transferSpec"), sID("shapeCurveType"),  desc718)
    desc716.PutUnitDouble(sID("inputRange"), sID("percentUnit"),  50.000000)
    desc716.PutEnumerated(sID("innerGlowSource"), sID("innerGlowSourceType"), sID("edgeGlow"))
    desc715.PutObject(sID("innerGlow"), sID("innerGlow"),  desc716)
    desc714.PutObject(sID("to"), sID("layerEffects"),  desc715)
    app.ExecuteAction(sID("set"), desc714, NO_DIALOG)



def apply_inner_glow(layer,size,opacity,r,g,b):
    current = app.activeDocument.activeLayer
    app.activeDocument.activeLayer = layer
    desc834 = ps.ActionDescriptor()
    ref42 = ps.ActionReference()
    desc835 = ps.ActionDescriptor()
    desc836 = ps.ActionDescriptor()
    desc837 = ps.ActionDescriptor()
    desc838 = ps.ActionDescriptor()
    ref42.PutProperty(sID("property"), sID("layerEffects"))
    ref42.PutEnumerated(sID("layer"), sID("ordinal"), sID("targetEnum"))
    desc834.PutReference(sID("target"),  ref42)
    # desc835.PutUnitDouble(sID("scale"), sID("percentUnit"),  1666.666667)
    # desc836.PutBoolean(sID("enabled"), True)
    # desc836.PutBoolean(sID("present"), True)
    # desc836.PutBoolean(sID("showInDialog"), True)
    desc836.PutEnumerated(sID("mode"), sID("blendMode"), sID("normal"))
    desc837.PutDouble(sID("red"),  r*1.000000)
    desc837.PutDouble(sID("grain"),  g*1.000007)
    desc837.PutDouble(sID("blue"),  b*1.000000)
    desc836.PutObject(sID("color"), sID("RGBColor"),  desc837)
    desc836.PutUnitDouble(sID("opacity"), sID("percentUnit"),  opacity*1.000000)
    # desc836.PutEnumerated(sID("glowTechnique"), sID("matteTechnique"), sID("softMatte"))
    # desc836.PutUnitDouble(sID("chokeMatte"), sID("pixelsUnit"),  0.000000)
    desc836.PutUnitDouble(sID("blur"), sID("pixelsUnit"),  size*1.000000)
    # desc836.PutUnitDouble(sID("noise"), sID("percentUnit"),  0.000000)
    # desc836.PutUnitDouble(sID("shadingNoise"), sID("percentUnit"),  0.000000)
    # desc836.PutBoolean(sID("antiAlias"), False)
    # desc838.PutString(sID("name"),  """$$$/Contours/Defaults/Linear=Linear""")
    # desc836.PutObject(sID("transferSpec"), sID("shapeCurveType"),  desc838)
    # desc836.PutUnitDouble(sID("inputRange"), sID("percentUnit"),  50.000000)
    # desc836.PutEnumerated(sID("innerGlowSource"), sID("innerGlowSourceType"), sID("edgeGlow"))
    desc835.PutObject(sID("innerGlow"), sID("innerGlow"),  desc836)
    desc834.PutObject(sID("to"), sID("layerEffects"),  desc835)
    app.ExecuteAction(sID("set"), desc834, NO_DIALOG)
