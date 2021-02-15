from pygame_studio_engine.scene_management.scene import Scene


class SceneList(list):
    def __init__(self, *args: tuple[Scene, ...]):
        if args:
            assert all(isinstance(i, Scene) for i in args)
            assert any(
                (iter_arg_actives := iter((scene.is_active for scene in args)))
            ) and not any(iter_arg_actives)
            for scene in args:
                scene.build_index = args.index(scene)
                if scene.is_active:
                    self._active_scene = scene
            super(SceneList, self).__init__(args)
        else:
            super(SceneList, self).__init__([Scene(build_index=0)])
            self._active_scene: Scene = self[0]

    def __setitem__(self, key, value):
        assert isinstance(value, Scene)
        if self[key].is_active:
            assert value.is_active
            super(SceneList, self).__setitem__(key, value)
            self.active_scene = value
        else:
            super(SceneList, self).__setitem__(key, value)
            if value.is_active:
                self.active_scene = value

    def __delitem__(self, key):
        assert not self[key].is_active
        scene_to_be_deleted_build_index = self[key].build_index
        super(SceneList, self).__delitem__(key)
        for scene in self[scene_to_be_deleted_build_index:]:
            scene.build_index -= 1

    def __add__(self, other):
        assert all(isinstance(i, Scene) for i in other)
        assert any(
                (iter_other_actives := iter(
                        (scene.is_active for scene in other)
                ))) and not any(iter_other_actives)
        new_scenes: list[Scene] = super(SceneList, self).__add__(other)
        for scene in new_scenes[-len(other):]:
            scene.build_index = self.index(scene)
        return SceneList(*new_scenes)

    def __iadd__(self, other):
        assert all(isinstance(i, Scene) for i in other)
        assert any(
                (iter_other_actives := iter(
                        (scene.is_active for scene in other)
                ))) and not any(iter_other_actives)
        new_scenes: list[Scene] = super(SceneList, self).__iadd__(other)
        for scene in new_scenes[-len(other):]:
            scene.build_index = self.index(scene)
        return SceneList(*new_scenes)

    def append(self, value):
        assert isinstance(value, Scene)
        assert not value.is_active
        super(SceneList, self).append(value)
        value.build_index = self.index(value)

    def remove(self, value):
        assert not value.is_active
        super(SceneList, self).remove(value)
        for scene in self[value.build_index:]:
            scene.build_index -= 1

    def active_scene_changed(
            self,
            old_active_scene: Scene,
            new_active_scene: Scene
    ) -> None:
        """
        Calls all active_scene_changed methods in all game_objects that have
        them in the active_scene.

        :param old_active_scene: The old active scene, that is no longer active
        :type old_active_scene: Scene
        :param new_active_scene: The new active scene, that is currently active
        :type new_active_scene: Scene
        :return: None
        :rtype: None
        """
        for game_object in self.active_scene.game_objects:
            if game_object.is_active:
                game_object.broadcast_message(
                        method_name="active_scene_changed",
                        old_active_scene=old_active_scene,
                        new_active_scene=new_active_scene
                )

    def scene_loaded(self, scene_loaded: Scene) -> None:
        """
        Calls all scene_loaded methods in all game_objects that have them in
        the active_scene.

        :param scene_loaded: The scene that was loaded to be the active scene
        :type scene_loaded: Scene
        :return: None
        :rtype: None
        """
        for game_object in self.active_scene.game_objects:
            if game_object.is_active:
                game_object.broadcast_message(
                        method_name="scene_loaded",
                        scene_loaded=scene_loaded
                )

    def scene_unloaded(self, scene_unloaded: Scene) -> None:
        """
        Calls all scene_unloaded methods in all game_objects that have them
        in the active_scene.

        :param scene_unloaded: The scene that was unloaded to no longer be the
                               active scene
        :type scene_unloaded: Scene
        :return: None
        :rtype: None
        """
        for game_object in scene_unloaded.game_objects:
            if game_object.is_active:
                game_object.broadcast_message(
                        method_name="scene_unloaded",
                        scene_unloaded=scene_unloaded
                )

    @property
    def active_scene(self) -> Scene:
        """
        Returns the currently active scene.

        :getter: Currently active scene
        :setter: The new active scene to load
        :type: Scene
        """
        return self._active_scene

    @active_scene.setter
    def active_scene(self, value):
        assert isinstance(value, Scene)

        def set_active_scene() -> None:
            """
            Sets the correct active scene and calls the correct scene events.

            :return: None
            :rtype: None
            """
            scene_being_unloaded = self._active_scene
            self._active_scene.is_active = False
            value.is_active = True
            self._active_scene = value
            self.scene_unloaded(scene_unloaded=scene_being_unloaded)
            self.scene_loaded(scene_loaded=self._active_scene)
            self.active_scene_changed(
                    old_active_scene=scene_being_unloaded,
                    new_active_scene=self._active_scene
            )

        if value in self:
            set_active_scene()
        else:
            self.append(value)
            set_active_scene()
