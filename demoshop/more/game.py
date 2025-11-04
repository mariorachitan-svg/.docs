import pygame as pg
import random

pg.init()

WIDTH, HEIGHT = 640, 480
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Command Shape Summoner")

font = pg.font.SysFont(None, 32)

command = ""
shapes = []  # {"type": "circle", "pos": (x,y), "color": (r,g,b)}
colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

selected_index = None
MOVE_SPEED = 5

clock = pg.time.Clock()
running = True

while running:
    screen.fill((0,0,0))

    # Draw shapes
    for idx, shape in enumerate(shapes):
        x, y = shape["pos"]
        color = shape["color"]
        if idx == selected_index:
            # highlight selected shape
            outline_color = (255, 255, 255)
        else:
            outline_color = color

        if shape["type"] == "circle":
            pg.draw.circle(screen, color, (x,y), 30)
            if idx == selected_index: pg.draw.circle(screen, outline_color, (x,y), 32, 2)
        elif shape["type"] == "square":
            pg.draw.rect(screen, color, (x-25,y-25,50,50))
            if idx == selected_index: pg.draw.rect(screen, outline_color, (x-27,y-27,54,54),2)
        elif shape["type"] == "triangle":
            points = [(x,y-30),(x-30,y+30),(x+30,y+30)]
            pg.draw.polygon(screen, color, points)
            if idx == selected_index: pg.draw.polygon(screen, outline_color, points,2)
        elif shape["type"] == "rectangle":
            pg.draw.rect(screen, color, (x-40,y-20,80,40))
            if idx == selected_index: pg.draw.rect(screen, outline_color, (x-42,y-22,84,44),2)
        elif shape["type"] == "ellipse":
            pg.draw.ellipse(screen, color, (x-40,y-20,80,40))
            if idx == selected_index: pg.draw.ellipse(screen, outline_color, (x-42,y-22,84,44),2)
        elif shape["type"] == "line":
            pg.draw.line(screen, color, (x-40,y-20),(x+40,y+20),3)
            if idx == selected_index: pg.draw.line(screen, outline_color, (x-40,y-20),(x+40,y+20),1)
        elif shape["type"] == "arrow":
            points = [(x-20,y-10),(x+20,y),(x-20,y+10)]
            pg.draw.polygon(screen, color, points)
            if idx == selected_index: pg.draw.polygon(screen, outline_color, points,2)
        elif shape["type"] == "polygon":
            points = [(x-20,y-20),(x+20,y-20),(x+30,y+20),(x-30,y+20)]
            pg.draw.polygon(screen, color, points)
            if idx == selected_index: pg.draw.polygon(screen, outline_color, points,2)
        elif shape["type"] == "cylinder":
            pg.draw.ellipse(screen, color, (x-20,y-30,40,20))
            pg.draw.rect(screen, color, (x-20,y-20,40,60))
            pg.draw.ellipse(screen, color, (x-20,y+40,40,20))
            if idx == selected_index:
                pg.draw.ellipse(screen, outline_color, (x-22,y-32,44,24),2)
                pg.draw.rect(screen, outline_color, (x-22,y-22,44,64),2)
                pg.draw.ellipse(screen, outline_color, (x-22,y+38,44,24),2)

    # Draw command bar
    pg.draw.rect(screen, (50,50,50), (0, HEIGHT-40, WIDTH, 40))
    cmd_surface = font.render("> " + command, True, (255,255,255))
    screen.blit(cmd_surface, (5, HEIGHT-35))

    pg.display.flip()

    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            # Command typing
            if event.key == pg.K_RETURN:
                if command.lower() in ["circle","square","triangle","rectangle","line","arrow","ellipse","polygon","cylinder"]:
                    shapes.append({
                        "type": command.lower(),
                        "pos": (random.randint(50,WIDTH-50), random.randint(50,HEIGHT-100)),
                        "color": colors[len(shapes)%len(colors)]
                    })
                    print(f"{command} summoned!")
                command = ""
            elif event.key == pg.K_BACKSPACE:
                command = command[:-1]
            elif event.unicode.isprintable():
                command += event.unicode
            # Select shape with number keys
            elif pg.K_1 <= event.key <= pg.K_9:
                idx = event.key - pg.K_1
                if idx < len(shapes):
                    selected_index = idx

    # Arrow key movement for selected shape
    keys = pg.key.get_pressed()
    if selected_index is not None:
        x, y = shapes[selected_index]["pos"]
        if keys[pg.K_UP]:
            y -= MOVE_SPEED
        if keys[pg.K_DOWN]:
            y += MOVE_SPEED
        if keys[pg.K_LEFT]:
            x -= MOVE_SPEED
        if keys[pg.K_RIGHT]:
            x += MOVE_SPEED
        shapes[selected_index]["pos"] = (x,y)

    clock.tick(60)

pg.quit()
