"""
    This module brings together functions used in several modules of the program.

    Functions
    ---------
    draw_text(obj, text, size, coordinate, align="topleft", color=WHITE, mouse_event_key=None):
        display a given one line text on the screen
    get_nbr_lines(max_width, text, size=25, coordinate=(5, 5), surface=None):
        returns returns the number of lines that a given text takes in a surface of given width
    draw_multilines_text(text_surface, text_rect, text, size=25, coordinate=(5, 5), color=WHITE, surface=None):
        display a given multi lines text on the screen
    get_hovered_rectangle(clickable_item, mouse_pos):
        returns the item which is currently hovered by the mouse pointer
    exit_gracefully(instance):
        quit the game
"""

import sys
import pygame as pg

import globvars as glob
from settings import *


def draw_text(obj, text, size, coordinate, align="topleft", color=WHITE, mouse_event_key=None):
    """ Display a given one line text on the screen.

    !!! This should be a one line text, if the text is larger than the screen there will be no line break. !!!

    :param obj: instance owning the rectangle
    :param text: text to display
    :param size: text size in pixel
    :param coordinate: a tuple containing the x and y position where you want to start writing the text
    :param align: position attribute of the Rect object
    :param color: text color in RGB code
    :param mouse_event_key: item key in case rectangle must react to mouse events
    :return: None
    :exception: align parameter is not valid
    """

    font = pg.font.Font(pg.font.match_font(DEFAULTFONT), size)
    text_surface = font.render(' ' + text + ' ', True, color)
    text_rect = text_surface.get_rect()

    if align == "topleft":
        text_rect.topleft = coordinate
    elif align == "topright":
        text_rect.topright = coordinate
    elif align == "bottomleft":
        text_rect.bottomleft = coordinate
    elif align == "bottomright":
        text_rect.bottomright = coordinate
    elif align == "midtop":
        text_rect.midtop = coordinate
    elif align == "midbottom":
        text_rect.midbottom = coordinate
    elif align == "midright":
        text_rect.midright = coordinate
    elif align == "midleft":
        text_rect.midleft = coordinate
    elif align == "center":
        text_rect.center = coordinate
    else:
        raise Exception("align parameter '{}' is not a valid position attribute of a Rect object.".format(align))

    if mouse_event_key is not None:
        obj.clickable_item[mouse_event_key] = text_rect
    glob.screen.blit(text_surface, text_rect)


def get_nbr_lines(max_width, text, size=25, coordinate=(5, 5), surface=None):
    """ Returns returns the number of lines that a given text takes in a surface of given width.

    :param max_width: the width of the surface
    :param text: text to write in the surface
    :param size: text size in pixel
    :param coordinate: a tuple containing the x and y position where you want to start writing the text
    :param surface: surface to blit the text into
    :return: number of lines that a given text takes in a surface of given width
    """

    font = pg.font.Font(pg.font.match_font(DEFAULTFONT), size)
    lines = [line.split(' ') for line in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    word_width, word_height = (0, 0 if surface is None else TILESIZE)
    x, y = coordinate
    nbr_lines = 0
    for line in lines:
        nbr_lines += 1
        for word in line:
            word_surface = font.render(word, True, WHITE)
            word_width, word_height = (word_surface.get_width(), word_surface.get_height() if surface is None else TILESIZE)
            if x + word_width >= max_width:
                nbr_lines += 1
                x = coordinate[0]  # Reset the x.
                y += word_height  # Start on new row.
            x += word_width + space
        x = coordinate[0]  # Reset the x.
        y += word_height  # Start on new row.

    return nbr_lines


def draw_multilines_text(text_surface, text_rect, text, size=25, coordinate=(5, 5), color=WHITE, surface=None):
    """ Display a given multi lines text on the screen.

    !!! If the text is wider than the surface, there will be a line break but
    if it is longer than the surface, the lines that exceed will not be written.

    :param text_surface: surface inside which the text will be written
    :param text_rect: used to blit the text
    :param text: multi lines text to display
    :param size: text size in pixel
    :param coordinate: a tuple containing the x and y position where you want to start writing the text
    :param color: text color in RGB code
    :param surface: surface to blit the text into
    :return: None
    """

    font = pg.font.Font(pg.font.match_font(DEFAULTFONT), size)
    lines = [line.split(' ') for line in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width = text_surface.get_width()
    word_width, word_height = (0, 0 if surface is None else TILESIZE)
    x, y = coordinate
    for line in lines:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = (word_surface.get_width(), word_surface.get_height() if surface is None else TILESIZE)
            if x + word_width >= max_width:
                x = coordinate[0]  # Reset the x.
                y += word_height  # Start on new row.
            text_surface.blit(word_surface, (x, y))
            x += word_width + space
        x = coordinate[0]  # Reset the x.
        y += word_height  # Start on new row.

    if surface is not None:
        surface.blit(text_surface, text_rect)
    else:
        glob.screen.blit(text_surface, text_rect)


def get_hovered_rectangle(clickable_item, mouse_pos):
    """ Returns the item on which the user clicked.

    :param clickable_item: dictionary of clickable items
    :param mouse_pos: x & y coordinate of the mouse pointer
    :return: the item on which the user clicked
    """

    for thisRect in clickable_item:
        if clickable_item[thisRect].collidepoint(mouse_pos):
            return thisRect
    return None


def exit_gracefully(instance):
    """ Quit the game.

    Performs properly all required closing tasks

    :param instance: location of the program from which the user has left the game
    :return: None
    """

    if DEBUG:
        print("Exit from "+instance.whoami)

    # Need to save the config only when the user quits the game
    glob.persistence.save_user_config()

    pg.quit()
    sys.exit()
