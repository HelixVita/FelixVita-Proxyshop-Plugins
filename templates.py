"""
FELIXVITA's TEMPLATES
"""
import proxyshop.templates as temp
from proxyshop.constants import con
from proxyshop.settings import cfg
import proxyshop.helpers as psd
import proxyshop.core as core
import photoshop.api as ps
app = ps.Application()
from pathlib import Path
from proxyshop.text_layers import ExpansionSymbolField, TextField  # For type hinting
import felix_helpers as flx
import json

"""
LOAD CONFIGURATION
"""


my_config = core.import_json_config(Path(Path(__file__).parent.resolve(), "config.json"))
ancient_cfg = my_config['Ancient']


"""
HELPERS
"""


def apply_custom_collector(self, set_layer):
    """
    Applies collector's info to the set layer, in the FelixVita custom format:
    <PrintYear> Proxy • Not for Sale • <SET> <CollectorNumber>/<CardCount> <Rarity>
    For example:
    2004 Proxy • Not for Sale • DST 140/165 U
    If any collector info is missing, it will simply be omitted.
    """
    # Try to obtain release year
    try:
        release_year = self.layout.scryfall['released_at'][:4]
    except:
        release_year = None
    # Conditionally build up the collector info string (leaving out any unavailable info)
    collector_string = f"{release_year} " if release_year else ""
    collector_string += "Proxy • Not for Sale • "
    collector_string += f"{self.layout.set} "
    collector_string += str(self.layout.collector_number).lstrip("0")
    collector_string += "/" + str(self.layout.card_count).lstrip("0") if self.layout.card_count else ""
    collector_string += f" {self.layout.rarity_letter}" if self.layout.rarity else ""
    # Apply the collector info
    set_layer.textItem.contents = collector_string


"""
MODERN TEMPLATE
"""


class ModernTemplate (temp.NormalTemplate):
    """
    FelixVita's Modern template (The 8th Edition / Pre-M15 frame)
    """
    template_file_name = "FelixVita/modern.psd"
    template_suffix = "Modern"

    def __init__(self, layout):
        super().__init__(layout)

    def enable_frame_layers(self):
        super().enable_frame_layers()

    def collector_info(self):
        # Layers we need
        set_layer = psd.getLayer("Set", self.legal_layer)
        artist_layer = psd.getLayer(con.layers['ARTIST'], self.legal_layer)

        # Fill set info / artist info
        apply_custom_collector(self, set_layer)
        psd.replace_text(artist_layer, "Artist", self.layout.artist)

        # Make text white for Lands and Black cards
        if self.layout.background in ["Land", "B"]:
            psd.getLayer("Invert Legal Color").visible = True

"""
ANCIENT TEMPLATE
"""

list_of_all_mtg_sets = list(con.set_symbols.keys())

pre_modern_sets = list_of_all_mtg_sets[:list_of_all_mtg_sets.index("8ED")]

pre_mmq_sets = list_of_all_mtg_sets[:list_of_all_mtg_sets.index("MMQ")]
# Mercadian Masques changed the color of the copyright/collector's info on red cards from black to white (though strangely HML had a mix of black & white).

pre_exodus_sets = list_of_all_mtg_sets[:list_of_all_mtg_sets.index("EXO")]
# Exodus featured a couple of important and lasting changes:
# 1. Colored set symbols for uncommons and rares (silver & gold color)
# 2. Artist+Collector text field at the bottom of the card is now centered (previously left-justified)

pre_mirage_sets = list_of_all_mtg_sets[:list_of_all_mtg_sets.index("MIR")]
# Mirage featured some changes to the frame, including but not limited to:
# 1. Citations in flavor text are now right-justified
# 2. Frame of black cards is now darker
# 3. Wider rules box, with some additional changes for each color:
# 3.1. W: Backgd now less patterned (less contrast); bevel shadows inverted.
# 3.2. U: Backgd now less patterned (less contrast); bevel shadows changed.
# 3.2. B: Parchment no longer surrounded by black box
# 3.2. R: Bevel shadow intensity slightly changed.
# 3.2. G: 'Parchment' brighter and less patterned
# 3.2. M: (No significant changes besides width.)
# 3.2. A: Bevel shadow width & intensity decreased.

pre_hml_sets = list_of_all_mtg_sets[:list_of_all_mtg_sets.index("HML")]
# Homelands changed the color of the copyright/collector's info on blue cards from black to white

pre_fourth_sets = list_of_all_mtg_sets[:list_of_all_mtg_sets.index("4ED")]
# 4ED Made the wooden rules text box of green cards considerably brighter.

