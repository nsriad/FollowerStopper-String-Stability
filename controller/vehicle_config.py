# controller/vehicle_config.py

vehicle_types = {
    "krauss_follower": {
        "carFollowModel": "Krauss",
        "accel": 2.5,
        "decel": 3.5,
        "tau": 1.1,
        "minGap": 2.5,
        "maxSpeed": 35
    },
    "idm_follower": {
        "carFollowModel": "IDM",
        "accel": 1.5,
        "decel": 3.5,
        "tau": 4,
        "minGap": 10,
        "maxSpeed": 30
    },
    "cacc_follower": {
        "carFollowModel": "CACC",
        "accel": 2.0,
        "decel": 2.0,
        "tau": 0.7,
        "minGap": 1.5,
        "maxSpeed": 35
    }
}
