GRAPHIC SCRIPTS USING GRID FOR PLOTTING
=======================================

These are (for now), stand-alone scripts using
Python and Pygame meant for having fun with little-squares
(or "big pixels") in the graphic output.


The are result of ludic and fun processes and are intended
to be hacked with and fine-tunned in the source code
(for tunning paramters, algoritms, and such), rather
than something ready-to-use (although they should
yield some plots by default).

The scripts so far use Pygame.


multilife.py
==============


Is a version of the "game of life" celular
authomata, factored in a way to have several,
differently colored layers, of the "game of life"
evolving simultaneously. Each layer may have
different rules.


tupper_self.py
=================

Is  a quick and dirty implementation of the
"Tupper Self refential Formula", using Pygame and
Python Decimals.

In short, the Tupper Self referential formula is an
algorithm encoded using regular mathematic operations
of Power, Floor and Modulo - which can display in a
grid an arbitrary image, providing the image encoding
as an offset (K) parameter in the form of a big
integer number (~500 digits).

The default plot is an image displaying the formula itself
in mathematical notation.

The function is presented in a nice-to-watch video in the NumberPhile
youtube channel at
https://www.youtube.com/watch?v=_s5RFgd59ao&fbclid=IwAR1DFQYVTHAGj_6jZG5dNsU-dAq09y-6xSyH67GveUETF20Mbnu6TieTj0E


The implementation so far lacks an elegand depicting of the formula
in Python - and a comment with the formula rendered using proper
unicode characters would also be a nice to have - contributions
are welcome.

