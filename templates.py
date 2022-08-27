"""
FELIXVITA's TEMPLATES
"""
import proxyshop.templates as temp
from proxyshop.constants import con
from proxyshop.settings import cfg
import proxyshop.helpers as psd
import photoshop.api as ps
app = ps.Application()

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
        super().__init__(layout)
        # Use alternate expansion symbol for ICE (ss-ice2 instead of ss-ice)
        if layout.set.upper() == "ICE":
            layout.symbol = ""
        # Use bold rules text and flavor divider for the three Portal sets (and S99):
        if layout.set.upper() in ["POR", "P02", "PTK", "S99"]:
            con.font_rules_text = "MPlantin-Bold"
        else: cfg.flavor_divider = False
        # Right-justify citations in flavor text for all sets starting with Mirage
        if layout.set.upper() not in pre_mirage_sets:
            con.align_classic_quote = True


    def collector_info(self):
        setcode = self.layout.set.upper()
        color = self.layout.background
        legal_layer = psd.getLayerSet(con.layers['LEGAL'])

        # Artist layer & set/copyright/collector info layer
        collector_layer = psd.getLayer(con.layers['SET'], legal_layer)
        artist_layer = psd.getLayer(con.layers['ARTIST'], legal_layer)
        # Color the artist info gray for old cards
        if setcode in pre_legends_sets:
            artist_layer.textItem.color = psd.get_rgb(186, 186, 186)  # Gray
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
            psd.apply_stroke(collector_layer, 1, psd.rgb_black())
        else:
            psd.apply_stroke(collector_layer, 1, psd.get_rgb(238, 238, 238))  # White (#EEEEEE)

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

    def enable_frame_layers(self):
        # Variables
        border_color = self.layout.scryfall['border_color']
        setcode = self.layout.set.upper()
        cardname = self.layout.scryfall['name']
        # print(f"{cardname=}")
        # Enable white border if scryfall says card border is white
        if border_color == 'white':
            psd.getLayer("WhiteBorder").visible = True
        elif border_color == 'black':
            if self.layout.scryfall['colors'] == ["B"]:
                psd.getLayer("Brighter Left & Bottom Frame Bevels", "Nonland").visible = True
        # Hide set symbol for any cards from sets LEA, LEB, 2ED, 3ED, 4ED, and 5ED.
        if setcode in sets_without_set_symbol or setcode == "ALL":
            text_and_icons = psd.getLayerSet(con.layers['TEXT_AND_ICONS'])
            psd.getLayerSet("OuterRetroExpansionGroup", text_and_icons).visible = False
        if setcode in pre_mirage_sets and self.layout.scryfall['colors'] == ["B"]:
            black_group = psd.getLayerSet("B", "Nonland")
            psd.getLayer("1993 Style - B Frame Tint Green", black_group).visible = True
            psd.getLayer("1993 Style - Parchment Black Backdrop", black_group).visible = True
            psd.getLayer("1993 Style - Parchment Color Balance", black_group).visible = True
            psd.getLayer("1993 Style - Brightness", black_group).visible = True
            psd.getLayer("1993 Style - NW Brown Tint", black_group).visible = True
            psd.getLayer("1993 Style - Browner Edges", black_group).visible = True
            psd.getLayer("1993 Style - Parchment Hue", black_group).visible = True
        elif setcode in pre_mirage_sets and self.layout.scryfall['colors'] == ["G"]:
            green_group = psd.getLayerSet("G", "Nonland")
            psd.getLayer("Un-1993 Exposure 2", green_group).visible = False
            psd.getLayer("Un-1993 Color Balance", green_group).visible = False
            if setcode in pre_fourth_sets:
                psd.getLayer("Un-1993 Exposure", green_group).visible = False
                psd.getLayer("Un-1993 Hue", green_group).visible = False
                psd.getLayer("1993 Style - G Frame Color Balance (Hidden by Default)", green_group).visible = True
        elif setcode in ["LEA", "LEB"] and self.layout.scryfall['colors'] == ["R"]:
            red_group = psd.getLayerSet("R", "Nonland")
            psd.getLayer("LEA-LEB Inner Bevel Sunlight", red_group).visible = True
            psd.getLayer("LEA-LEB Box Hue", red_group).visible = True
            psd.getLayer("LEA-LEB Hue", red_group).visible = True
            psd.getLayer("LEA-LEB Color Balance", red_group).visible = True
        elif setcode in pre_hml_sets and self.layout.scryfall['colors'] == ["Artifact"]:
            artifact_group = psd.getLayerSet("Artifact", "Nonland")
            psd.getLayer("1993 Style - Hue/Saturation", artifact_group).visible = True
            psd.getLayer("1993 Style - Levels", artifact_group).visible = True
            psd.getLayer("1993 Style - Levels Overall", artifact_group).visible = True
        elif setcode in pre_mirage_sets and self.layout.scryfall['colors'] == ["W"]:
            white_group = psd.getLayerSet("W", "Nonland")
            psd.getLayer("LEA-LEB - Box Levels", white_group).visible = True
            psd.getLayer("LEA-LEB - Box Hue/Saturation", white_group).visible = True
            psd.getLayer("LEA-LEB - Frame Levels", white_group).visible = True
            psd.getLayer("LEA-LEB - Frame Hue/Saturation", white_group).visible = True
            psd.getLayer("LEA-LEB - Frame Color Balance", white_group).visible = True
        elif setcode in pre_mirage_sets and self.layout.scryfall['colors'] == ["U"]:
            blue_group = psd.getLayerSet("U", "Nonland")
            psd.getLayer("Rules Bevels - Bright SW (Normal)", blue_group).visible = False
            psd.getLayer("Rules Bevels - Bright SW (LEA)", blue_group).visible = True
            # psd.getLayer("LEA-LEB Frame Color Balance", blue_group).visible = True
            # psd.getLayer("LEA-LEB Frame Levels", blue_group).visible = True
            # psd.getLayer("LEA-LEB Frame Hue", blue_group).visible = True
            # psd.getLayer("LEA-LEB Rules Color Balance", blue_group).visible = True
            psd.getLayer("LEA-LEB Rules Brightness", blue_group).visible = True
            psd.getLayer("LEA-LEB Rules Levels", blue_group).visible = True
        elif border_color == 'white' and self.layout.scryfall['colors'] == ["Gold"]:
            gold_group = psd.getLayerSet("Gold", "Nonland")
            psd.getLayer("Left & Bottom Bevel Levels", gold_group).visible = False
        if "tombstone" in self.layout.frame_effects or "Flashback" in self.layout.keywords:  # TODO: Test the new "tombstone" condition. Is self.layout.frame_effects the right expression? Try a non-flashback card, like Genesis (JUD)
            unhide(("Tombstone", con.layers['TEXT_AND_ICONS']), is_group=True)

         # super().enable_frame_layers()

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
        if self.layout.set.upper() in pre_exodus_sets + ["P02", "PTK"]:
            # Left-align artist and collector's info
            reference = psd.getLayer("Left-Aligned Artist Reference", con.layers['LEGAL'])
            artist = psd.getLayer(con.layers['ARTIST'], con.layers['LEGAL'])
            collector = psd.getLayer(con.layers['SET'], con.layers['LEGAL'])
            artist_delta = reference.bounds[0] - artist.bounds[0]
            collector_delta = reference.bounds[0] - collector.bounds[0]
            artist.translate(artist_delta, 0)
            collector.translate(collector_delta, 0)


