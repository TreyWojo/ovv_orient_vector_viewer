# OVV - Orientation and Vector Viewer

OVV is designed to act as an extension of the viewer in geo nodes, allowing you to quickly visualize vectors and orientations. The main goals of this tool are:
1. quick, easy visualization
2. support for multiple ways of defining orientations (2 vectors, rotation vector, quaternion, matrix) 
3. fully customizable user defaults for the node
4. Auto switching of visualization types (that the user can override when they need to)

In designing this tool, I ended up needing a collection of quaternion math nodes and a few matrix math nodes, they have been included as well. 

Besides reading this doc, one of the easiest ways to learn the tool is to just try it out! A demo file has been included with the plugin and can be accessed by going to the add-on preferences and clicking "Open Demo Scene."

<img width="592" height="1068" alt="image" src="https://github.com/user-attachments/assets/58d7637f-43b3-4ac9-beb4-356362539ab8" />


## The Node:
To get started select a node with a geometry output, and hit 'V'. That will create the `ovv_orient_vector_vis` node and a viewer, and wire it up to the geometry. 

## To-Do:
[x] - make settings panel in preferences 
[ ] - add settings to pref-panel
[ ] - add link to demo file in preferences
[ ] - add link to documentation in preferences
[ ] - make matrix demo in demo file
[ ] - write documentation
[ ] - make video for plugin
[ ] - write post for plugin
