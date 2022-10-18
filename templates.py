"""
FELIXVITA's TEMPLATES
"""
from proxyshop.gui import ConsoleOutput, console_handler as console
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
import os
import csv

"""
HELPER CONSTANTS
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

pre_dominaria_sets = list_of_all_mtg_sets[:list_of_all_mtg_sets.index("DDU")]

sets_without_set_symbol = [
    "LEA",
    "LEB",
    "2ED",
    "3ED",
    "4ED",
    "5ED",
]

sets_without_rarity = pre_exodus_sets + ["POR", "P02"]

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

portal_frame_sets = ["POR", "P02", "PTK", "S99"]

all_keyrune_pre_eighth_symbols_for_debugging = ""

ancient_sets_with_felix_approved_ccghq_symbols = ["ALL", "ARN", "LEG", "FEM", "ICE", "POR", "WTH", "TMP", "STH", "PCY", "TOR", "MMQ", "JUD", "INV", "SCG", "UDS", "ODY", "ONS", "EXO", "ULG", "USG", "PLS", "APC", "LGN", "S99", "PTK", "NEM"]

felix_rejected_ccghq_symbols = ["AFC", "MID", "CLB", "NCC"]

"""
LOAD CONFIGURATION
"""

config_json = core.import_json_config(Path(Path(__file__).parent.resolve(), "config.json"))

# Defaults for auto
if config_json['Global']['thicker_collector_info'] == "auto":
    config_json['Global']['thicker_collector_info'] = False
if config_json['Global']['enable_mock_copyright'] == "auto":
    config_json['Global']['enable_mock_copyright'] = True
if config_json['Global']['smart_tombstone'] == "auto":
    config_json['Global']['smart_tombstone'] = True
if config_json['Global']['use_legendary_crown'] == "auto" or False:
   console.update("WARNING: Disabling of legendary crown is not yet implemented. Consider voting for this issue at https://github.com/MrTeferi/MTG-Proxyshop/issues/18")

def decision_to_enable_art_position_memory(self):
    user_input = self.config_json['Global']['art_position_memory_enabled']
    if isinstance(user_input, bool):
        return user_input
    if user_input == "auto":
        return True

def decision_to_memorize_new_art_position(self):
    user_input = config_json['Global']['art_position_memorize_new']
    if isinstance(user_input, bool):
        return user_input
    if  user_input == "auto":
        return not self.current_art_pos_entry_exists

def decision_to_use_premium_star_between_set_and_lang(self):
    user_input = self.config_json['Normal']['use_premium_star_between_set_and_lang']
    if isinstance(user_input, bool):
        return user_input
    if user_input == "auto":
        # If no nonfoil printing of the card exists in this set, then use the "premium" star instead of the regular dot:
        return not self.layout.scryfall['nonfoil']

def decision_to_use_flavor_divider(self, layout):
    user_input = self.config_json['Global']['flavor_divider']
    if isinstance(user_input, bool):
        return user_input
    if  user_input == "auto":
        if layout.set.upper() in portal_frame_sets:
            return True
        elif layout.set.upper() in pre_modern_sets:
            return False
        elif layout.set.upper() in pre_dominaria_sets:
            return False
        elif Path(self.template_file_name).stem in["modern", "ancient"]:
            return False
        else:
            return True

def decision_to_have_legendary_crown(self):
    user_input = self.config_json['Global']['use_legendary_crown']
    if isinstance(user_input, bool):
        return user_input
    if user_input == "auto":
        return self.layout.set.upper() not in pre_dominaria_sets

def decision_to_use_ccghq_symbol(self):
    user_input = self.config_json['Global']['use_ccghq_set_symbols']
    if isinstance(user_input, bool):
        return user_input
    if user_input == "auto":
        if self.layout.set.upper() in pre_modern_sets:
            return self.layout.set.upper() in ancient_sets_with_felix_approved_ccghq_symbols
        else:
            return self.layout.set.upper() not in felix_rejected_ccghq_symbols

def decision_to_have_set_symbol(self):
    user_input = self.config_json['Global']['use_set_symbol']
    if isinstance(user_input, bool):
        return user_input
    if user_input == "auto":
        return self.layout.set.upper() not in sets_without_set_symbol

def decision_to_use_ccghq_symbol_rarity(self):
    user_input = self.config_json['Global']['use_ccghq_set_symbol_rarity_color']
    if isinstance(user_input, bool):
        return user_input
    if user_input == "auto":
        return self.layout.set.upper() not in sets_without_rarity

def decision_to_use_timeshifted_rarity_for_ccghq(self):
    user_input = self.config_json['Global']['use_ccghq_timeshifted_rarity_color']
    if isinstance(user_input, bool):
        return user_input
    if user_input == "auto":
        if Path(self.template_file_name).stem == "ancient":
            return self.layout.set.upper() in post_ancient_sets
        else:
            return False

def decision_to_use_1993_frame(self):
    user_input = self.config_json['Ancient']['use_1993_frame']
    if isinstance(user_input, bool):
        return user_input
    if user_input == "auto":
        return self.layout.set.upper() in pre_mirage_sets



"""
HELPER FUNCTIONS
"""

def apply_custom_collector(self, set_layer, userstring: str = None):
    """
    Applies collector's info to the set layer, in a user-defined format, using a mix of variables and free text.
    The variables are:
    <PrintYear>
    <Set>
    <CollectorNumber>
    <CardCount>
    <Rarity>
    For example:
    "<PrintYear> Proxy • Not for Sale • <Set> <CollectorNumber>/<CardCount> <Rarity>"
    Will produce something like:
    2004 Proxy • Not for Sale • DST 140/165 U
    If any collector info is missing, it will simply be omitted.
    """
    # Set default userstring if none is provided
    if not userstring:
        userstring = ""
    # Retrieve collector's info if it exists
    if "<PrintYear>" in userstring:
        try:
            PrintYear = self.layout.scryfall['released_at'][:4]
        except:
            PrintYear = ""
        userstring = userstring.replace("<PrintYear>", PrintYear)
    if "<Set>" in userstring:
        try:
            Set = self.layout.set
        except:
            Set = ""
        userstring = userstring.replace("<Set>", Set)
    if "<CollectorNumber>" in userstring:
        try:
            CollectorNumber = str(self.layout.collector_number).lstrip("0")
        except:
            CollectorNumber = ""
        userstring = userstring.replace("<CollectorNumber>", CollectorNumber)
    if "<CardCount>" in userstring:
        try:
            CardCount = str(self.layout.card_count).lstrip("0")
        except:
            CardCount = ""
        userstring = userstring.replace("<CardCount>", CardCount)
    if "<Rarity>" in userstring:
        try:
            Rarity = self.layout.rarity_letter
        except:
            Rarity = ""
        userstring = userstring.replace("<Rarity>", Rarity)
    # Get rid of all leading, trailing, and double spaces in userstring
    userstring = " ".join(userstring.split()).lstrip().rstrip()
    # Replace asterisks with thick dots
    userstring = userstring.replace("*", "•")
    # Apply the collector info
    set_layer.textItem.contents = userstring

def _apply_custom_collector(self, set_layer):
    """
    Applies collector's info to the set layer, in the FelixVita custom format:
    <PrintYear> Proxy • Not for Sale • <Set> <CollectorNumber>/<CardCount> <Rarity>
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

