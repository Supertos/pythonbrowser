# ----------------------------------------------------#
# *Python browser
# render.py
# ----------------
# Renders css boxes
# ----------------------------------------------------#
import pygame as pg


class box():
    def __init__(self, css_content):
        self.padding = (0, 0, 0, 0)
        self.margin = (0, 0, 0, 0)
        self.border = (0, 0, 0, 0)
        self.content = (0, 0)

        if "padding" in css_content: self.padding = css_content["padding"]
        if "margin" in css_content: self.margin = css_content["margin"]
        if "border" in css_content: self.border = css_content["border"]
        if "content" in css_content: self.content = css_content["content"]

    def autoForText(self, text, size):
        chars = len(text)
        px_per_char = size
        self.content = (chars * px_per_char * 2 / 3, px_per_char)

    def autoForSurf(self, surf: pg.Surface):
        self.content = surf.get_size()

    def getDimensions(self):
        width, height = self.content

        top, right, bottom, left = self.padding
        width += right + left
        height += top + bottom

        top, right, bottom, left = self.margin
        width += right + left
        height += top + bottom

        top, right, bottom, left = self.border
        width += right + left
        height += top + bottom

        return width, height

    def render(self, content=None):

        width, height = self.getDimensions()
        margin = self.margin
        padding = self.padding
        border = self.border

        padding_top, padding_right, padding_bottom, padding_left = padding
        margin_top, margin_right, margin_bottom, margin_left = margin
        border_top, border_right, border_bottom, border_left = border

        border_left_top_corner = (padding_left + border_left * 0.5, padding_top + border_top * 0.5)
        border_right_bottom_corner = (width - padding_right - border_right * 0.5, height - border_bottom * 0.5)

        border_left_bottom_corner = (padding_left + border_left * 0.5, height - padding_bottom - border_bottom * 0.5)
        border_right_top_corner = (width - padding_right - border_right * 0.5, padding_top + border_top * 0.5)

        border_left_top_corner_hor = (padding_left + border_left * 0.5, padding_top)
        border_right_bottom_corner_hor = (width - padding_right - border_right * 0.5, height)

        border_left_bottom_corner_hor = (padding_left + border_left * 0.5, height - padding_bottom)
        border_right_top_corner_hor = (width - padding_right - border_right * 0.5, padding_top)

        # Render
        cssBox = pg.Surface(size=(width, height), flags=pg.SRCALPHA)

        color = (0,0,0)

        pg.draw.line( cssBox, color, border_right_top_corner, border_left_top_corner, border_top)
        pg.draw.line( cssBox, color, border_right_top_corner_hor, border_right_bottom_corner_hor, border_right)
        pg.draw.line( cssBox, color,  border_left_top_corner_hor, border_left_bottom_corner_hor, border_left)
        pg.draw.line( cssBox, color, border_right_bottom_corner, border_left_bottom_corner, border_bottom)

        if content is pg.Surface:
            x = padding_left + margin_left + border_left
            y = padding_top + margin_top + border_top
            cssBox.blit( content, ( x, y ) )

        return cssBox














