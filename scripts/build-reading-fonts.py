"""Build local Latin subsets: uv run --with 'fonttools[woff]==4.68.0' python scripts/build-reading-fonts.py."""

from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

from fontTools import subset
from fontTools.ttLib import TTFont

SOURCE = "https://raw.githubusercontent.com/adobe-fonts/source-sans/87b37a2daaed80fcb8e8ccb0085c4d72ddade12e/WOFF2/VF/"
DEST = Path(__file__).resolve().parents[1] / "rnp/static/fonts/source-sans-3"
UNICODES = "U+0000-017F,U+0300-036F,U+2000-206F,U+20AC,U+2122,U+2190-2193,U+2212"

for style, upstream in [("upright", "Upright"), ("italic", "Italic")]:
    with urlopen(f"{SOURCE}SourceSans3VF-{upstream}.ttf.woff2") as response:
        font = TTFont(BytesIO(response.read()))
    # Adobe reserves 'Source'; give the derived font a distinct family name.
    for record in font["name"].names:
        if record.nameID in {1, 3, 4, 6, 16, 21, 25}:
            text = record.toUnicode()
            text = text.replace("Source Sans 3", "RNP Sans").replace(
                "SourceSans3", "RNPSans"
            )
            record.string = text.encode(record.getEncoding())
    options = subset.Options()
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=subset.parse_unicodes(UNICODES))
    subsetter.subset(font)
    font.flavor = "woff2"
    font.save(DEST / f"{style}.woff2")
