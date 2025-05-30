"""tagGenerator.py: Generate an stl file for a 3D-printable tag"""

import argparse
import cadquery as cq
from cadquery.func import *
from cadquery.vis import show


class PrintTag:
    """Definition of the Print Tag model"""
    def __init__(self,
                 textString: str = "<text>",
                 width: float = 2.0,
                 height: float = 1.0,
                 thickness: float = 0.125,
                 emboss_depth: float = 0.0625,
                 font_height: float = 0.5,
                 hole_diameter: float = 0.125,
                 fillet_radius: float = 0.125):

        # Tag geometry
        # -- Rectangle
        tag = cq.Workplane("ZY")
        tag = tag.box(height, width, thickness)
        # -- Semicircle on the left side
        extracircle = cq.Workplane("ZY").cylinder(thickness, 0.5 * height).translate((0,-0.5 * width,0))
        tag += extracircle
        # -- Filleted edges
        tag = tag.edges("|X").fillet(fillet_radius)

        # Hole cutout
        hole = cq.Workplane("ZY")
        hole = hole.cylinder(thickness, 0.5 * hole_diameter)
        # -- Move to the old left edge / center of the left circle
        hole = hole.translate((0, -0.5 * width, 0))

        # Text
        embossed_text = cq.Workplane("YZ").text(textString, font_height, emboss_depth, kind="bold")

        # Cuts
        tag -= hole
        tag -= embossed_text

        # Final body
        self.body = tag


def parseArgs():
    """Parse the arguments for the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument("text",     help="The text to be shown on the tag",           default="MM.DD.YY | MM:SS")
    parser.add_argument("filename", help="The .STL filename to save the tag to",      default="tag.stl")
    parser.add_argument("--noshow", help="Don't show the model before exporting", action="store_true")
    parser.add_argument("--width",        type=float, help="Tag width            (in)", default = 2.0)
    parser.add_argument("--height",       type=float, help="Tag height           (in)", default = 1.0)
    parser.add_argument("--thickness",    type=float, help="Tag thickness        (in)", default = 0.125)
    parser.add_argument("--embossdepth",  type=float, help="Text emboss depth    (in)", default = 0.0625)
    parser.add_argument("--fontheight",   type=float, help="Text height          (in)", default = 0.5)
    parser.add_argument("--holediameter", type=float, help="Mount hole diameter  (in)", default = 0.125)
    parser.add_argument("--filletradius", type=float, help="Corner fillet radius (in)", default = 0.125)
    args = parser.parse_args()
    return args


def main():
    """Main execution"""
    args = parseArgs()
    tag = PrintTag(
        textString = args.text,
        width = args.width,
        height = args.height,
        thickness = args.thickness,
        emboss_depth = args.embossdepth,
        font_height = args.fontheight,
        hole_diameter = args.holediameter,
        fillet_radius = args.filletradius
    )
    if not args.noshow:
        show(tag.body)
    tag.body.export(args.filename)
    return


if __name__ == "__main__":
    main()
