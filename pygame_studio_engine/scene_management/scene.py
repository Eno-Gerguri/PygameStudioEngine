from pygame_studio_engine.scene_management import SceneManager
from pygame_studio_engine.utils import get_first_available_name


class Scene:
    """
    Scene, which contain the objects of your game.

    :param build_index: Build index in the Build Settings, default is -1,
                        which means it hasn't been assigned
    :type: int
    :param is_active: Whether or not the scene is currently active
    :type: bool
    :param name
    """

    def __init__(self,
                 build_index: int = -1,
                 is_active: bool = False,
                 name: str = "Untitled"):
        self.build_index = build_index
        self.is_active = is_active
        self.name = get_first_available_name(
                base_name=name,
                names=(scene.name for scene in SceneManager.scenes)
        )
        self.game_objects: list[GameObject] = []
