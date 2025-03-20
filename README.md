# Apt 33 light show

Individually addressable on/off lights for the Ultimate board.

## About

Lights are projected onto the board via a projector.

The projector is connected to a computer, and displays via standard screen mirroring/extension.

This program creates a GUI window (via pygame) fullscreen, which should appear on the projector's
screen.
Then, a set of circles is drawn, each corresponding to a pixel, which get projected onto the board.

There are two aspects to note:

1. Perspective correction: The projector is probably not square to the board.
   The software allows the user to input an arbitrary perspective transform, to counter this and ensure
   that the pixels are rectangular.
2. Displaying the images: A boolean array is edited in real time (via threading), which is live
   updated on the board.

## Usage

First, align the board.

Place the projector on a stable surface, and don't move it for the duration of the show.

Run `python adjust_disp.py`. This allows you to live adjust the grid.

You can grab and move the four corners independently. Press ASXZ to select the corresponding
corner, and use arrow keys to move.

Hold Shift to move slowly, and Ctrl to move quickly.

This automatically saves `disp.json` live, which is read by all other programs.

Next, run any program you want.

## Files

**System**

- display.py: Display drawing and logic.
- adjust_disp.py: Live adjust projection.
- random_bw.py: Random display for testing.
- make_mask.py: Manually make binary image.

**Programs**

- game_of_life.py: Conway's Game of Life.
- image.py: Image or video.
- screensaver.py: Matrix and floodfill I/Ultimate.
- snake.py: Snake game.
- text.py: Scrolling text.

**Datafiles**

- disp.json: Projection data, automatically written.
- ultimate.npy, I.npy: Pre-made images.