pre_legends_sets = list_of_all_mtg_sets[:list_of_all_mtg_sets.index("LEG")]
# Legends made white text (cardname, typeline, P/T) white instead of gray

pre_atq_sets = list_of_all_mtg_sets[:list_of_all_mtg_sets.index("ATQ")]
# Antiquities gave white frames a hint of yellow tint

post_ancient_sets = list_of_all_mtg_sets[list_of_all_mtg_sets.index("8ED"):]

sets_without_set_symbol = [
    "LEA",
    "LEB",
    "2ED",
    "3ED",
    "4ED",
    "5ED",
]

sets_with_hollow_set_symbol = [
    "6ED",
    "DKM",
    "TOR",
    "JUD", # Probably
    "ONS", # Probably
    # Maybe:
    # POR
    "ATQ",
]

sets_lacking_symbol_stroke = [
    # The result of putting a set here is that it will get a near-invisible 1-pixel thick BLACK stroke. (Because can't apply 0-px thick stroke.... WAIT A SEC, what about just not applying a stroke at all?)  # TODO: Finish writing this
    # Only pre-exodus sets should go into this list, as putting a set into this list will result in no gold/silver/mythic color being applied to the set symbol.
    "VIS",
    "ARN", # Probably
    "LEG", # Probably
    # "POR",
    "ICE", # Nope, because even a 1px black stroke is too much; it needs to be white.
    "P02",
    "ATQ",
]

sets_with_black_copyright_for_lands = [_ for _ in pre_mmq_sets if _ not in ["USG", "S99"]]

special_land_frames = {
    "ARN": "Arabian Nights",
    "ATQ": "Antiquities",
    "LEG": "Legends",
    "DRK": "The Dark",
    "FEM": "Fallen Empires",
    "ICE": "Ice Age",
    "HML": "Homelands",
    "ALL": "Alliances",
    "MIR": "Mirage",
    "VIS": "Visions",
    "4ED": "Fourth Edition",
}

original_dual_lands = [
    "Tundra",
    "Underground Sea",
    "Badlands",
    "Taiga",
    "Savannah",
    "Scrubland",
    "Volcanic Island",
    "Bayou",
    "Plateau",
    "Tropical Island",
]

all_keyrune_pre_eighth_symbols_for_debugging = ""

# TODO: Get rid of this "unhide" function, as it's no longer needed (now that psd.getLayer has this functionality).
def unhide(psdpath: tuple, is_group=False):
    # Example: psdpath = ("RW", "ABUR Duals (ME4)", "Land")
    revpath = list(reversed(psdpath))
    # Example: revpath = ("Land", "ABUR Duals (ME4)", "RW")
    selection = psd.getLayerSet(revpath[0])
    psdpath_iter = revpath[1:] if is_group else revpath[1:-1]
    for _ in psdpath_iter:
        selection = psd.getLayerSet(_, selection)
    if not is_group:
        selection = psd.getLayer(revpath[-1], selection)
    selection.visible = True

