def demo():
    """### Launch the app"""
    import mimikit as mmk
    from ipywidgets import widgets as W
    import IPython.display as ipd

    # *************** MacOS user with M1 *****************
    # if creating a dataset hang, uncomment the next 2 lines:
    # import multiprocess as mp
    # mp.set_start_method("spawn")

    ipd.display(mmk.MMK_STYLE_SHEET)
    ipd.display(W.HTML(
        """
        <style>
        .container {
            width: 95% !important;
        }
        """
    ))

    app = mmk.ClusterizerApp()

    ipd.display(
        app.dataset_widget,
        app.clustering_widget,
        app.labels_widget
    )
    """### Note"""
    """
you can interact with the waveform/widgets with following shortcuts:

- Navigation:
    * `Ctrl + wheel`: zoom
    * `SHIFT + dbl-click`: reset zoom
    * `SHIFT + wheel`: scroll wvaveform
    * `arrow left/right`: move playhead left/right
    * `SHIFT + arrow left/right`: move playhead left/right a lot.
- Controls:
    * `dbl-click`: play from there
    * `SPACE BAR`: play/pause 
- Segments:
    * `alt + click`: add segment
    * `alt + SHIFT + click` on a segment: remove segment
    * `Ctrl + alt + click` on a segment: edit segment's label

you can also drag segments' boundaries with the mouse to edit their position"""
    """----------------------------"""