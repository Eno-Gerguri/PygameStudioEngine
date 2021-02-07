from pygame_studio_engine.scene import Scene

from typing import Any


class SceneList(list):
    def __init__(self, *args: tuple[Any, ...]):
        if args:
            assert all(isinstance(i, Scene) for i in args)
            assert any(
                (iter_arg_actives := iter((scene.is_active for scene in args)))
            ) and not any(iter_arg_actives)
            super(SceneList, self).__init__(args)
            for scene in args:
                if scene.is_active:
                    self.active_scene = scene
                    break
        else:
            super(SceneList, self).__init__([Scene()])
            self.active_scene: Scene = self[0]

    def __setitem__(self, key, value):
        assert isinstance(value, Scene)
        super(SceneList, self).__setitem__(key, value)

    def __delitem__(self, key):
        scene_to_be_deleted_build_index = self[key].build_index
        super(SceneList, self).__delitem__(key)
        for scene in self[scene_to_be_deleted_build_index:]:
            scene.build_index -= 1

    def __add__(self, other):
        assert all(isinstance(i, Scene) for i in other)
        new_scenes: list[Scene] = super(SceneList, self).__add__(other)
        for scene in new_scenes[-len(other):]:
            scene.build_index = self.index(scene)
        return SceneList(*new_scenes)

    def __iadd__(self, other):
        assert all(isinstance(i, Scene) for i in other)
        new_scenes: list[Scene] = super(SceneList, self).__iadd__(other)
        for scene in new_scenes[-len(other):]:
            scene.build_index = self.index(scene)
        return SceneList(*new_scenes)

    def append(self, value):
        assert isinstance(value, Scene)
        super(SceneList, self).append(value)
        value.build_index = self.index(value)

    def remove(self, value):
        super(SceneList, self).remove(value)
        for scene in self[value.build_index:]:
            scene.build_index -= 1