class AncientTemplate (temp.NormalClassicTemplate):
    """
    FelixVita's template
    """
    template_file_name = "FelixVita/ancient.psd"
    template_suffix = "Ancient"

    def __init__(self, layout):

        # The tombstone icon was not introduced until Odyssey, but you can set this option to True to enable this on all relevant cards. # TODO: Make this a user option.
        # self.smart_tombstone = True
        # self.thicker_collector_info = False  # TODO: Make this a user config option
        # self.use_ccghq_set_symbols = True  # TODO: Make this a config option
        # self.use_timeshifted_symbol_for_non_ancient_sets = True
        # self.use_1993_frame_for_applicable_sets = False


        self.smart_tombstone = ancient_cfg["smart_tombstone"]
        self.thicker_collector_info = ancient_cfg["thicker_collector_info"]
        self.use_ccghq_set_symbols = ancient_cfg["use_ccghq_set_symbols"]
        self.force_use_ccghq_set_symbols_even_when_aesthetically_inferior = ancient_cfg["force_use_ccghq_set_symbols_even_when_aesthetically_inferior"]
        self.use_timeshifted_symbol_for_non_ancient_sets = ancient_cfg["use_timeshifted_symbol_for_non_ancient_sets"]
        self.use_1993_frame_for_applicable_sets = ancient_cfg["use_1993_frame_for_applicable_sets"]

        self.sets_to_use_ccghq_svgs_for = ["PTK", "ALL", "ARN", "LEG", "FEM", "ICE", "POR", "WTH", "TMP", "STH", "PCY", "TOR", "MMQ", "JUD", "INV", "SCG", "UDS", "ODY", "ONS", "EXO", "ULG", "USG", "PLS", "APC", "LGN", "S99", "PTK", "NEM"] + post_ancient_sets  # TODO: Make this a config option

        # Replace the imported contents of symbols.json with that of plugins/FelixVita/symbols.json
        with open(Path(Path(__file__).parent.resolve(), "symbols.json"), "r", encoding="utf-8-sig") as js:
            con.set_symbols = json.load(js)
        # Automatic set symbol enabled?
        if cfg.auto_symbol:
            if layout.set in con.set_symbols:
                layout.symbol = con.set_symbols[layout.set]
            else: layout.symbol = cfg.symbol_char
        else: layout.symbol = cfg.symbol_char

        super().__init__(layout)
        # Use alternate expansion symbol for ICE (ss-ice2 instead of ss-ice)
        if layout.set.upper() == "ICE":
            layout.symbol = ""
        # For Portal sets, use bold rules text and flavor divider:
        if layout.set.upper() in ["POR", "P02", "PTK", "S99"]:
            con.font_rules_text = "MPlantin-Bold"
        else: cfg.flavor_divider = False
        # Right-justify citations in flavor text for all sets starting with Mirage
        if layout.set.upper() not in pre_mirage_sets:
            con.align_classic_quote = True

        self.frame_style = "CardConRemastered-97"
        if self.use_1993_frame_for_applicable_sets and layout.set.upper() in pre_mirage_sets:
            if self.is_land or self.layout.background == "Gold":
                self.frame_style = "Mock-93"
            else:
                self.frame_style = "Real-93" # TODO: Make this a user config option

    def basic_text_layers(self, text_and_icons):

        # TODO: Add code to fix unrenderable cardnames like "Ring of Ma'ruf" and "Marton Stromgald" (might be able to reuse the commented-out code snippet from "templates_old.py" below)
        # # Hardcoded changes to certain cardnames containing unrenderable chars:
        # cardname = str(self.layout.name)
        # if setcode == "ARN" and cardname.upper().startswith("RING"):
        #     cardname = "Ring of Ma'ruf"
        # elif setcode == "ICE" and cardname.upper().endswith("STROMGALD"):
        #     cardname = "Marton Stromgald"

        if self.frame_style == "Real-93":
            # Make the rules text narrower
            rtext = psd.getLayer("Rules Text", con.layers['TEXT_AND_ICONS'])
            tref = psd.getLayer("Textbox Reference", con.layers['TEXT_AND_ICONS'])
            tref.resize(95, 100, ps.AnchorPosition.MiddleCenter)
            rtext.textItem.width = 110
            psd.align_horizontal(rtext, tref); psd.clear_selection()
            tref.visible = False

        if not hasattr(self, "expansion_disabled") or (hasattr(self, "expansion_disabled") and self.expansion_disabled == False):
            expansion_symbol = psd.getLayer(con.layers['EXPANSION_SYMBOL'], con.layers['TEXT_AND_ICONS'])
            super().basic_text_layers(text_and_icons)
            if self.layout.set.upper() in sets_without_set_symbol:
                self.skip_symbol_formatting()
                expansion_symbol.visible = False
            else:
                if (self.use_ccghq_set_symbols and (
                        self.layout.set.upper() in self.sets_to_use_ccghq_svgs_for or
                        self.force_use_ccghq_set_symbols_even_when_aesthetically_inferior
                        )):
                    try:
                        set_symbol_layer = self.load_symbol_svg()
                        self.skip_symbol_formatting()
                        expansion_symbol.visible = False
                        self.frame_set_symbol_layer(set_symbol_layer)
                        self.apply_set_specific_svg_symbol_adjustments(set_symbol_layer)
                    except:
                        pass
                else:
                    # self.frame_set_symbol_layer(expansion_symbol)
                    self.apply_set_specific_keyrune_symbol_adjustments(expansion_symbol)

        if self.layout.set.upper() in ["POR", "P02", "PTK"] and self.is_creature:
            print("breakpoint here")
            power_toughness = psd.getLayer(con.layers['POWER_TOUGHNESS'], text_and_icons)
            power_toughness.visible = False
            sword_and_shield_group = psd.getLayer("Sword & Shield", text_and_icons)
            sword_and_shield_group.visible = True
            power_toughness = psd.getLayer(con.layers['POWER_TOUGHNESS'], sword_and_shield_group)
            print("breakpoint here")
            for lay in self.tx_layers:
                if isinstance(lay, TextField):
                    if lay.layer.name == "Power / Toughness":
                        space = "  "
                        power, tough = tuple(lay.contents.split("/"))
                        lay.contents = str(power) + space + "/" + str(tough) + space
                        lay.layer = power_toughness

    def apply_set_specific_keyrune_symbol_adjustments(self, expansion_symbol):
        if self.layout.set.upper() == "ATQ":
            expansion_symbol.resize(112, 112)
            expansion_symbol.translate(-200, -20)
            self.skip_symbol_formatting()
        if self.layout.set.upper() == "DRK":
            expansion_symbol.translate(30, 10)
            self.skip_symbol_formatting()
            if self.layout.background == "B":
                psd.apply_stroke(expansion_symbol, 2, psd.get_rgb(133, 138, 153))
        if self.layout.set.upper() == "HML":
            self.skip_symbol_formatting()
            app.activeDocument.activeLayer = expansion_symbol
            # expansion_symbol.resize(105, 105)
            expansion_symbol.translate(0, -5)
            psd.fill_expansion_symbol(expansion_symbol, psd.get_rgb(186, 186, 186))  # Gray
            expansion_mask = psd.getLayer("Expansion Mask", con.layers['TEXT_AND_ICONS'])
            psd.apply_stroke(expansion_mask, 5, psd.rgb_white())
        if self.layout.set.upper() == "MIR":
            self.skip_symbol_formatting()
            psd.apply_stroke(expansion_symbol, 9, psd.rgb_white())
        if self.layout.set.upper() == "VIS":
            self.skip_symbol_formatting()
            self.frame_set_symbol_layer(expansion_symbol)
            psd.fill_expansion_symbol(expansion_symbol, psd.rgb_white())
        else:
            # Tested for the following sets: TOR,
            expansion_symbol.translate(-30, 0)

    def skip_symbol_formatting(self):
        """ Skip the default Proxyshop symbol formatting (stroke, fill, etc.) """
        self.tx_layers = [_ for _ in self.tx_layers if not isinstance(_, ExpansionSymbolField)]

    def load_symbol_svg(self, commons_pre_exodus=True):
        # Get rarity
        ccghq_rarity_abbreviations = {
            "Common": "C",
            "Uncommon": "U",
            "Rare": "R",
            "Mythic Rare": "M",
            "Special": "S",
            "Basic Land": "L",
            "Timeshifted": "T",
            "Masterpiece": "M",
        }
        svg_rarity = ccghq_rarity_abbreviations[self.layout.rarity.title()]
        # Don't use rarity colors on set symbol for cards from pre-exodus sets
        if commons_pre_exodus and self.layout.set.upper() in pre_exodus_sets + ["POR", "P02"]:
            svg_rarity = "C"
        if self.layout.set in post_ancient_sets and self.use_timeshifted_symbol_for_non_ancient_sets:
            svg_rarity = "T"
        # Load custom set symbol SVG
        symbols_dirpath = Path("templates", "CCGHQ", "Magic the Gathering Vectors", "Set symbols")
        svg_path = Path(symbols_dirpath, self.layout.set.upper(), svg_rarity + ".svg")
        if svg_rarity == "C":
            # Prefer the "Original" version of the common set symbol whenever it exists
            svg_c_original_path = Path(symbols_dirpath, self.layout.set.upper(), svg_rarity + " - Original.svg")
            if svg_c_original_path.is_file():
                svg_path = svg_c_original_path
        # Select the "Card Name" layer so that the new set symbol layer is created next to it
        app.activeDocument.activeLayer = psd.getLayer(con.layers['NAME'], con.layers['TEXT_AND_ICONS'])
        set_symbol_layer = psd.paste_file_into_new_layer(str(svg_path.resolve()))
        return set_symbol_layer

    def frame_set_symbol_layer(self, set_symbol_layer):
        # Resize and position the set symbol
        expansion_reference = psd.getLayer(con.layers['EXPANSION_REFERENCE'], con.layers['TEXT_AND_ICONS'])
        psd.frame_layer(set_symbol_layer, expansion_reference, anchor=ps.AnchorPosition.MiddleRight, smallest=True, align_h=False, align_v=True)
        psd.align("AdRg", set_symbol_layer, expansion_reference); psd.clear_selection()
        # font_symbol = psd.getLayer(con.layers['EXPANSION_SYMBOL'], con.layers['TEXT_AND_ICONS'])
        # psd.frame_layer(font_symbol, expansion_reference, anchor=ps.AnchorPosition.MiddleRight, smallest=True, align_h=True, align_v=True)
        print("Debug breakpoint here")

    def apply_set_specific_svg_symbol_adjustments(self, svg_symbol):
        if self.layout.set.upper() == "ALL":
            svg_symbol.translate(-90,0)
        if self.layout.set.upper() == "LEG":
            scale = 0.9
            svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
            svg_symbol.translate(30, 10)
        if self.layout.set.upper() == "FEM":
            scale = 0.75
            svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
            svg_symbol.translate(23, -15)
        if self.layout.set.upper() == "ICE":
            scale = 0.8
            svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
            svg_symbol.translate(0, -10)
        if self.layout.set.upper() == "WTH":
            svg_symbol.translate(-30, 0)
        if self.layout.set.upper() == "TMP":
            psd.apply_stroke(svg_symbol, 6, psd.rgb_white())
            scale = 0.85
            svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
            svg_symbol.translate(-35,4)
        if self.layout.set.upper() == "STH":
            psd.apply_stroke(svg_symbol, 3, psd.rgb_white())
            scale = 0.75
            svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
            svg_symbol.translate(-30,0)
        if self.layout.set.upper() == "PTK":
            psd.apply_stroke(svg_symbol, 8, psd.rgb_white())
            psd.rasterize_layer_style(svg_symbol)
            psd.apply_stroke(svg_symbol, 4, psd.rgb_black())
            scale = 0.9
            svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
            svg_symbol.translate(-10,-2)
        # ===========
        # EXO to SCG
        # ===========
        # Stroke thickness
        if self.layout.set.upper() in ["UDS", "MMQ", "JUD", "APC"]:
            psd.apply_stroke(svg_symbol, 1, psd.rgb_white())
        if self.layout.set.upper() in ["SCG"]:
            psd.apply_stroke(svg_symbol, 3, psd.rgb_white())
        if self.layout.set.upper() in ["EXO", "UDS", "S99"]:
            psd.apply_stroke(svg_symbol, 4, psd.rgb_white())
        if self.layout.set.upper() in ["INV"]:
            psd.apply_stroke(svg_symbol, 6, psd.rgb_white())
        if self.layout.set in post_ancient_sets and self.use_timeshifted_symbol_for_non_ancient_sets:
            psd.apply_stroke(svg_symbol, 5, psd.rgb_white())
        # Resize
        if self.layout.set.upper() in ["NEM", "MMQ", "EXO", "LGN"]:
            scale = 0.9
            svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
        if self.layout.set.upper() in ["ONS"]:
            scale = 0.95
            svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
        # Vertical shift
        if self.layout.set.upper() in ["JUD", "LGN", "NEM"]:
            svg_symbol.translate(0, -5)
        # Horizontal shift
        if self.layout.set.upper() in ["EXO", "UDS", "SCG", "S99", "TOR"]:
            svg_symbol.translate(-30,0)
        if self.layout.set.upper() in []:
            svg_symbol.translate(-25,0)
        if self.layout.set.upper() in ["JUD", "LGN", "PCY", "MMQ", "ODY", "PLS"]:
            svg_symbol.translate(-15,0)
        if self.layout.set.upper() in ["ONS", "APC", "NEM"]:
            svg_symbol.translate(-10,0)
        if self.layout.set.upper() in ["ULG", "USG", "PLS"]:
            pass


    def collector_info(self):
        setcode = self.layout.set.upper()
        color = self.layout.background
        legal_layer = psd.getLayerSet(con.layers['LEGAL'])

        # Artist layer & set/copyright/collector info layer
        collector_layer = psd.getLayer(con.layers['SET'], legal_layer)
        artist_layer = psd.getLayer(con.layers['ARTIST'], legal_layer)
        # Replace "Illus. Artist" with "Illus. <Artist Name>"
        psd.replace_text(artist_layer, "Artist", self.layout.artist)
        # Select the collector info layer:
        app.activeDocument.activeLayer = collector_layer
        # Make the collector's info text black instead of white if the following conditions are met:  # TODO: This should probably be moved out of the collector_info() function, and into the post_text_layers() function, or something like that.
        if (
            (color == "W") or
            (color == "U" and setcode in pre_hml_sets) or
            (color == "R" and setcode in pre_mmq_sets) or
            (color == "Land" and setcode in sets_with_black_copyright_for_lands) or
            (setcode in pre_legends_sets)  # Pre-legends coll must be black, because grey is ugly/illegible and white looks weird when all the other legal text is gray.
            ):
            collector_layer.textItem.color = psd.rgb_black()

        if self.thicker_collector_info: psd.apply_stroke(collector_layer, 1, psd.get_text_layer_color(collector_layer))

        # Fill in detailed collector info if available ("SET • 999/999 C" --> "ABC • 043/150 R")
        collector_layer.visible = True
        # Try to obtain release year
        try:
            release_year = self.layout.scryfall['released_at'][:4]
        except:
            release_year = None
        # Conditionally build up the collector info string (leaving out any unavailable info)
        collector_string = ""
        collector_string += "Proxy • Not for Sale — "
        collector_string += f"{self.layout.set} • "
        collector_string += f"{release_year} • " if release_year else ""
        collector_string += str(self.layout.collector_number).lstrip("0")
        collector_string += "/" + str(self.layout.card_count).lstrip("0") if self.layout.card_count else ""
        collector_string += f" {self.layout.rarity_letter}" if self.layout.rarity else ""
        # Apply the collector info
        collector_layer.textItem.contents = collector_string
        # Left-align the collector info for old cards
        if self.layout.set.upper() in pre_exodus_sets + ["P02", "PTK"]:
            self.left_align_artist_and_collector()

    def left_align_artist_and_collector(self):
        """ Left-align the artist and collector info """
        reference = psd.getLayer("Left-Aligned Artist Reference", con.layers['LEGAL'])
        artist = psd.getLayer(con.layers['ARTIST'], con.layers['LEGAL'])
        collector = psd.getLayer(con.layers['SET'], con.layers['LEGAL'])
        artist_delta = reference.bounds[0] - artist.bounds[0]
        collector_delta = reference.bounds[0] - collector.bounds[0]
        artist.translate(artist_delta, 0)
        collector.translate(collector_delta, 0)

    def enable_frame_layers(self):
        # Variables
        border_color = self.layout.scryfall['border_color']
        setcode = self.layout.set.upper()
        cardname = self.layout.scryfall['name']
        # print(f"{cardname=}")

        # White-border vs. Black-border
        if border_color == 'white':
            psd.getLayer("WhiteBorder").visible = True
            if self.frame_style == "Real-93":
                psd.getLayer("If frame is Real-93 and card is white-bordered", ("Nonland", "Misc frame logic")).visible = True  #TODO: Make sure this works.
        elif border_color == 'black':
            if self.layout.scryfall['colors'] == ["B"] and self.frame_style != "Real-93":
                psd.getLayer("If card is B and card is black-bordered", ("Nonland", "Misc frame logic")).visible = True  #TODO: Make sure this works.

        # Frame Style: CardConRemastered-97 vs. Mock-93 vs. Real-93
        if not self.frame_style == "CardConRemastered-97" and not self.is_land and not self.layout.background == "Gold":
            backgd = psd.getLayerSet(self.layout.background, "Nonland")
            psd.getLayer("CardConRemastered-97", backgd).visible = False
            if self.frame_style == "Mock-93":
                psd.getLayer("Mock-93", backgd).visible = True
            if self.frame_style == "Real-93":
                psd.getLayer("Real-93", backgd).visible = True

        if "tombstone" in self.layout.frame_effects:
            psd.getLayer("Tombstone", con.layers['TEXT_AND_ICONS']).visible = True
        if self.smart_tombstone:
            if (
                ("Aftermath" in self.layout.keywords) or  # TODO: Test this once split cards is implemented
                ("Disturb" in self.layout.keywords) or  # TODO: Test this once sun-moon MDFCs are implemented
                ("Dredge" in self.layout.keywords) or
                ("Embalm" in self.layout.keywords) or
                ("Encore" in self.layout.keywords) or
                ("Escape" in self.layout.keywords) or
                ("Eternalize" in self.layout.keywords) or
                ("Flashback" in self.layout.keywords) or  # Example: True for "Faithless looting", but not for "Snapcaster Mage"
                ("Jump-start" in self.layout.keywords) or
                ("Recover" in self.layout.keywords) or
                ("Retrace" in self.layout.keywords) or
                ("Scavenge" in self.layout.keywords) or
                ("Unearth" in self.layout.keywords) or
                (f"{self.layout.card_name_raw} is in your graveyard" in self.layout.oracle_text_raw) or
                (f"return {self.layout.card_name_raw} from your graveyard" in self.layout.oracle_text_raw) or
                (f"exile {self.layout.card_name_raw} from your graveyard" in self.layout.oracle_text_raw) or
                (f"cast {self.layout.card_name_raw} from your graveyard" in self.layout.oracle_text_raw) or
                (f"put {self.layout.card_name_raw} from your graveyard" in self.layout.oracle_text_raw) or
                (f"combine {self.layout.card_name_raw} from your graveyard" in self.layout.oracle_text_raw) or
                (self.layout.card_name_raw in ["Nether Spirit", "Skyblade's Boon"])
                ):
                psd.getLayer("Tombstone", con.layers['TEXT_AND_ICONS']).visible = True
                # TODO: Test all of these tombstone conditions.

        if not self.is_land:
            layer_set = psd.getLayerSet(con.layers['NONLAND'])
            selected_layer = self.layout.background
            # psd.getLayer(selected_layer, layer_set).visible = True
            psd.getLayerSet(selected_layer, layer_set).visible = True
        elif self.is_land:
            land = con.layers['LAND']
            abur = "ABUR Duals (ME4)"
            wholes = "Wholes for regular duals and monocolors"
            halves = "Halves for regular duals"
            modifications = "Modifications"
            thicker_trim_stroke = "Trim - Thicker Outer Black Stroke (2px)"
            thickest_trim_stroke = "Trim - Thickest Outer Black Stroke (3px)"
            thicker_bevels_rules_box = "Rules Box - Inner Bevel - Enhance"
            neutral_land_frame_color = "Neutral - Color (v3)"
            pinlines: str = self.layout.pinlines
            print(f"{pinlines=}")
            is_dual = len(pinlines) == 2
            is_mono = len(pinlines) == 1
            groups_to_unhide = []
            layers_to_unhide = []

            if setcode in ["ARN", "LEG", "ATQ", "ALL", "FEM", "DRK", "HML", "ICE", "4ED"]:
                # Then use that set's unique frame
                layers_to_unhide.append((land, wholes, land))
                groups_to_unhide.append((setcode + " - Color", wholes, land))
                if setcode in ["FEM", "ALL"]:
                    # Enable thick colored trim with no black strokes
                    groups_to_unhide.append(("Trim - " + setcode, modifications, land))
                elif setcode != "LEG":
                    layers_to_unhide.append((thicker_trim_stroke, modifications, land))

            elif setcode in ["MIR", "VIS"]:
                    # Mirage/Visions colorless lands -- Examples: Teferi's Isle (MIR), Griffin Canyon (VIS)
                    layers_to_unhide.append((land, wholes, land))
                    groups_to_unhide.append(("VIS - Color", wholes, land))
                    groups_to_unhide.append((thicker_bevels_rules_box, modifications, land))
                    layers_to_unhide.append((thicker_trim_stroke, modifications, land))
                    if is_mono and setcode == "VIS":
                        # Visions monocolor lands -- Examples: Dormant Volcano (VIS)
                        groups_to_unhide.append((pinlines, wholes, land))
                        layers_to_unhide.append(("Trim - VIS", modifications, land))

            elif is_dual and setcode not in ["TMP", "JUD"]:
            # TMP and JUD are excluded here because those dual lands instead have the same box as colorless lands like Crystal Quarry. -- Examples: "Caldera Lake (TMP)", "Riftstone Portal (JUD)"
                if cardname in original_dual_lands or setcode in ["LEA", "LEB", "2ED", "3ED"]:
                    # ABUR Duals (with the classic 'cascading squares' design in the rules box)
                    layers_to_unhide.append((thicker_trim_stroke, modifications, land))
                    abur_combined_groups = ["WU, UB, UR", "GU, BG, RG, GW"]
                    use_combined_group = None
                    for abur_group in abur_combined_groups:
                        pairs = abur_group.split(", ")
                        if pinlines in pairs:
                            use_combined_group = abur_group
                            break
                    if use_combined_group:
                        selected_abur_group = use_combined_group
                        abur_first_color = "".join(set.intersection(*map(set, selected_abur_group.split(", "))))
                        abur_second_color = pinlines.replace(abur_first_color, "")
                        groups_to_unhide.append((selected_abur_group, abur, land))
                        layers_to_unhide.append((abur_second_color, abur, land))
                    else:
                        selected_abur_group = pinlines
                        abur_second_color = "R" if pinlines in ["RW", "BR"] else "B"
                        groups_to_unhide.append((selected_abur_group, abur, land))
                        layers_to_unhide.append((abur_second_color, abur, land))
                else:
                    # Regular duals (vertically split half-n-half color) -- Examples: Adarkar Wastes (6ED)
                    # TODO: Make sure this does in fact result in "Crystal Quarry" type frame for TMP and JUD duals like "Caldera Lake" and "Riftstone Portal"
                    left_half = pinlines[0]
                    right_half = pinlines[1]
                    layers_to_unhide.append((land, wholes, land))
                    groups_to_unhide.append((neutral_land_frame_color, wholes, land))
                    groups_to_unhide.append((left_half, halves, land))
                    groups_to_unhide.append((right_half, wholes, land))
                    groups_to_unhide.append((thicker_bevels_rules_box, modifications, land))
                    layers_to_unhide.append((thicker_trim_stroke, modifications, land))

            elif is_mono and cardname != "Phyrexian Tower":
                    # Monocolored lands with colored rules box -- Examples: Rushwood Grove (MMQ), Spawning Pool (ULG)
                    # Phyrexian Tower is excluded because it has the colorless land frame despite producing only black mana (not sure why).
                    # TODO: Test to make sure phyrex does indeed render with the colorless land frame
                    layers_to_unhide.append((land, wholes, land))
                    groups_to_unhide.append((neutral_land_frame_color, wholes, land))
                    groups_to_unhide.append((pinlines, wholes, land))
                    groups_to_unhide.append((thicker_bevels_rules_box, modifications, land))
                    layers_to_unhide.append((thickest_trim_stroke, modifications, land))
                    if setcode in ["5ED", "USG"]:
                        # Monocolored lands with colored rules box and YELLOW TRIM -- Examples: Hollow Trees (5ED)
                        layers_to_unhide.append(("Trim 5ED-USG", modifications, land))
                        if pinlines == "W":
                            layers_to_unhide.append(("W - Color Correction - 5ED-USG", pinlines, wholes, land))

            else:
                # Colorless lands (post-USG style) -- Examples: Crystal Quarry (ODY)
                layers_to_unhide.append((land, wholes, land))
                groups_to_unhide.append((neutral_land_frame_color, wholes, land))
                layers_to_unhide.append((thickest_trim_stroke, modifications, land))

            # Figure out which group or layer to unhide
            for group in groups_to_unhide:
                unhide(group, is_group=True)
            for layer in layers_to_unhide:
                unhide(layer)

        # Basic text layers
        text_and_icons = psd.getLayerSet(con.layers['TEXT_AND_ICONS'])
        self.basic_text_layers(text_and_icons)


    def post_text_layers(self):
        super().post_text_layers()

        if self.frame_style == "Real-93" and self.layout.set.upper() in pre_mirage_sets:
            if self.layout.power is not None or self.layout.toughness is not None:
                # Use non-bold MPlantin for the Power and Toughness text
                pt = psd.getLayer("Power / Toughness", con.layers['TEXT_AND_ICONS'])
                pt.textItem.font = "MPlantin"
                pt.textItem.size = 10
                pt.translate(0, -30)

            # Shift the cardname slightly left
            if not self.smart_tombstone:
                psd.getLayer("Card Name", "Text and Icons").translate(-100,0)

            # Color the white text grey for old cards
            if self.layout.set.upper() in pre_legends_sets:
                gray = psd.get_rgb(186, 186, 186)  # Gray
                if self.layout.set.upper() in ['LEA', 'LEB'] or (self.layout.background == "W" and self.layout.set.upper() in ['ARN', 'ATQ']):
                    gray = psd.get_rgb(133, 138, 153)  # Gray for Alpha
                white_text_layers = [
                    psd.getLayer("Card Name", con.layers['TEXT_AND_ICONS']),
                    psd.getLayer("Typeline", con.layers['TEXT_AND_ICONS']),
                    psd.getLayer("Power / Toughness", con.layers['TEXT_AND_ICONS']),
                    psd.getLayer("Artist", con.layers['LEGAL']),
                ]
                for layer in white_text_layers:
                    layer.textItem.color = gray
                    if self.layout.set.upper() in ['LEA', 'LEB']:
                        flx.hide_style_inner_glow(layer)
                    if self.layout.set.upper() == "ATQ" and self.layout.rarity != "C":
                        pass  # TODO: Change color of inner glow to orange/yellow
                if self.layout.background == "B":
                    # Turn collector info grey and clear layer style
                    collector_info = psd.getLayer("Set", con.layers['LEGAL'])
                    collector_info.textItem.color = gray  # Grey Alpha
                    psd.clear_layer_style(collector_info)
                    if self.thicker_collector_info: psd.apply_stroke(collector_info, 1, gray)
                if self.layout.set.upper() in ["LEA", "LEB"]:
                    # Reveal "Border with Dots" by hiding the layers obscuring it
                    psd.getLayer("Border").visible = False
                    psd.getLayer("Extended Black Backdrop", "Frame backdrop").visible = False
                    if self.layout.background in ["W", "R"]:
                        sback = self.layout.background
                        # Use a slightly more pink version of the red frame, or softer version of the white frame
                        psd.getLayer("LEA", ("Nonland", sback, "Real-93")).visible = True

        print("Breakpoint for debug here")
