from pygame_studio_engine.scene_management.scene_list import SceneList

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pygame_studio_engine.scene import Scene


scenes: SceneList[Scene] = SceneList()
