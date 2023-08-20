# Geo-Gebra

## Introduction
GeoGebra is a mathematical UI software that integrates geometry, algebra, and calculus. 
It allows users to explore mathematical concepts through dynamic visualizations, making it an invaluable tool for students, teachers, and professionals alike.
Our contribution is the translation of GeoGebra from Java to Python.

## features
### Draw / Delete
Our GUI is able to handle inputs of data, Draw it and Delete. <br />
Current shapes availables: <br />
Point, Line, Circle and others. <br /><br />
Each shape have those following features: <br />
   Label - Represent the shape in the text and also on the figure. <br />
   Drag - Each shape can be drag from it place, the label will change as follow. <br />
   Hide - hide the object from the figure but not from the list of shapes (not as delete). <br />


### Undo / Redo
In our program, all kind of operaiton are saved.<br />
The Undo and Redo works in this way:<br />
Undo take an operation that has occurred and do the opposite one to undo it, 
and the Redo simply take an operation and do it as is.<br />


### Reset / delete history
Reset is the ability to reset the figure from shape (and it's included as operation that we can Undo or Redo)<br />
Delete history simply delete all the operations from the history s.t you can't restore anymore and it is initialize (but save the shapes already drawn)<br />

### Save / Load
Save the current poisition of the figure with all the shaped on it.<br />
Load from file a position and continue from there.<br />

## platform
Our Gui use two main classes:<br />
   1) matplotlib - to display information on the grids (such as plotting shapes).<br />
   2) tkinter - to display all the wrraper information (such as equalitions, buttons and other features).<br />

<img src="Images/sample.PNG" alt="Image" width="1000" height="600">

## How to use it?
### Prerequisites
- Python: If you do not have Python installed, please follow this [link](https://www.python.org/downloads/) to download and install the latest version.

1. Clone the repository to your local machine using the following command: git clone https://github.com/HILLELOH/Project_Geo_Gebra.git
2. Open your command prompt (CMD) or terminal and navigate to the project directory.
3. Install the required packages by running the following commands: 
    - pip install matplotlib,colorama,scipy
   or simply, navigate to the requirements.txt in the cmd and run: pip install -r requirements.txt

4. Run the `geogebra_interface.py` file using the following command:
    - python geogebra_interface.py

### Original Java based project
https://github.com/geogebra/geogebra.git





