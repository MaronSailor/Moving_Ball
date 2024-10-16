# Move a ball. Left click to spawn and drag the ball. Right click to despawn ball
import pygame
import math

Screen_Height, Screen_Width = 720, 720

pygame.init()

Screen = pygame.display.set_mode((Screen_Width, Screen_Height))

Ball_Created = False
Ball_Y_Coordinate = -100
Ball_X_Coordinate = -100
Ball_Radius = 50

Mouse_Position = -100, -100
Mouse_Pressed = False
Dragging = False
Offset_X = 0
Offset_Y = 0
Velocity_X = 0
Velocity_Y = 0
Friction = 1  # Friction coefficient to gradually slow down the ball

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            Mouse_Position = pygame.mouse.get_pos()
            Mouse_Pressed = True
            # Check if mouse click is on the ball
            if Ball_Created:
                distance = math.sqrt((Mouse_Position[0] - Ball_X_Coordinate) ** 2 + (Mouse_Position[1] - Ball_Y_Coordinate) ** 2)
                if distance <= Ball_Radius:
                    Dragging = True
                    Offset_X = Ball_X_Coordinate - Mouse_Position[0]
                    Offset_Y = Ball_Y_Coordinate - Mouse_Position[1]
                    Velocity_X = 0 
                    Velocity_Y = 0
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            Mouse_Pressed = False
            Dragging = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            Ball_X_Coordinate, Ball_Y_Coordinate = -100, -100
            Ball_Created = False
            Friction = 1
            Velocity_X, Velocity_Y = 0,0

    Screen.fill("White")
    Ball = pygame.draw.circle(Screen,"Black",(Ball_X_Coordinate, Ball_Y_Coordinate),Ball_Radius,Ball_Radius)

    if not Ball_Created and Mouse_Pressed:
        Ball_X_Coordinate, Ball_Y_Coordinate = Mouse_Position
        Ball_Created = True

    if Dragging:
        Mouse_Position = pygame.mouse.get_pos()
        Velocity_X = (Mouse_Position[0] + Offset_X - Ball_X_Coordinate) * 0.1  # Adjust the multiplier to control sensitivity
        Velocity_Y = (Mouse_Position[1] + Offset_Y - Ball_Y_Coordinate) * 0.1

    # Update ball position based on velocity
    Ball_X_Coordinate += Velocity_X
    Ball_Y_Coordinate += Velocity_Y

    # Apply friction to gradually slow down the ball
    Velocity_X *= Friction
    Velocity_Y *= Friction

    if (Ball_X_Coordinate - Ball_Radius <= 0 or Ball_X_Coordinate + Ball_Radius >= Screen_Width) and Ball_Created:
        Velocity_X = -Velocity_X
        Friction += 0.00000 # If ball touches the wall - it changes it's speed, if number is not 0. Try to keep it less than 0.0001 otherwise it will speed up too much
        print(Velocity_Y, "   ",Velocity_X, "   ", Friction)
    # Bounce off the floor and ceiling
    if (Ball_Y_Coordinate - Ball_Radius <= 0 or Ball_Y_Coordinate + Ball_Radius >= Screen_Height) and Ball_Created:
        Velocity_Y = -Velocity_Y
        Friction += 0.00000
        print(Velocity_Y, "   ",Velocity_X, "   ", Friction)

    pygame.display.flip()
