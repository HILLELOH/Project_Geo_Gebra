# Geo-Gebra

## features
### Draw / Delete
Our GUI is able to handle inputs of data, Draw it and Delete.
Current shapes availables:
Point
Line
Circle
Each shape have those following features:
   Label - Represent the shape in the text and also on the figure.
   Drag - Each shape can be drag from it place, the label will change as follow.
   Hide - hide the object from the figure but not from the list of shapes (not as delete).


### Undo / Redo
In our program, all kind of operaiton are saved.
The Undo and Redo works in this way:
Undo take an operation that has occurred and do the opposite one to undo it, 
and the Redo simply take an operation and do it as is.


### Reset / delete history
Reset is the abilit to reset the figure from shape (and it's included as operation that we can Undo or Redo)
Delete history simply delete all the operations from the history s.t you can't restore anymore and it is initialize (but save the shapes already drawn)

### Save / Load
Save the current poisition of the figure with all the shaped on it.
Load from file a position and continue from there.



