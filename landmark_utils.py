jointNames = ["head", "l_shoulder", "r_shoulder", "l_elbow", "r_elbow", "l_wrist", "r_wrist", "l_hip", "r_hip"]
hand_names = ["wrist", 'thumb_knuckle', "thumb",  'pointer_knuckle', "pointer",  'middle_knuckle', "middle",  'index_knuckle', "index",  "pinky_knuckle", "pinky"]

def hideUnwanted(all, keep):
    visibilities = [False] * len(all)
    for i, landmark in enumerate(all):
        visibilities[i] = landmark.visibility
        landmark.visibility = 0
    for i in keep:
        all[i].visibility = visibilities[i]
