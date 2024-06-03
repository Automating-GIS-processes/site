# color.py
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, hex2color
import ipywidgets as widgets
from IPython.display import display, clear_output


def adjust_lightness(color, amount=1.0):
    import colorsys
    c = colorsys.rgb_to_hls(*hex2color(color))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

def display_color_palette(base_color='#30bab0', n_colors=5):
    base_rgb = hex2color(base_color)
    palette = [adjust_lightness(base_rgb, 1 + (i - n_colors / 2) * 0.2) for i in range(n_colors)]
    palette_hex = [to_hex(color) for color in palette]

    fig, ax = plt.subplots(figsize=(n_colors * 0.8, 1), dpi=80)
    ax.imshow([palette], extent=[0, n_colors, 0, 1])
    ax.set_xticks(range(n_colors))
    ax.set_xticklabels(palette_hex, rotation=45, fontsize=10)
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.show()



def run_visualizer():
    base_color_widget = widgets.ColorPicker(value='#30bab0', description='Base Color:', disabled=False)
    n_colors_widget = widgets.IntSlider(value=5, min=1, max=10, step=1, description='Number of Colors:', continuous_update=False)

    ui = widgets.VBox([base_color_widget, n_colors_widget])
    out = widgets.Output()

    def update_color_palette(change):
        with out:
            clear_output(wait=True)
            display_color_palette(base_color_widget.value, n_colors_widget.value)

    base_color_widget.observe(update_color_palette, names='value')
    n_colors_widget.observe(update_color_palette, names='value')

    display(ui, out)
    update_color_palette(None)

