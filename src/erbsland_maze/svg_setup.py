#  Copyright © 2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from .parity import Parity
from .size import Size
from .svg_fill_mode import SvgFillMode
from .svg_unit import SvgUnit
from .svg_zero_point import SvgZeroPoint


@dataclass(frozen=True, kw_only=True)
class SvgSetup:
    """
    The setup for the SVG layout.
    """

    width: float
    """The width of the maze in mm."""

    height: float
    """The height of the maze in mm."""

    wall_thickness: float = 1.7
    """The thickness of the walls in mm."""

    side_length: float = 4.0
    """The side length of a room, *including* the wall thickness, in mm."""

    fill_mode: SvgFillMode = SvgFillMode.STRETCH_EDGE
    """The fill mode used to calculate the room sizes."""

    width_parity: Parity = Parity.ODD
    """The parity of the room count in the X axis."""

    height_parity: Parity = Parity.ODD
    """The parity of the room count in the Y axis."""

    start_end_mark: bool = True
    """If the start and end room shall be marked with a red and blue rectangle."""

    svg_unit: SvgUnit = SvgUnit.MM
    """The unit for the generated SVG file."""

    svg_dpi: float = 96.0
    """In case of PX unit, the DPI value to convert the MM values into PX."""

    svg_zero: SvgZeroPoint = SvgZeroPoint.CENTER
    """Select where the zero point of the maze shall be placed."""

    svg_background: bool = True
    """If the SVG background shall be drawn opaque."""
    
    svg_bg: list
    """Background color to render the SVG paths."""
    
    svg_fg: list
    """Foreground color to render the SVG paths."""

    def get_size(self) -> Size:
        return Size(self.width, self.height)

    def __post_init__(self):
        if not isinstance(self.width, float) or self.width < 1.0:
            raise ValueError("`width` must be a float, larger than 1.0.")
        if not isinstance(self.height, float) or self.height < 1.0:
            raise ValueError("`height` must be a float, larger than 1.0.")
        if not isinstance(self.wall_thickness, float) or self.wall_thickness < 0.1:
            raise ValueError("`wall_thickness` must be a float, larger than 0.1.")
        if not isinstance(self.side_length, float) or self.side_length < 1.0:
            raise ValueError("`side_length` must be a float, larger than 1.0.")
        if not isinstance(self.fill_mode, SvgFillMode):
            raise TypeError("`fill_mode` must be an instance of SvgFillMode.")
        if not isinstance(self.width_parity, Parity):
            raise TypeError("`width_parity` has the wrong type.")
        if not isinstance(self.height_parity, Parity):
            raise TypeError("`height_parity` has the wrong type.")
        if not isinstance(self.svg_unit, SvgUnit):
            raise TypeError("`svg_unit` has the wrong type.")
        if not isinstance(self.svg_dpi, float) or self.svg_dpi < 60 or self.svg_dpi > 10_000:
            raise ValueError("`svg_dpi` must be a float, between 60 and 10'000.")
        if not isinstance(self.svg_zero, SvgZeroPoint):
            raise TypeError("`svg_zero` has the wrong type.")
        if not isinstance(self.svg_background, bool):
            raise TypeError("`svg_background` has the wrong type.")
        if (self.side_length - self.wall_thickness) < 0.5:
            raise ValueError(
                "`side_length` and `wall_thickness` do not match, the resulting path width is smaller than 0.5 mm."
            )
        if not isinstance(self.svg_bg, list) or any(rgb_val < 0 or rgb_val > 1 for rgb_val in self.svg_bg):
            raise ValueError("`background` must be in RGB format 0.5,0.5,0.5 with all three values being between 0 and 1 inclusive.")
        if not isinstance(self.svg_fg, list) or any(rgb_val < 0 or rgb_val > 1 for rgb_val in self.svg_fg):
            raise ValueError("`foreground` must be in RGB format 0.5,0.5,0.5 with all three values being between 0 and 1 inclusive.")
