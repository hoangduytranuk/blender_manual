import bge

def main():
    cont = bge.logic.getCurrentController()
    player = cont.owner

    keyboard = bge.logic.keyboard
    mouse = bge.logic.mouse
    scene = bge.logic.getCurrentScene()

    #move up down, turn left right
    if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.WKEY]:
        player.applyMovement((0, 0.2, 0), True)
    if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.SKEY]:
        player.applyMovement((0, -0.2, 0), True)
    if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.AKEY]:
        player.applyRotation((0, 0, 0.05), True)
    if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.DKEY]:
        player.applyRotation((0, 0, -0.05), True)
    #framerate = str(bge.logic.getAverageFrameRate())
    #print(framerate[0: 4])
main()        
