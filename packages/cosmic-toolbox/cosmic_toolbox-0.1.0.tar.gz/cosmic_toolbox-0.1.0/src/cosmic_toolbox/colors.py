import matplotlib.pyplot as plt
from cycler import cycler


def get_colors(cycle="silvan"):

    if cycle == "silvan":
        return {
            "b": "#0063B9",
            "r": "#BA1A13",
            "g": "#34BA09",
            "orange": "#ED6018",
            "violet": "#6E13BA",
            "brown": "#6E2C0B",
            "grey": "#808080",
            "pink": "#BA13A0",
            "olive": "#B0BA13",
            "bluegreen": "#09BAAF",
        }
    else:
        return cycle


def set_cycle(cycle="silvan"):

    colors = get_colors(cycle=cycle)
    if isinstance(colors, dict):
        col = colors.values()
    else:
        col = colors
    plt.rc("axes", prop_cycle=cycler(color=col))
