"""Low-level routines for interacting with PicoDVI Output"""

from __future__ import annotations

import microcontroller

class Framebuffer:
    """A PicoDVI managed frame buffer."""

    def __init__(
        self,
        width: int,
        height: int,
        *,
        clk_dp: microcontroller.Pin,
        clk_dn: microcontroller.Pin,
        red_dp: microcontroller.Pin,
        red_dn: microcontroller.Pin,
        green_dp: microcontroller.Pin,
        green_dn: microcontroller.Pin,
        blue_dp: microcontroller.Pin,
        blue_dn: microcontroller.Pin,
        color_depth: int = 8,
    ) -> None:
        """Create a Framebuffer object with the given dimensions (640x480 or 800x480). Memory is
           allocated outside of onto the heap and then moved outside on VM
           end.

        This will change the system clock speed to match the DVI signal.
        Make sure to initialize other objects after this one so they account
        for the changed clock. This also allocates a very large framebuffer
        and is most likely to succeed the earlier it is attempted.

        Each dp and dn pair of pins must be neighboring, such as 19 and 20.
        They must also be ordered the same way. In other words, dp must be
        less than dn for all pairs or dp must be greater than dn for all pairs.

        The framebuffer pixel format varies depending on color_depth:
        * 1 - Each bit is a pixel. Either white (1) or black (0).
        * 2 - Each 2 bits is a pixels. Grayscale between white (0x3) and black (0x0).
        * 8 - Each byte is a pixels in RGB332 format.
        * 16 - Each two bytes are a pixel in RGB565 format.

        Monochrome framebuffers (color_depth=1 or 2) will be full resolution.
        Color framebuffers will be half resolution and pixels will be
        duplicated to create a signal with the target dimensions.

        A Framebuffer is often used in conjunction with a
        `framebufferio.FramebufferDisplay`.

        :param int width: the width of the target display signal. It will be halved when
          color_depth >= 8 when creating the framebuffer. Only 640 or 800 is currently supported.
        :param int height: the height of the target display signal. It will be halved when
          color_depth >= 8 when creating the framebuffer. Only 480 is currently supported.
        :param ~microcontroller.Pin clk_dp: the positive clock signal pin
        :param ~microcontroller.Pin clk_dn: the negative clock signal pin
        :param ~microcontroller.Pin red_dp: the positive red signal pin
        :param ~microcontroller.Pin red_dn: the negative red signal pin
        :param ~microcontroller.Pin green_dp: the positive green signal pin
        :param ~microcontroller.Pin green_dn: the negative green signal pin
        :param ~microcontroller.Pin blue_dp: the positive blue signal pin
        :param ~microcontroller.Pin blue_dn: the negative blue signal pin
        :param int color_depth: the color depth of the framebuffer in bits. 1, 2 for grayscale
          and 8 or 16 for color
        """
    def deinit(self) -> None:
        """Free the resources (pins, timers, etc.) associated with this
        `picodvi.Framebuffer` instance.  After deinitialization, no further operations
        may be performed."""
        ...
    width: int
    """The width of the framebuffer, in pixels. It may be doubled for output (and half of what
       width was given to __init__.)"""
    height: int
    """The width of the framebuffer, in pixels. It may be doubled for output (and half of what
       width was given to __init__.)"""
