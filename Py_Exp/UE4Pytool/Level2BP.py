import unreal

# # Get all actors in the current level
# EditorSub = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
# EditorActorSubsys = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# level_actors  = EditorActorSubsys.get_all_level_actors()
# editor_world = EditorSub.get_editor_world()

# current_level_name = editor_world.get_name()

# print(current_level_name)


# # Create a new Blueprint class
# asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
# blueprint_factory = unreal.BlueprintFactory()
# blueprint_factory.set_editor_property('ParentClass', unreal.Actor)

# path_prefabfolder = '/Game/Ballance_Game/Prefabs/AutoLevel'

# bpname = 'PL_' + current_level_name

# new_blueprint = asset_tools.create_asset(bpname, path_prefabfolder, None, blueprint_factory)

# new_blueprint_actor = EditorActorSubsys.spawn_actor_from_class(new_blueprint.generated_class(), unreal.Vector(0, 0, 0))

# for actor in level_actors:
#     #new_component = unreal.EditorAssetLibrary.add_actor_component(new_blueprint_actor, actor.get_class(), actor.get_name())
#     new_component = new_blueprint_actor.add_child_actor_component(actor.get_class(), actor.get_name())
#     new_component.set_world_transform(actor.get_actor_transform())


# # Save the new Blueprint asset
# unreal.EditorAssetLibrary.save_loaded_asset(new_blueprint_actor)


path_level_folder = '/Game/Ballance_Game/Maps/Temp'
level_name = 'Map_Toy_S_02_Goe'

total_name = path_level_folder + '/' + level_name

times = 3

# Load the level multiple times
for i in range(times):
    new_level = unreal.EditorLevelUtils.create_new_streaming_level(unreal.LevelStreamingKismet, new_level_path=total_name)
    

    #new_level.set_should_be_visible(True)