import maya.cmds as cmds

def compensate_grp():
    selected_objects = cmds.ls(selection=True)
    
    if not selected_objects:
        cmds.warning("Aucun objet sélectionné.")
        return
    
    for obj in selected_objects:
        # Obtenir la position actuelle de l'objet
        obj_parent = cmds.listRelatives(obj, parent=True)
        obj_position = cmds.xform(obj, query=True, worldSpace=True, matrix=True)
        
        # Création du groupe _Compensate au même endroit que l'objet
        compensate_group = cmds.group(empty=True, name=f"{obj}_Compensate")
        cmds.xform(compensate_group, worldSpace=True, matrix=obj_position)
        
        # Parent l'objet au groupe Compensate
        cmds.parent(obj, compensate_group)
        
        # Création du node multiplyDivide
        multiply_node = cmds.shadingNode("multiplyDivide", asUtility=True, name=f"{obj}_Multiply")
        cmds.setAttr(f"{multiply_node}.input2X", -1)
        cmds.setAttr(f"{multiply_node}.input2Y", -1)
        cmds.setAttr(f"{multiply_node}.input2Z", -1)
        
        # Connecte les translations de l'objet au multiplyDivide
        cmds.connectAttr(f"{obj}.translateX", f"{multiply_node}.input1X")
        cmds.connectAttr(f"{obj}.translateY", f"{multiply_node}.input1Y")
        cmds.connectAttr(f"{obj}.translateZ", f"{multiply_node}.input1Z")
        
        # Connecte le multiplyDivide au groupe _Compensate
        cmds.connectAttr(f"{multiply_node}.outputX", f"{compensate_group}.translateX")
        cmds.connectAttr(f"{multiply_node}.outputY", f"{compensate_group}.translateY")
        cmds.connectAttr(f"{multiply_node}.outputZ", f"{compensate_group}.translateZ")
        
        # Groupe _Compensate dans un groupe _Move
        move_group = cmds.group(compensate_group, name=f"{obj}_Move")
        
        # Restaurer la hiérarchie d'origine
        if obj_parent:
            cmds.parent(compensate_group, obj_parent[0])

compensate_grp()