def left_align_artist_and_collector(self):
    """ Left-align the artist and collector info """
    reference = psd.getLayer("Left-Aligned Artist Reference", con.layers['LEGAL'])
    artist = psd.getLayer(con.layers['ARTIST'], con.layers['LEGAL'])
    collector = psd.getLayer(con.layers['SET'], con.layers['LEGAL'])
    artist_delta = reference.bounds[0] - artist.bounds[0]
    collector_delta = reference.bounds[0] - collector.bounds[0]
    artist.translate(artist_delta, 0)
    collector.translate(collector_delta, 0)

def felix_set_symbol_logic(self):
    if not hasattr(self, "expansion_disabled") or (hasattr(self, "expansion_disabled") and self.expansion_disabled == False):
        expansion_symbol = psd.getLayer(con.layers['EXPANSION_SYMBOL'], con.layers['TEXT_AND_ICONS'])
        if decision_to_have_set_symbol(self) is False:
            skip_symbol_formatting(self)
            expansion_symbol.visible = False
        else:
            if decision_to_use_ccghq_symbol(self):
                try:
                    if not cfg.dev_mode:
                        console.update("Attempting use CCGHQ set symbol...")
                    use_common_rarity_color = not decision_to_use_ccghq_symbol_rarity(self)
                    use_timeshifted_rarity_color = decision_to_use_timeshifted_rarity_for_ccghq(self)
                    set_symbol_layer = load_symbol_svg(self, use_common_rarity_color, use_timeshifted_rarity_color)
                    skip_symbol_formatting(self)
                    reassign_symbol_reference(self, set_symbol_layer)
                    expansion_symbol.visible = False
                    frame_set_symbol_layer(set_symbol_layer)
                    apply_set_specific_svg_symbol_adjustments(self, set_symbol_layer)
                except:
                    if not cfg.dev_mode: console.update("CCGHQ SVG failed to load. Defaulting to regular Proxyshop approach...")
                    pass
            else:
                # frame_set_symbol_layer(self, expansion_symbol)
                apply_set_specific_keyrune_symbol_adjustments(self, expansion_symbol)

