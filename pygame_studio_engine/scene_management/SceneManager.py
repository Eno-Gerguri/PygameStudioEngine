from os import getcwd
from os.path import isfile

from pygame_studio_engine.scene_management.scene_list import SceneList

from typing import TYPE_CHECKING, Optional, Union
if TYPE_CHECKING:
    from pygame_studio_engine.scene_management.scene import Scene


scenes: SceneList[Scene] = SceneList()


def get_scene_by_name(name: str) -> Optional[Scene]:
    """
    Searches through and returns any scene with the given name in the build
    settings.

    If no Scene with given name exists in Build Settings, then None will be
    returned.

    :param name: Name of Scene to find
    :type name: str
    :return: Scene with given name
    :rtype: Scene or None
    """
    for scene in scenes:
        if scene.name == name:
            return scene

    return None


def get_scene_by_path(scene_path: str) -> Optional[Scene]:
    """
    Searches all Scenes in Build Settings for a Scene that has the given
    asset path.

    :param scene_path: Path of the Scene.
                       Should be relative to the project folder. Like:
                       "Assets/MyScenes/my_scene.py"
    :type scene_path: str
    :return: Scene with given asset path
    :rtype: Scene or None
    """
    if isfile(path=(full_scene_path := getcwd() + "\\" + scene_path)):
        scene_file = __import__(full_scene_path)
        from inspect import isclass
        scene_class = [i for i in dir(scene_file)
                       if isclass(object=getattr(scene_file, i))]
        for scene in scenes:
            if isinstance(scene, eval(f"scene_file.{scene_class}")):
                return scene

        return None


def load_scene_by_name(scene_name: str) -> Optional[Scene]:
    """
    Loads the Scene by its name in Build Settings.

    :param scene_name: Name of the Scene to load
    :type scene_name: str
    :return: Scene that was loaded
    :rtype: Scene or None
    """
    for scene in scenes:
        if scene.name == scene_name:
            scenes.active_scene = scene
            return scene


def load_scene_by_build_index(build_index: int) -> Optional[Scene]:
    """
    Loads the Scene by its build index in Build Settings.

    :param build_index: Index of the Scene in the Build Settings
    :type build_index: int
    :return: Scene that was loaded
    :rtype: Scene or None
    """
    try:
        scenes.active_scene = scenes[build_index]
        return scenes[build_index]
    except IndexError:
        return None


def load_scene(scene_information: Union[str, int]) -> Optional[Scene]:
    """
    Loads Scene based on the given scene information.
    
    :param scene_information: Name of the Scene to load or
                              Index of the Scene in the Build Settings
    :type scene_information: str or int
    :return: Scene that was loaded
    :rtype: Scene or None
    """
    if isinstance(scene_information, str):
        return load_scene_by_name(scene_name=scene_information)
    elif isinstance(scene_information, int):
        return load_scene_by_build_index(build_index=scene_information)
    else:
        return None
