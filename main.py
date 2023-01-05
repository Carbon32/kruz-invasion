# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                        Land Invasion, shooter video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.engine import *

# Game: #

game = Game()

# Sounds: #

sounds = Sounds(game)

# Resolution: #

resolution = Resolution(game)

# Resoltuion Selection: #

while(resolution.resolution_status):
    resolution.update_background()
    if(resolution.resolution_a.render()):
        resolution.set_resolution(1280, 720)
        break

    if(resolution.resolution_b.render()):
        resolution.set_resolution(1920, 1080)
        break

    resolution.update_window()

# Graphics: #

graphics = Graphics(game)

# Graphics Selection: #

while(graphics.graphics_status):
    graphics.update_background()
    if(graphics.effects.render()):
        graphics.set_effects()

    if(graphics.start.render()):
        break

    graphics.update_window()

# Start Window:

game.start_window(sounds)

# Particles:

particles = Particles(game)

# World:

world = World(game, particles)

# Assets Manager:

assets_manager = AssetsManager(game)

# Menu: #

menu = Menu(game, assets_manager)

# Editor:

editor = Editor(game, world, assets_manager, menu)

# User Interface:

ui = UserInterface(game)

# Game Icon: 

game.set_game_icon('assets/Player/Idle/0.png')

# Tiles:

assets_manager.load_pickups()
world.load_tiles()

# World: #

world.set_game_level(1)

# Fade In:

start_fade = Fade(game, 1, ((0, 0, 0)))
end_fade = Fade(game, 2, ((0, 0, 0)))

# Game Loop: #

while(game.engine_running):
	game.set_background(assets_manager)
	if(game.menu_on):
		menu.handle_menu(world)
		start_fade.reset()
	else:
		if(game.editor_status):
			editor.generate_editor_world()
			editor.draw_world()
			editor.draw_grid()
			editor.draw_user_interface()
			editor.draw_information()
			editor.handle_buttons()
			if(start_fade.fade()):
				editor.handle_editor()
		else:
			game.update_game_mechanics(world, particles)
			game.draw_game_sprites(world, ui)
			particles.draw_game_particles()
			menu.check_death(world, start_fade, end_fade)
			if(start_fade.fade()):
				game.start_game()
				game.start_level()

	game.update_display(60)