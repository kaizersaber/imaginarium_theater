from shiny import ui


def imgs_from_paths(paths: list[str], width):
    imgs = [ui.img(src=p, width=width) for p in paths]
    return ui.TagList(*imgs)
