# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                        Land Invasion, shooter video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from engine import *

# Window Creation: #

window = Window(1024, 768, "Land Invasion:")
window.init()

# Game Loop: #

while(window.engineRunning):
	window.limitFPS(60)
	window.updateDisplay()
window.quit()