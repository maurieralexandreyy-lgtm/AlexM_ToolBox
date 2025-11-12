import maya.cmds as cmds

# On garde les variables de noms pour la clarté
WINDOW_NAME = "blendJointCreatorWindow"
BLEND_JOINT_SUFFIX = "bld" 

# Variables globales pour les noms des joints sélectionnés (initialisées à None)
G_BASE_JNT = None
G_TARGET_JNT = None

# Variables globales pour les contrôles de l'UI (pour pouvoir lire leurs valeurs)
G_TRANSLATE_SLIDER = None
G_ROTATE_SLIDER = None
G_SCALE_SLIDER = None
G_SHEAR_SLIDER = None
G_COLOR_SLIDER = None # Nouveau : pour le contrôle de la couleur


def get_selection_and_update_ui():
    """
    Récupère la sélection et met à jour les champs de texte de l'UI.
    """
    global G_BASE_JNT, G_TARGET_JNT
    
    sel = cmds.ls(sl=True)
    if len(sel) != 2:
        cmds.warning("Veuillez sélectionner exactement deux joints (Base, puis Target).")
        return

    G_BASE_JNT = sel[0]
    G_TARGET_JNT = sel[1]
    
    # Mise à jour des champs de texte dans l'UI
    cmds.text('base_jnt_label', edit=True, label=f"Base (0%): **{G_BASE_JNT}**")
    cmds.text('target_jnt_label', edit=True, label=f"Target (100%): **{G_TARGET_JNT}**")
    cmds.button('create_button', edit=True, enable=True, 
                label=f"Créer Joint Blend ({G_BASE_JNT}_{BLEND_JOINT_SUFFIX})")
    
    cmds.inViewMessage(am="Joints sélectionnés. Prêt à créer le Blend Joint.", pos='topCenter', fade=True)


def get_color_index(rgb_value):
    """
    Convertit la couleur RGB du slider en index de couleur Maya.
    Ceci est une version simplifiée et ne correspondra qu'à des couleurs franches.
    """
    # Liste d'index de couleurs communes dans Maya (exemple)
    # L'index 14 (vert clair) est celui par défaut dans le script
    if rgb_value[0] > 0.9 and rgb_value[1] < 0.1 and rgb_value[2] < 0.1: # Rouge
        return 13
    elif rgb_value[0] < 0.1 and rgb_value[1] > 0.9 and rgb_value[2] < 0.1: # Vert
        return 14
    elif rgb_value[0] < 0.1 and rgb_value[1] < 0.1 and rgb_value[2] > 0.9: # Bleu
        return 6
    elif rgb_value[0] > 0.9 and rgb_value[1] > 0.9 and rgb_value[2] < 0.1: # Jaune
        return 17
    # Retourne une couleur neutre (gris) si la couleur n'est pas franche
    return 8


def create_blend_joint(*args):
    """
    Crée le blend joint en utilisant les joints stockés, les poids et la couleur spécifiée.
    """
    if G_BASE_JNT is None or G_TARGET_JNT is None:
        cmds.warning("Veuillez d'abord sélectionner deux joints en utilisant le bouton 'Sélectionner Joints'.")
        return

    # 1. Récupération des valeurs des sliders
    translate_w = cmds.floatSliderGrp(G_TRANSLATE_SLIDER, query=True, value=True)
    rotate_w = cmds.floatSliderGrp(G_ROTATE_SLIDER, query=True, value=True)
    scale_w = cmds.floatSliderGrp(G_SCALE_SLIDER, query=True, value=True)
    shear_w = cmds.floatSliderGrp(G_SHEAR_SLIDER, query=True, value=True)
    
    # Nouveau : Récupération de la couleur [R, G, B]
    color_rgb = cmds.colorSliderGrp(G_COLOR_SLIDER, query=True, rgbValue=True)
    color_index = get_color_index(color_rgb)

    # 2. Création des éléments
    cmds.select(clear=True)
    bld_jnt = cmds.joint(name=f"{G_BASE_JNT}_{BLEND_JOINT_SUFFIX}")
    # On ajoute une valeur aléatoire à la fin du nom pour éviter les conflits si l'UI est lancée plusieurs fois
    # (cela simplifie le script en évitant la vérification d'existence)
    import random
    unique_id = int(random.random() * 1000)
    bldMatX = cmds.createNode("blendMatrix", name=f"bldMatX_{G_BASE_JNT}_{unique_id}")

    # 3. Connexions de base
    cmds.connectAttr(f"{G_BASE_JNT}.worldMatrix[0]", f"{bldMatX}.inputMatrix", f=True)
    cmds.connectAttr(f"{G_TARGET_JNT}.worldMatrix[0]", f"{bldMatX}.target[0].targetMatrix", f=True)
    cmds.connectAttr(f"{bldMatX}.outputMatrix", f"{bld_jnt}.offsetParentMatrix", f=True)

    # 4. Application des poids et de la couleur
    cmds.setAttr(f"{bldMatX}.target[0].weight", 1.0)
    cmds.setAttr(f"{bldMatX}.target[0].translateWeight", translate_w)
    cmds.setAttr(f"{bldMatX}.target[0].rotateWeight", rotate_w)
    cmds.setAttr(f"{bldMatX}.target[0].scaleWeight", scale_w)
    cmds.setAttr(f"{bldMatX}.target[0].shearWeight", shear_w)

    # 5. Setup visuel du joint (avec la couleur de l'UI)
    cmds.setAttr(f"{bld_jnt}.radius", 1.5)
    cmds.setAttr(f"{bld_jnt}.overrideEnabled", 1)
    cmds.setAttr(f"{bld_jnt}.overrideColor", color_index) # Utilise l'index calculé
    
    cmds.select(bld_jnt)
    cmds.inViewMessage(am=f"Blend Joint créé : {bld_jnt}", pos='topCenter', fade=True)


