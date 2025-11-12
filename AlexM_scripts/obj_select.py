import maya.cmds as cmds

def select_filtered_objects(*args):
    name_filter = cmds.textField("nameField", query=True, text=True)
    type_filter = cmds.radioCollection("typeRadioCol", query=True, select=True)
    selected_type = cmds.radioButton(type_filter, query=True, label=True)

    selection = cmds.ls(selection=True, long=True) or cmds.ls(assemblies=True, long=True)
    all_objects = cmds.listRelatives(selection, allDescendents=True, fullPath=True) or []
    all_objects += selection

    if name_filter:
        all_objects = [obj for obj in all_objects if name_filter in obj]

    if selected_type != "none":
        if selected_type == "joint":
            all_objects = [obj for obj in all_objects if cmds.objectType(obj) == "joint"]
        elif selected_type == "curve":
            all_objects = [obj for obj in all_objects if cmds.objectType(obj) == "nurbsCurve" or
                           (cmds.listRelatives(obj, shapes=True) and 
                            cmds.objectType(cmds.listRelatives(obj, shapes=True)[0]) == "nurbsCurve")]

    if all_objects:
        cmds.select(all_objects, replace=True)
    else:
        cmds.select(clear=True)
        cmds.warning("Aucun objet trouvé avec ces critères.")

def object_selector_ui():
    if cmds.window("simpleSelectorWin", exists=True):
        cmds.deleteUI("simpleSelectorWin")
    window = cmds.window("simpleSelectorWin", title="Object Selector", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label="object name:")
    cmds.textField("nameField", width=150, placeholderText="Enter part of name...")
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=2)
    cmds.text(label="object type:")
    cmds.columnLayout()
    cmds.radioCollection("typeRadioCol")
    cmds.radioButton(label="none")
    cmds.radioButton(label="joint")
    cmds.radioButton(label="curve")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.button(label="Select Objects", command=select_filtered_objects)
    cmds.showWindow(window)

object_selector_ui()