import maya.cmds as cmds

def joints_on_curve():
    # Récupérer la curve sélectionnée
    selection = cmds.ls(selection=True, long=True)
    
    if not selection:
        cmds.warning("Veuillez sélectionner une curve.")
        return
    
    curve = selection[0]
    shape = cmds.listRelatives(curve, shapes=True, fullPath=True)
    
    if not shape or cmds.nodeType(shape[0]) != "nurbsCurve":
        cmds.warning("L'objet sélectionné n'est pas une curve.")
        return
    
    # Récupérer le nombre de spans de la curve
    num_cvs = cmds.getAttr(curve + ".spans") + cmds.getAttr(curve + ".degree")
    joints = []
    locators = cmds.group(empty=True, name=f"Locators_{curve.split('|')[-1]}")
    
    for i in range(num_cvs):
        # Créer un locator pour stocker la position
        locator = cmds.spaceLocator(name=f"Loc_{curve.split('|')[-1]}_{i}")[0]
        cmds.parent(locator, locators)
        
        # Créer un PointOnCurveInfo node
        poc = cmds.createNode("pointOnCurveInfo", name=f"POC_{curve.split('|')[-1]}_{i}")
        cmds.connectAttr(f"{shape[0]}.worldSpace[0]", f"{poc}.inputCurve")
        cmds.setAttr(f"{poc}.turnOnPercentage", 1)
        cmds.setAttr(f"{poc}.parameter", i / float(num_cvs - 1))
        
        # Connecter la position du locator
        cmds.connectAttr(f"{poc}.position", f"{locator}.translate")
        
        # Créer un joint
        joint_name = f"Bind_{curve.split('|')[-1]}_{i}"
        joint = cmds.joint(name=joint_name)
        cmds.parent(joint, locator)
        cmds.setAttr(f"{joint}.translate", 0, 0, 0)
        joints.append(joint)
        cmds.select(clear=True)

joints_on_curve()