def create_blend_joint_ui():
    """ Ouvre la fenêtre de l'outil de Blend Joint. """
    global G_TRANSLATE_SLIDER, G_ROTATE_SLIDER, G_SCALE_SLIDER, G_SHEAR_SLIDER, G_COLOR_SLIDER
    
    if cmds.window(WINDOW_NAME, exists=True):
        cmds.deleteUI(WINDOW_NAME, window=True)

    # --- UI Creation ---
    cmds.window(WINDOW_NAME, title="Blend Joint Creator (Simple)", widthHeight=(320, 370), s=False)
    
    main_layout = cmds.columnLayout(adjustableColumn=True, columnAttach=('both', 5), rowSpacing=5, parent=WINDOW_NAME)
    
    # 1. Zone de sélection
    cmds.text(label="**ÉTAPE 1 : SÉLECTIONNER JOINTS**", align='center', fn='boldLabelFont')
    cmds.button(label="Sélectionner Joints (Base, puis Target)", command=lambda *args: get_selection_and_update_ui())
    
    cmds.text('base_jnt_label', label="Base (0%): **AUCUN**", align='left')
    cmds.text('target_jnt_label', label="Target (100%): **AUCUN**", align='left')
    
    cmds.separator(height=10, style='in')
    
    # 2. Zone des poids
    cmds.text(label="**ÉTAPE 2 : INFLUENCE**", align='center', fn='boldLabelFont')
    
    G_TRANSLATE_SLIDER = cmds.floatSliderGrp(
        label="Translation", field=True, precision=2, minValue=0.0, 
        maxValue=1.0, value=0.5, step=0.01, columnWidth3=(70, 40, 150)
    )
    G_ROTATE_SLIDER = cmds.floatSliderGrp(
        label="Rotation", field=True, precision=2, minValue=0.0, 
        maxValue=1.0, value=0.5, step=0.01, columnWidth3=(70, 40, 150)
    )
    G_SCALE_SLIDER = cmds.floatSliderGrp(
        label="Scale", field=True, precision=2, minValue=0.0, 
        maxValue=1.0, value=0.5, step=0.01, columnWidth3=(70, 40, 150)
    )
    G_SHEAR_SLIDER = cmds.floatSliderGrp(
        label="Shear", field=True, precision=2, minValue=0.0, 
        maxValue=1.0, value=0.5, step=0.01, columnWidth3=(70, 40, 150)
    )
    
    cmds.separator(height=10, style='in')

    # Nouveau : Contrôle de la couleur
    cmds.text(label="**ÉTAPE 3 : COULEUR DU JOINT**", align='center', fn='boldLabelFont')
    G_COLOR_SLIDER = cmds.colorSliderGrp(
        label="Couleur",
        rgb=(0.0, 1.0, 0.0), # Vert par défaut (correspond à l'index 14)
        columnWidth3=(70, 40, 150)
    )
    
    cmds.separator(height=10, style='in')

    # 4. Bouton d'action
    cmds.button('create_button', 
                label="Créer Joint Blend (Sélectionner joints d'abord)", 
                command=create_blend_joint, 
                enable=False)
    
    cmds.showWindow(WINDOW_NAME)

# Lancement de la fenêtre
create_blend_joint_ui()