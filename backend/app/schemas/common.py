from typing import Literal

ServiceType = Literal["iv_cannula", "iv_fluids", "blood_draw", "home_visit"]
RelationType = Literal["self", "father", "mother", "child", "other"]
RequestStatus = Literal["pending", "assigned", "arrived", "in_progress", "completed", "cancelled"]
RoleType = Literal["patient", "nurse", "admin"]
