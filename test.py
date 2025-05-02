from sa_suite.controllers import SpaceMouse, SpaceMouseConfig

space_mouse_config = SpaceMouseConfig()
spacemouse = SpaceMouse(space_mouse_config)

while True:
    print(spacemouse.get_controller_state())
