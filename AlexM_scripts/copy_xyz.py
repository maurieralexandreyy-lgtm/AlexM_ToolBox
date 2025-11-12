import maya.cmds as cmds

def copy_xyz():
    # Récupérer les objets sélectionnés
    selected_objects = cmds.ls(selection=True)
    
    if len(selected_objects) < 2:
        cmds.warning("Veuillez sélectionner deux objets.")
        return

    source = selected_objects[0]
    target = selected_objects[1]

    translate_values = cmds.getAttr(f"{source}.translate")[0]
    cmds.setAttr(f"{target}.translate", translate_values[0], translate_values[1], translate_values[2])

    rotate_values = cmds.getAttr(f"{source}.rotate")[0]
    cmds.setAttr(f"{target}.rotate", rotate_values[0], rotate_values[1], rotate_values[2])

copy_xyz()