def load_symbol_svg(self, no_rarity: bool = False, timeshifted: bool = False):
    # Get rarity
    ccghq_rarity_abbreviations = {
        "Common": "C",
        "Uncommon": "U",
        "Rare": "R",
        "Mythic": "M",
        "Mythic Rare": "M",
        "Special": "S",
        "Basic Land": "L",
        "Timeshifted": "T",
        "Masterpiece": "M",
    }
    svg_rarity = ccghq_rarity_abbreviations[self.layout.rarity.title()]
    if no_rarity:
        svg_rarity = "C"
    if timeshifted:
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

def import_custom_symbols_json(layout):
    """
    Replace the imported contents of symbols.json with that of plugins/FelixVita/symbols.json
    """
    with open(Path(Path(__file__).parent.resolve(), "symbols.json"), "r", encoding="utf-8-sig") as js:
        con.set_symbols = json.load(js)
    # Automatic set symbol enabled?
    if cfg.auto_symbol:
        if layout.set in con.set_symbols:
            layout.symbol = con.set_symbols[layout.set]
        else: layout.symbol = cfg.symbol_char
    else: layout.symbol = cfg.symbol_char

def skip_symbol_formatting(self):
    """ Skip the default Proxyshop symbol formatting (stroke, fill, etc.) """
    self.tx_layers = [_ for _ in self.tx_layers if not isinstance(_, ExpansionSymbolField)]

def reassign_symbol_reference(self, new_layer):
    """
    Reassign the Typeline text field's expansion symbol reference to a different layer.
    This is needed in order to make the automatic sizing of the typeline to work properly, as it uses the expansion symbol's bounds to determine the typeline's width.
    """
    for lay in self.tx_layers:
        if lay.layer.name == 'Typeline':
            lay.reference = new_layer

def frame_set_symbol_layer(set_symbol_layer):
    # Resize and position the set symbol
    expansion_reference = psd.getLayer(con.layers['EXPANSION_REFERENCE'], con.layers['TEXT_AND_ICONS'])
    psd.frame_layer(set_symbol_layer, expansion_reference, anchor=ps.AnchorPosition.MiddleRight, smallest=True, align_h=False, align_v=True)
    psd.align("AdRg", set_symbol_layer, expansion_reference); psd.clear_selection()
    # font_symbol = psd.getLayer(con.layers['EXPANSION_SYMBOL'], con.layers['TEXT_AND_ICONS'])
    # psd.frame_layer(font_symbol, expansion_reference, anchor=ps.AnchorPosition.MiddleRight, smallest=True, align_h=True, align_v=True)
    print("Debug breakpoint here")

def normalplus_collector_fix(self):
    """
    Fix for issue where cardnum > card_count in collector's info.
    While arguably an improvement, this fix is still a bit heavy-handed, as it will also affect cards like [[Super Secret Tech (UNH)]] which ARE supposed to have a cardnum > card_count.
    Intended only for use with templates using the M15 frame.
    """
    if int(self.layout.collector_number) > int(self.layout.card_count):
        collector_layer = psd.getLayerSet(con.layers['COLLECTOR'], con.layers['LEGAL'])
        collector_top = psd.getLayer(con.layers['TOP_LINE'], collector_layer).textItem
        collector_top.contents = self.layout.collector_number + 10 * " " + self.layout.rarity_letter

def normalplus_bottom_right_text(self):
    """
    Adds a "BS & Copyleft" copyright line to the bottom right of the card, for a slightly more authentic look at a glance.
    The line includes the release year of the set (if available), which is useful as a piece of collector's info.
    Intended only for use with templates using the M15 frame.
    """
    custom_collector_string = self.config_json['Normal']['custom_collector_string']
    enable_mock_copyright = self.config_json['Global']['enable_mock_copyright']
    if not custom_collector_string and not enable_mock_copyright:
        return
    copyleft_dirpath = Path("templates", "FelixVita", "bscopyleft.psb")
    app.activeDocument.activeLayer = psd.getLayer("Set", con.layers['LEGAL'])
    emb = flx.place_embedded(str(copyleft_dirpath.resolve()))
    psd.getLayer("Set", con.layers['LEGAL']).visible = False
    vertical_ref = "Bottom" if self.is_creature else "Top"
    psd.align_vertical(emb, psd.getLayer(vertical_ref, (con.layers['LEGAL'], con.layers['COLLECTOR']))); psd.clear_selection()
    flx.convert_to_layers()
    emb_group = psd.getLayer(f"{copyleft_dirpath.stem} - Smart Object Group", con.layers['LEGAL'])
    emb_set = psd.getLayer("Set", emb_group)
    # disable mock copyright if disabled in config.json
    if not enable_mock_copyright:
        tmc = psd.getLayer("BS & Copyleft", emb_group)
        psd.getLayer("BS &", tmc).visible = False
        psd.getLayer("Copyleft", tmc).visible = False
    apply_custom_collector(self, emb_set, userstring=custom_collector_string)
    psd.align("AdRg", emb_group, psd.getLayer("Textbox Reference", "Text and Icons")); psd.clear_selection()

