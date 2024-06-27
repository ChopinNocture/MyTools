import unreal

# Get all actors in the current level
level_actors  = unreal.EditorLevelLibrary.get_all_level_actors()


editor_world = unreal.EditorLevelLibrary.get_editor_world()

current_level_name = editor_world.get_name()

print(current_level_name)


# Create a new Blueprint class
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
blueprint_factory = unreal.BlueprintFactory()
blueprint_factory.set_editor_property('ParentClass', unreal.Actor)

path_prefabfolder = '/Game/Ballance_Game/Prefabs/AutoLevel'

bpname = 'PL_' + current_level_name

new_blueprint = asset_tools.create_asset(bpname, path_prefabfolder, None, blueprint_factory)



new_blueprint_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(editor_world, new_blueprint.GeneratedClass, unreal.Vector(0, 0, 0))

for actor in level_actors:
    new_component = unreal.EditorAssetLibrary.add_actor_component(new_blueprint_actor, actor.get_class(), actor.get_name())
    new_component.set_world_transform(actor.get_actor_transform())


# Save the new Blueprint asset
unreal.EditorAssetLibrary.save_loaded_asset(new_blueprint_actor)

# Now, you would need to add the actors to the new Blueprint.
# This part of the script will depend on how you want to reference or include the actors in the Blueprint.
