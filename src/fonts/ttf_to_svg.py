from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import svgwrite

def extract_char_to_svg(ttf_path, character, output_svg_path, padding=150):
    # Load the font
    font = TTFont(ttf_path)
    glyph_set = font.getGlyphSet()

    # Map character to glyph name
    cmap = font['cmap'].getBestCmap()
    char_code = ord(character)
    glyph_name = cmap.get(char_code)

    if glyph_name is None:
        raise ValueError(f"Character {character} not found in font.")

    glyph = glyph_set[glyph_name]

    # Extract path
    pen = SVGPathPen(glyph_set)
    glyph.draw(pen)
    path_data = pen.getCommands()

    # Extract bounding box
    bounds_pen = BoundsPen(glyph_set)
    glyph.draw(bounds_pen)
    xMin, yMin, xMax, yMax = bounds_pen.bounds

    # Add padding
    viewbox_x = xMin
    viewbox_y = yMin
    width = (xMax - xMin)
    height = (yMax - yMin)

    # Create SVG
    dwg = svgwrite.Drawing(
        output_svg_path,
        viewBox=f"{viewbox_x} {viewbox_y} {width} {height}"
    )

    # No scaling or extra transform needed
    dwg.add(dwg.path(d=path_data))
    dwg.save()

    print(f"Saved SVG for '{character}' with margin to: {output_svg_path}")

# Example usage
extract_char_to_svg("Symbola-13.otf", "\ufe37", "bracket.svg")