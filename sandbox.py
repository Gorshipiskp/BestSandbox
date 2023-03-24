import random
import time
import pygame
import pygame_widgets
from pygame_widgets.button import Button
import base_sandbox
from base_sandbox import Matrix, Pixel

time_play = 0
WID, HEI = 160, 120
MENU_WIDTH = 250
SCALE = 6
FPS = 0
st = time.time()


def main():
    pygame.init()

    global select_pix
    select_pix = 'sand'
    playing = True
    screen = pygame.display.set_mode((WID * SCALE + 15 * SCALE, HEI * SCALE))
    pygame.display.set_caption("Sandbox")
    new_surf = pygame.PixelArray(pygame.Surface(size=(WID, HEI)))
    new_surf.surface.fill(Pixel('air').info['color'])
    clock = pygame.time.Clock()

    matx = Matrix((WID, HEI))

    def change_pix(type_pix):
        global select_pix
        select_pix = type_pix

    shift = 0
    for name, vals in base_sandbox.mats.items():
        Button(
            screen, 5, 5 + 35 * shift, MENU_WIDTH - 15, 30, text=vals['name'],
            fontSize=30, margin=5,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=5,
            onClick=change_pix,
            onClickParams=(name, )
        )
        shift += 1

    while playing and ((time.time() - st < time_play) or not time_play):
        edited = matx.iteration()

        for coords_m in edited:
            for coords in coords_m:
                new_surf.surface.set_at((coords[0], coords[1]), matx.matrix[coords[0]][coords[1]].info['color'])
        background = pygame.transform.scale(new_surf.make_surface(), (WID * SCALE, HEI * SCALE))

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            pos = (pos[0] - MENU_WIDTH) // SCALE, pos[1] // SCALE

            if pos[0] >= 0 and pos[1] >= 0:
                matx[pos[0], pos[1]] = Pixel(select_pix)
                new_surf.surface.set_at((pos[0], pos[1]), matx.matrix[pos[0]][pos[1]].info['color'])

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        pygame_widgets.update(pygame.event.get())  # Call once every loop to allow widgets to render and listen
        pygame.display.update()

        screen.blit(background, (MENU_WIDTH, 0))
        pygame.display.flip()
    else:
        print(f"TOTAL ITERATION: {matx.iter_num} ({round(matx.iter_num / (time.time() - st), 2)}iter/s)")


if __name__ == "__main__":
    main()
