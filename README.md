# Proxyshop Plugins by FelixVita

## The Ancient Template

This is what you're probably here for.

_Ancient_ is a custom plugin for [Proxyshop](https://github.com/MrTeferi/MTG-Proxyshop.git) which lets you create cards with the [old-school/classic frame](https://scryfall.com/search?q=%28frame%3A1993+or+frame%3A1997%29).

This template / plugin is my main project, and is by far the largest plugin in terms of complexity and number of lines of code.

### Examples of cards rendered using Ancient

_Content placeholder: Coming soon..._

...

...

...

## Other plugins: Modern & Normal Plus

Although developing _Ancient_ has been my primary focus, I have additionally made a few spin-offs of the default "Normal" template

### Modern

The _Modern_ template / plugin lets you create cards with the [modern frame](https://scryfall.com/search?q=frame%3Amodern+-is%3Adigital).
It is basically the same as `normal.psd` except for the following modifications:

- Bottom part of the card frame is added back in
- Square frame instead of rounded corners
- Added Artist & Collector Info in the modern frame style (paintbrush icon, mock copyright, etc.)
- Added masks to the nyxtouched cards to make the starry frame effect only go about halfway down the card
- Added [miracles](https://scryfall.com/search?q=frame%3Amiracle) frame effect
- Adds functionality to use SVGs (e.g. from CCGHQ) in place of the set symbols normally generated by Proxyshop.

### Normal Plus

The _Normal Plus_ plugin just adds some extra features to the default "Normal" template to bring its appearance even closer how the [M15 frame](https://scryfall.com/search?q=frame%3Am15+-is%3Adigital) really looks, by adding the following features:

- Adds an optional "BS & Copyleft" copyright line to the bottom right of the card, for a slightly more authentic look at a glance.
- Fixes the collector's info for cards like [[Mind Stone (AFC)]] by hiding card count whenever collector number is greater than card count.)
- Adds functionality to use SVGs (e.g. from CCGHQ) in place of the set symbols normally generated by Proxyshop.

Note that the _Normal Plus_ plugin has no accompanying custom photoshop template. It simply uses your existing `normal.psd` file. That said, if you wish to use the feature `enable_text_copyleft_proxy_not_for_sale` to place a "mock copyright" in the bottom right corner, then make sure you remember to download `bscopyleft.psb` (as explained in the instructions below).

#### Normal Plus Class: Miracle

The _Miracle Plus_ plugin does the exact same thing for the existing _Miracle_ template as _Normal Plus_ does for the _Normal_ template.

#### Normal Plus Class: Invention

The _Invention Bronze Plus_ plugin does the exact same thing for the existing _Invention Bronze_ template as _Normal Plus_ does for the _Normal_ template.
Additionally, it adds the orange gradient in the rules text box — a visual element which (as of 2022-Oct-14) is still missing from the current masterpiece.psd template.

## Instructions

### Prerequisites

Before you begin, make sure you are using the right version of Proxyshop. The FelixVita-Proxyshop-Plugins are compatible with [Proxyshop v1.1.8](https://github.com/MrTeferi/MTG-Proxyshop/releases/tag/v1.1.8)

### Installing the FelixVita plugin package

1. Go to the latest release of the plugin [here](https://github.com/HelixVita/FelixVita-Proxyshop-Plugins/releases/latest) and download it by clicking `Source code (zip)` (under "Assets").

    ![image](https://user-images.githubusercontent.com/102387379/191358011-81f4138c-8ed8-45ae-a532-17d5931a6524.png)

1. Unzip the folder and place it into your Proxyshop `plugins` folder, so that it looks something like this:

    ![image](https://user-images.githubusercontent.com/102387379/191348877-72feeadd-28c0-4002-b48d-1a83ddcab31e.png)

1. Rename it to get rid of the version number at the end, like so:

    ![image](https://user-images.githubusercontent.com/102387379/191352722-b02ab966-e3b4-4a0f-86cb-b4ac2661af1f.png)

1. Create a new folder named `FelixVita` inside the Proxyshop `templates` folder, then download [these](https://drive.google.com/drive/folders/1EqmL85czp44qWXaSpmN-DSJk430ocMkN?usp=sharing) files and place them there, like so:

    ![image](https://user-images.githubusercontent.com/102387379/193914068-3e5020e9-c823-4f09-868d-c7a2c5a06c73.png)

1. Optional (for better-looking set symbols): Create another new folder in `templates` named `CCGHQ`, then download the CCGHQ Set Symbol SVG files from [here](https://www.dropbox.com/sh/e84z5l5za99uwah/AAAKbGdgCW1uM1wZ3T128OYya?dl=0) and place them inside, so that the path looks like this:

    ![image](https://user-images.githubusercontent.com/102387379/191598378-3e36f318-6345-49e6-9be0-d210b594c387.png)

1. Run Proxyshop. You should now see "Ancient", "Modern", and "Normal Plus" (and its class variants) in the list of available templates. Enjoy!

    ![image](https://user-images.githubusercontent.com/102387379/191357752-ebe486c1-59d9-480f-bb55-639ba64a7753.png)


## A Note Regarding the CCGHQ Set Symbol SVGs

Downloading these is completely optional. All the plugins will run completely fine without it. They just make the set symbols look a bit better (imho).

When enabled, Proxyshop will attempt to use CCGHQ set symbol SVGs instead of generating set symbols using the info from `symbols.json`, except when:

- I've deemed that the Proxyshop one looks more authentic; or
- An error was encountered when attempting to load the CCGHQ SVG

Please also note that I have not yet checked every set symbol to ensure that it looks authentic. (I have thus far only done that for the sets from Alpha to Scourge, i.e. the old-school/classic frame cards relevant to the _Ancient_ template).

## Optional user configuration

You have the option to toggle certain behaviors on and off by modifying the `config.json` file, located here:

![image](https://user-images.githubusercontent.com/102387379/195993272-00d341c7-61c4-4a1e-a59a-a43be9f66905.png)

Simply open the file in Notepad and change the value of the config option you wish to modify. It'll look something like this:

![image](https://user-images.githubusercontent.com/102387379/200657597-72a23ada-162f-4c8e-98b8-005613473500.png)

### Explanation of what each configuration option means

Here is a table summarizing what each config option does.

| config option                         | description                                                                                                                                                                                                                                                            | default | behavior of the "auto" option                                                                                                           | known issues                                                                                                                                                                                              |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| art_position_memory_enabled           | automatically re-position the art using the position values from a csv file (created by using the option below); this 'memory' is linked to the art filename, so if you change that then you must either re-position it or update the filename in the csv to match     | false   | true                                                                                                                                    | none                                                                                                                                                                                                      |
| art_position_memorize_new             | pauses the proxyshop rendering process to let you manually adjust the art position in photoshop; when you click "Continue" this position will be saved in a CSV file                                                                                                   | auto    | true if 'art_position_memory_enabled" is true and no position is saved yet                                                              | none                                                                                                                                                                                                      |
| art_position_autoalign                | if enabled, the image in your art folder will be used as a guide to autoalign a higher resolution version of the same art which you have placed in a subfolder of the art folder named 'autoalign'                                                                     | auto    | true if an 'autoalign' subfolder exists and contains an art file with identical filename to the one in the art folder                   | none, but still new and experimental                                                                                                                                                                      |
| flavor_divider                        | enable flavor text separator bar for cards that have both rules text and flavor text                                                                                                                                                                                   | auto    | true for cards printed in dominaria or later if rendered with normal.psd; true for portal set cards if rendered with ancient.psd        | [portal-style divider spacing issue](https://github.com/MrTeferi/MTG-Proxyshop/issues/25)                                                                                                                 |
| use_legendary_crown                   | apply the legendary crown frame effect (introduced in Dominaria set for legendary cards); if 'smart' then legendary cards will get crowns; if 'true' then all cards will get crowns regardless of whether card is legendary; if 'false' then no cards will get crowns; | auto    | true for legendary cards from dominaria set or later                                                                                    | none                                                                                                                                                                                                      |
| use_tombstone_icon                    | enable tombstone icon in upper left corner; if 'smart', then all cards with graveyard abilities (regardless of whether the printed card actually had a tombstone)                                                                                                      | smart   | true if the real card was printed with a tombstone                                                                                      | none                                                                                                                                                                                                      |
| use_set_symbol                        | set this to 'false' to completely disable the set symbol                                                                                                                                                                                                               | auto    | true for all cards except cards from non-expansion early core sets (like Alpha, Beta, 4th Edition)                                      | none                                                                                                                                                                                                      |
| use_ccghq_set_symbols                 | attempt to use ccghq set symbol SVGs instead of the default proxyshop-generated set symbol                                                                                                                                                                             | auto    | true except for certain sets where I've made a subjective decision that the CCGHQ symbols look inferior to the Proxyshop-generated ones | none                                                                                                                                                                                                      |
| use_ccghq_set_symbol_rarity_color     | enable set symbol rarity color (silver=uncommon, gold=rare, orange=mythic rare); if set to false, the "common" rarity color will be used                                                                                                                               | auto    | true for all cards except those from pre-Exodus sets                                                                                    | none                                                                                                                                                                                                      |
| use_ccghq_timeshifted_rarity_color    | enable the timeshifted (purple) rarity set symbol color                                                                                                                                                                                                                | auto    | true for all post-Scourge cards if rendered with the _Ancient_ template (to indicate they've been "timeshifted" to the classic frame)   | none                                                                                                                                                                                                      |
| thicker_collector_info                | slightly increase thickness of the collector's info / copyright line (for readability)                                                                                                                                                                                 | false   | false                                                                                                                                   | incompatible with "enable_mock_copyright"                                                                                                                                                                 |
| enable_mock_copyright                 | adds a "BS & Copyleft" text, for a more authentic look at a glance; please don't create renders for mpcfill with this setting, as it looks "too real"                                                                                                                  | false   | false                                                                                                                                   | none                                                                                                                                                                                                      |
| use_1993_frame                        | (ancient) use the 1993 version of the classic frame instead of the default 1997 version                                                                                                                                                                                | auto    | true for cards from any pre-Mirage sets                                                                                                 | [missing land and gold frame](https://github.com/HelixVita/FelixVita-Proxyshop-Plugins/issues/9); and [inter-1993 nuances are missing](https://github.com/HelixVita/FelixVita-Proxyshop-Plugins/issues/8) |
| use_premium_star_between_set_and_lang | (normalplus) use a star instead of a dot in the bottom part of the collector's info                                                                                                                                                                                    | auto    | true if a nonfoil printing does not exist for the card in question (for example, the MPS version of Sol Ring)                           | none                                                                                                                                                                                                      |
| enable_watermark                      | apply watermark in rules text box for cards that were printed with watermarks (e.g. guild symbols, foretell watermark, etc.)                                                                                                                                           | true    | true                                                                                                                                    | not all watermarks are implemented yet                                                                                                                                                                    |

### What does true/false/auto mean?

Each config option has exactly three possible values: `true`, `false`, or `"auto"`

You must always pick one of these values. If you write something else or misspell them (for example 'True' instead of 'true'), then Proxyshop will fail.

However there are two exceptions to this rule.

### Exception 1: The "smart" value

An additional possible config value `"smart"` exists for the following config options:
-  use_tombstone_icon
-  use_legendary_crown

The idea behind this `"smart"` options is essentially: 
> "If wotc had printed the card today, it'd be printed this way"

This differs from the `"auto"` option, whose philosophy could be stated as:
> "I don't care about what the card would've looked like if reprinted by wotc; I want the card to look as close as possible to the original printing."

### Exception 2: The `custom_collector_string` option

The `custom_collector_string` option applies collector's info to the set layer, in a user-defined format, using a mix of variables and free text. The variables are

```text
<PrintYear>
<Set>
<CollectorNumber>
<CardCount>
<Rarity>
```

For example, if you're rendering `Skullclamp [DST]` and you've modified `custom_collector_string` to say

```text
<PrintYear> Joe Proxy * Not for Sanctioned Play * <Set> <CollectorNumber>/<CardCount> <Rarity>
```

Then this will produce something like:

> 2004 Joe Proxy • Not for Sanctioned Play • DST 140/165 U

and if any collector info is missing, it will simply be omitted.

## Thank you

- Magic Proxies server on Discord — for helping me get started, and for being a fantastic community
- Investigamer — for creating and maintaining Proxyshop
- lmonair — for the 1993 frame assets
- Day7 — for hosting the most up-to-date dropbox repo of CCGHQ set symbol SVGs (linked in instructions, step 5)