def inventionplus_rules_box_gradient_fix():
    """
    Places an orange gradient inside the rules box.
    This is intended to be used for Kaladesh Invention cards, since the current "masterpiece.psd" file doesn't have one.
    """
    orange_path = Path("templates", "FelixVita", "mps_rules_box_orange_gradient.psb")
    app.activeDocument.activeLayer = psd.getLayer("Shadows")
    emb = flx.place_embedded(str(orange_path.resolve()))
    flx.convert_to_layers()
    emb_group = psd.getLayer(f"{orange_path.stem}")
    psd.getLayer("CanvasSize", emb_group).visible = False

def tombstone_decision_matrix(self) -> bool:
    decision = (
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
        )
    return decision

def art_position_memory(self):
    # Find the CSV file or create it (plus folders) if it doesn't exist.
    csv_folder = "memorized-art-positions"
    csv_name = os.path.splitext(self.template_file_name.split('/')[-1])[0] + ".csv"
    csv_expected_path = os.path.join(os.path.dirname(self.layout.file), csv_folder, csv_name)
    csv_exists = os.path.exists(csv_expected_path)
    if not csv_exists:
        os.makedirs(os.path.dirname(csv_expected_path), exist_ok=True)
        with open(csv_expected_path, 'w') as f:
            pass
    # Grab all csv data and save to var
    self.art_pos_data = []
    self.current_art_pos_idx = None
    with open(csv_expected_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            self.art_pos_data.append(row)
    # Iterate through all rows of the CSV to find the first row that matches the current card
    self.current_art_pos_entry_exists = None
    current_art_pos = None
    duplicate_csv_entries = []
    for row_num,row_content in enumerate(self.art_pos_data):
        # If the art filename of the current row matches that of the card currently being rendered, save the row number and the art position IF this is the first occurence. Delete any subsequent matching rows as duplicates.
        if row_content['filename'] == os.path.basename(self.layout.file):
            if not current_art_pos:
                current_art_pos = tuple([float(_) for _ in [row_content['x'], row_content['y'], row_content['w'], row_content['h']]])
                self.current_art_pos_idx = row_num
                self.current_art_pos_entry_exists = True
            else:
                console.update("Found duplicate entry in art position memory CSV!")
                duplicate_csv_entries.append(row_num)
    if duplicate_csv_entries:
        console.update("Deleting duplicate entries...")
        for idx in sorted(duplicate_csv_entries, reverse=True):
            del self.art_pos_data[idx]
    # Use the retrieved art position to align & resize the art layer. Note: This does not support 'stretching' art (as in changing its aspect ratio).
    if self.current_art_pos_entry_exists:
        console.update("Aligning & resizing art using memorized values from CSV (no stretching)...")
        x,y,w,h = current_art_pos
        layer = self.art_layer
        anchor = ps.AnchorPosition.TopLeft
        layer_dim = psd.get_layer_dimensions(layer)
        ref_dim = dict(zip(('width', 'height'), (w, h)))
        if layer_dim != ref_dim:
            scale = 100 * max((ref_dim['width'] / layer_dim['width']), (ref_dim['height'] / layer_dim['height']))
            layer.resize(scale, scale, anchor)
        # Align the layer
        layer.translate(x-layer.bounds[0], y-layer.bounds[1])
    elif not decision_to_memorize_new_art_position(self):
        console.update("No memorized art position found. (To memorize new positions, you must enable the option 'art_position_memorize_new' in config.json).")

    if decision_to_memorize_new_art_position(self) and not cfg.dev_mode:
        # Set art layer to be the active layer, because this this will now make it super quick to detect if an image does not fully fill the frame (if you have "Show Transform Controls" enabled)
        app.activeDocument.activeLayer = self.art_layer
        # Trigger a manual edit mode
        console.wait("New memorization of art positions is enabled. Please make your adjustments, then click continue...")
        console.update(f"Saving art position to memorized-art-positions/{Path(csv_expected_path).name} in same folder as your art...")
        # Update posData values based on current art position
        new_x, new_y = self.art_layer.bounds[:2]
        new_w,new_h = tuple([psd.get_layer_dimensions(self.art_layer).get(key) for key in ['width', 'height']])
        updatedArtPos = {'filename': os.path.basename(self.layout.file), 'x': new_x, 'y': new_y, 'w': new_w, 'h': new_h}
        # Update the art_post_data var at the correct index
        if self.current_art_pos_entry_exists:
            self.art_pos_data[self.current_art_pos_idx] = updatedArtPos
        else:
            self.art_pos_data.append(updatedArtPos)
        # Update the csv file
        with open(csv_expected_path, 'w', newline='') as csvfile:
            fieldnames = ['filename', 'x', 'y', 'w', 'h']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.art_pos_data:
                writer.writerow(row)

def use_premium_star_in_coll_info_where_appropriate(self):
    if decision_to_use_premium_star_between_set_and_lang(self):
        collector_bottom = psd.getLayer("Bottom", ("Legal", "Collector"))
        # psd.replace_text(collector_bottom, "•", "µ∂∑∏∫¬≈")
        console.update("Changing of dot to star is not yet implemented (WIP).")

unsupported_chars_dict = {
    "á": "a",  # Example: "Marton Stromgald"
    "û": "u",  # Example: "Ring of Ma'ruf"
    "ǵ": "g",  # Example: "Volkan Baga" (Artist)
    }

def felix_fix_unsupported_chars(text):
    for bad_char, good_char in unsupported_chars_dict.items():
        text = text.replace(bad_char, good_char)
    return text

def felix_fix_unsupported_chars_in_cardname(self):
    """
    Use this in the basic_text_layers() method, prior to calling super().basic_text_layers().
    Seems to only be necessary with templates using the font "" (i.e. NormalClassic class).
    """
    for lay in self.tx_layers:
        if lay.layer.name == "Card Name":
            if any(bad_char in lay.contents for bad_char in unsupported_chars_dict.keys()):
                lay.contents = felix_fix_unsupported_chars(lay.contents)

def felix_fix_unsupported_chars_in_artist_name(self):
    """
    Use this at any point prior to the execution of the collector_info() method.
    Seems to only be necessary with templates using the font "Magic:the Gathering" (i.e. Normal class, but not Modern)
    """
    self.layout.artist = felix_fix_unsupported_chars(self.layout.artist)


"""
HELPERS FOR SET-SPECIFIC SYMBOL ADJUSTMENTS
"""

def apply_set_specific_keyrune_symbol_adjustments(self, expansion_symbol):
    if self.layout.set.upper() == "ATQ":
        expansion_symbol.resize(112, 112)
        expansion_symbol.translate(-200, -20)
        skip_symbol_formatting(self)
    elif self.layout.set.upper() == "DRK":
        expansion_symbol.translate(30, 10)
        skip_symbol_formatting(self)
        if self.layout.background == "B":
            psd.apply_stroke(expansion_symbol, 2, psd.get_rgb(133, 138, 153))
    elif self.layout.set.upper() == "HML":
        skip_symbol_formatting(self)
        app.activeDocument.activeLayer = expansion_symbol
        # expansion_symbol.resize(105, 105)
        expansion_symbol.translate(0, -5)
        psd.fill_expansion_symbol(expansion_symbol, psd.get_rgb(186, 186, 186))  # Gray
        expansion_mask = psd.getLayer("Expansion Mask", con.layers['TEXT_AND_ICONS'])
        psd.apply_stroke(expansion_mask, 5, psd.rgb_white())
        # expansion_mask.translate(0, -5)
    elif self.layout.set.upper() == "MIR":
        skip_symbol_formatting(self)
        psd.apply_stroke(expansion_symbol, 9, psd.rgb_white())
    elif self.layout.set.upper() == "VIS":
        skip_symbol_formatting(self)
        frame_set_symbol_layer(self, expansion_symbol)
        psd.fill_expansion_symbol(expansion_symbol, psd.rgb_white())
    else:
        # Tested for the following sets: TOR,
        expansion_symbol.translate(-30, 0)

def apply_set_specific_svg_symbol_adjustments(self, svg_symbol):
    if self.layout.set.upper() == "ALL":
        svg_symbol.translate(-90,0)
    elif self.layout.set.upper() == "LEG":
        scale = 0.9
        svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
        svg_symbol.translate(30, 10)
    elif self.layout.set.upper() == "FEM":
        scale = 0.75
        svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
        svg_symbol.translate(23, -15)
    elif self.layout.set.upper() == "ICE":
        scale = 0.8
        svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
        svg_symbol.translate(0, -10)
    elif self.layout.set.upper() == "WTH":
        svg_symbol.translate(-30, 0)
    elif self.layout.set.upper() == "TMP":
        psd.apply_stroke(svg_symbol, 6, psd.rgb_white())
        scale = 0.85
        svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
        svg_symbol.translate(-35,4)
    elif self.layout.set.upper() == "STH":
        psd.apply_stroke(svg_symbol, 3, psd.rgb_white())
        scale = 0.75
        svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
        svg_symbol.translate(-30,0)
    elif self.layout.set.upper() == "PTK":
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
    elif self.layout.set.upper() in ["SCG"]:
        psd.apply_stroke(svg_symbol, 3, psd.rgb_white())
    elif self.layout.set.upper() in ["EXO", "UDS", "S99"]:
        psd.apply_stroke(svg_symbol, 4, psd.rgb_white())
    elif self.layout.set.upper() in ["INV"]:
        psd.apply_stroke(svg_symbol, 6, psd.rgb_white())
    elif self.layout.set in post_ancient_sets and decision_to_use_timeshifted_rarity_for_ccghq(self):
        psd.apply_stroke(svg_symbol, 5, psd.rgb_white())
    # Resize
    if self.layout.set.upper() in ["NEM", "MMQ", "EXO", "LGN"]:
        scale = 0.9
        svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
    elif self.layout.set.upper() in ["ONS"]:
        scale = 0.95
        svg_symbol.resize(scale*100, scale*100, ps.AnchorPosition.MiddleRight)
    # Vertical shift
    if self.layout.set.upper() in ["JUD", "LGN", "NEM"]:
        svg_symbol.translate(0, -5)
    # Horizontal shift
    if self.layout.set.upper() in ["EXO", "UDS", "SCG", "S99", "TOR"]:
        svg_symbol.translate(-30,0)
    elif self.layout.set.upper() in []:
        svg_symbol.translate(-25,0)
    elif self.layout.set.upper() in ["JUD", "LGN", "PCY", "MMQ", "ODY", "PLS"]:
        svg_symbol.translate(-15,0)
    elif self.layout.set.upper() in ["ONS", "APC", "NEM"]:
        svg_symbol.translate(-10,0)
    elif self.layout.set.upper() in ["ULG", "USG", "PLS"]:
        pass

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



"""
NORMALPLUS TEMPLATE
"""
# TODO: Improve set symbol faithfulness for the following sets:
# AFC: The color inside should be white, not black, for cards like [[Mind Stone]]

class NormalPlusTemplate(temp.NormalTemplate):
    """
    FelixVita's minor modifications to MrTeferi's Normal template.
    - Adds functionality to use SVGs (e.g. from CCGHQ) in place of the set symbols normally generated by Proxyshop.
    - Adds an optional "BS & Copyleft" copyright line to the bottom right of the card, for a slightly more authentic look at a glance.
    - Fixes the collector's info for cards like [[Mind Stone (AFC)]] by hiding card count whenever collector number is greater than card count.)
    """
    template_file_name = "normal.psd"
    template_suffix = "NormalPlus"

    def __init__(self, layout):
        self.config_json = config_json
        import_custom_symbols_json(layout)
        cfg.flavor_divider = decision_to_use_flavor_divider(self, layout)
        super().__init__(layout)

    def basic_text_layers(self, text_and_icons):
        super().basic_text_layers(text_and_icons)
        felix_fix_unsupported_chars_in_cardname(self)
        felix_set_symbol_logic(self)
        felix_fix_unsupported_chars_in_artist_name(self)

    def post_text_layers(self):
        normalplus_collector_fix(self)
        normalplus_bottom_right_text(self)
        art_position_memory(self)
        use_premium_star_in_coll_info_where_appropriate(self)

class MiraclePlusTemplate(temp.MiracleTemplate):
    """
    FelixVita's NormalPlus template, but for Miracle cards.
    """
    template_file_name = "miracle"

    def __init__(self, layout):
        self.config_json = config_json
        import_custom_symbols_json(layout)
        cfg.flavor_divider = decision_to_use_flavor_divider(self, layout)
        super().__init__(layout)

    def basic_text_layers(self, text_and_icons):
        super().basic_text_layers(text_and_icons)
        felix_fix_unsupported_chars_in_cardname(self)
        felix_set_symbol_logic(self)
        felix_fix_unsupported_chars_in_artist_name(self)

    def post_text_layers(self):
        normalplus_collector_fix(self)
        normalplus_bottom_right_text(self)
        art_position_memory(self)
        use_premium_star_in_coll_info_where_appropriate(self)

class InventionPlusTemplate(temp.InventionTemplate):
    """
    FelixVita's NormalPlus template, but for Kaladesh Invention cards.
    """
    template_file_name = "masterpiece.psd"
    template_suffix = "Masterpiece"

    def __init__(self, layout):
        self.config_json = config_json
        import_custom_symbols_json(layout)
        cfg.flavor_divider = decision_to_use_flavor_divider(self, layout)
        super().__init__(layout)
        inventionplus_rules_box_gradient_fix()

    def basic_text_layers(self, text_and_icons):
        super().basic_text_layers(text_and_icons)
        felix_fix_unsupported_chars_in_cardname(self)
        felix_set_symbol_logic(self)
        felix_fix_unsupported_chars_in_artist_name(self)

    def post_text_layers(self):
        normalplus_collector_fix(self)
        normalplus_bottom_right_text(self)
        art_position_memory(self)
        use_premium_star_in_coll_info_where_appropriate(self)

"""
MODERN TEMPLATE
"""
# TODO: Improve set symbol faithfulness for the following sets:
# THS: Stroke should be white, not black.
# BNG: Stroke should be white, not black.
# Add tombstone icon (some modern cards do actually have it)

class ModernTemplate (temp.NormalTemplate):
    """
    FelixVita's Modern template (The 8th Edition / Pre-M15 frame)

    Mostly based on MrTeferi's Normal template, with the following changes:
    - Square frame instead of rounded corners
    - Bottom part of the card frame is added back in
    - Added Artist & Collector Info in the modern frame style (paintbrush icon, mock copyright, etc.)
    - Added masks to the nyxtouched cards to make the starry frame effect only go about halfway down the card
    """
    template_file_name = "FelixVita/modern.psd"
    template_suffix = "Modern"

    def __init__(self, layout):
        self.config_json = config_json
        import_custom_symbols_json(layout)
        cfg.flavor_divider = decision_to_use_flavor_divider(self, layout)
        super().__init__(layout)

    def enable_frame_layers(self):
        super().enable_frame_layers()

    def collector_info(self):
        # Layers we need
        set_layer = psd.getLayer("Set", self.legal_layer)
        artist_layer = psd.getLayer(con.layers['ARTIST'], self.legal_layer)

        # Fill set info / artist info
        apply_custom_collector(self, set_layer, userstring=self.config_json['Modern']['custom_collector_string'])
        psd.replace_text(artist_layer, "Artist", self.layout.artist)

        # Make text white for Lands and Black cards
        if self.layout.background in ["Land", "B"]:
            psd.getLayer("Invert Legal Color").visible = True

    def basic_text_layers(self, text_and_icons):
        super().basic_text_layers(text_and_icons)
        felix_fix_unsupported_chars_in_cardname(self)
        felix_set_symbol_logic(self)

    def post_text_layers(self):
        art_position_memory(self)

class AncientTemplate (temp.NormalClassicTemplate):
    """
    FelixVita's template
    """
    template_file_name = "FelixVita/ancient.psd"
    template_suffix = "Ancient"

    def __init__(self, layout):
        self.config_json = config_json
        import_custom_symbols_json(layout)
        cfg.flavor_divider = decision_to_use_flavor_divider(self, layout)
        super().__init__(layout)

        # # For Portal sets, use bold rules text and flavor divider:
        # if layout.set.upper() in portal_frame_sets:
        #     con.font_rules_text = "MPlantin-Bold"
        # else: cfg.flavor_divider = False
        # Right-justify citations in flavor text for all sets starting with Mirage
        if layout.set.upper() not in pre_mirage_sets:
            con.align_classic_quote = True

        self.frame_style = "CardConRemastered-97"
        if decision_to_use_1993_frame(self):
            if self.is_land or self.layout.background == "Gold":
                self.frame_style = "Mock-93"  # Because ancient.psd doesn't yet have an asset for the 1993 multicolor frame or 1993 land frame
            else:
                self.frame_style = "Real-93"

    def basic_text_layers(self, text_and_icons):

        if self.frame_style == "Real-93":
            # Make the rules text narrower
            rtext = psd.getLayer("Rules Text", con.layers['TEXT_AND_ICONS'])
            tref = psd.getLayer("Textbox Reference", con.layers['TEXT_AND_ICONS'])
            tref.resize(95, 100, ps.AnchorPosition.MiddleCenter)
            rtext.textItem.width = 110
            psd.align_horizontal(rtext, tref); psd.clear_selection()
            tref.visible = False

        super().basic_text_layers(text_and_icons)
        felix_fix_unsupported_chars_in_cardname(self)
        felix_set_symbol_logic(self)

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


    def collector_info(self):
        setcode = self.layout.set.upper()
        color = self.layout.background
        legal_layer = psd.getLayerSet(con.layers['LEGAL'])

        # Artist layer & set/copyright/collector info layer
        collector_layer = psd.getLayer(con.layers['SET'], legal_layer)
        artist_layer = psd.getLayer(con.layers['ARTIST'], legal_layer)
        tmc = psd.getLayer("BS & Copyleft", legal_layer)
        tm_layer = psd.getLayer("BS &", tmc)
        c_layer = psd.getLayer("Copyleft", tmc)
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
            tm_layer.textItem.color = psd.rgb_black()
            c_layer.textItem.color = psd.rgb_black()

        if self.config_json['Global']['thicker_collector_info']: psd.apply_stroke(collector_layer, 1, psd.get_text_layer_color(collector_layer))

        if self.layout.set.upper() in pre_legends_sets and self.layout.background == "B":
            # Turn collector info grey and clear layer style  # TODO: Test this
            # gray = psd.get_rgb(133, 138, 153)  # Gray for Alpha
            gray = flx.rgb_hex("acb0bc")  # Gray for Alpha
            collector_layer.textItem.color = gray
            tm_layer.textItem.color = gray
            c_layer.textItem.color = gray
            psd.clear_layer_style(collector_layer)  # To get rid of inner glow
            psd.clear_layer_style(tm_layer)  # To get rid of inner glow
            psd.clear_layer_style(c_layer)  # To get rid of inner glow
            if self.config_json['Global']['thicker_collector_info']: psd.apply_stroke(collector_layer)

        # Fill in detailed collector info if available ("SET • 999/999 C" --> "ABC • 043/150 R")
        # collector_layer.visible = True  # Probably not needed? Hence commented out.
        apply_custom_collector(self, collector_layer, userstring=self.config_json['Ancient']['custom_collector_string'])

        # Remove "BS & Copyleft" layer if user has disabled mock copyright in config.json
        if not self.config_json['Global']['enable_mock_copyright']:
            tm_layer.visible = False
            c_layer.visible = False

        # For old cards (pre-Mirage), left-justify the artist and collector info (and remove trademark symbol)
        if self.layout.set.upper() in pre_exodus_sets + ["P02", "PTK"]:
            tm_layer.visible = False
            coll_combo = psd.merge_layers(collector_layer, tmc)
            lalign_ref = psd.getLayer("Left-Aligned Artist Reference", con.layers['LEGAL'])
            psd.align("AdLf", coll_combo, lalign_ref); psd.clear_selection()
            psd.align("AdLf", artist_layer, lalign_ref); psd.clear_selection()

        else:
            # Center-align the collector info
            tref = psd.getLayer("Textbox Reference", con.layers['TEXT_AND_ICONS'])
            coll_combo = psd.merge_layers(collector_layer, tmc)
            psd.align("AdCH", coll_combo, tref); psd.clear_selection()
            psd.align("AdCH", artist_layer, tref); psd.clear_selection()



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

        # Tombstone icon in upper left corner
        self.tombstone = None
        if "tombstone" in self.layout.frame_effects:
            self.tombstone = True
        elif self.config_json['Global']['smart_tombstone'] and tombstone_decision_matrix(self):
            self.tombstone = True
        if self.tombstone:
            psd.getLayer("Tombstone", con.layers['TEXT_AND_ICONS']).visible = True

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
        # Misc post-text steps for 1993 frame
        if self.frame_style == "Real-93" and self.layout.set.upper() in pre_mirage_sets:
            if self.layout.power is not None or self.layout.toughness is not None:
                # Use non-bold MPlantin for the Power and Toughness text
                pt = psd.getLayer("Power / Toughness", con.layers['TEXT_AND_ICONS'])
                pt.textItem.font = "MPlantin"
                pt.textItem.size = 10
                pt.translate(0, -30)
            # Shift the cardname slightly left
            if not self.tombstone:
                psd.getLayer("Card Name", "Text and Icons").translate(-100,0)
            # Color the white text grey for old cards
            if self.layout.set.upper() in pre_legends_sets:
                gray = psd.get_rgb(186, 186, 186)  # Gray
                if self.layout.set.upper() in ['LEA', 'LEB'] or (self.layout.background == "W" and self.layout.set.upper() in ['ARN', 'ATQ']):
                    # gray = psd.get_rgb(133, 138, 153)  # Gray for Alpha
                    gray = flx.rgb_hex("acb0bc")  # Gray for Alpha
                    if self.layout.background == "W":
                        gray = flx.rgb_hex("9a9eaa")  # Gray for Alpha
                white_text_layers = [
                    psd.getLayer("Card Name", con.layers['TEXT_AND_ICONS']),
                    psd.getLayer("Typeline", con.layers['TEXT_AND_ICONS']),
                    psd.getLayer("Artist", con.layers['LEGAL']),
                ]
                if self.is_creature:
                    white_text_layers.append(psd.getLayer("Power / Toughness", con.layers['TEXT_AND_ICONS']))
                for layer in white_text_layers:
                    layer.textItem.color = gray
                    if self.layout.set.upper() in ['LEA', 'LEB']:
                        flx.hide_style_inner_glow(layer)
                    if self.layout.set.upper() == "ATQ" and self.layout.rarity != "C":
                        pass  # TODO: Change color of inner glow to orange/yellow
                if self.layout.set.upper() in ["LEA", "LEB"]:
                    # Reveal "Border with Dots" by hiding the layers obscuring it
                    psd.getLayer("Border").visible = False
                    psd.getLayer("Extended Black Backdrop", "Frame backdrop").visible = False
                    if self.layout.background in ["W", "R"]:
                        sback = self.layout.background
                        # Use a slightly more pink version of the red frame, or softer version of the white frame
                        psd.getLayer("LEA", ("Nonland", sback, "Real-93")).visible = True
        art_position_memory(self)
