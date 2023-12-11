import cairocffi as cairo
from io import BytesIO
from PIL import Image


def convert_svg_to_png(svg_content, output_path):
    # Create a Cairo surface for rendering
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
    context = cairo.Context(surface)

    # Parse the SVG content
    surface.set_size(width=500, height=500)  # Set a reasonable size
    context.scale(1, 1)  # Adjust scaling if needed
    cairo.svg.surface_set_document(surface._surface, svg_content.encode())

    # Write the surface to a PNG file
    surface.write_to_png(output_path)

    print(f"Conversion complete. PNG saved at: {output_path}")


if __name__ == "__main__":
    # Replace 'your_svg_content' with the actual content of your SVG file
    svg_content = """
        <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
            <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
        </svg>
    """

    # Replace 'output.png' with the desired output path for the PNG file
    output_path = 'output.png'

    convert_svg_to_png(svg_content, output_path)
