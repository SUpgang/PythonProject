import random
from MyClasses import *

# init pygame
pygame.init()
pygame.font.init()
my_screen = pygame.display.set_mode((800, 500))
## init pygame font
# font_size = 20
# myfont = pygame.font.SysFont('Comic Sans MS', font_size)

my_game_session = GameSession(screen=my_screen)

while my_game_session.live:

    my_game_session.gameloop()
    pygame.display.flip()

pygame.quit()
quit()

# ALLES AB HIER WIRD IGNORIERT

# Game settings
number_of_lanes = 8
car_starting_lane = 1
car_current_lane = car_starting_lane
tick = 0
delta_px_per_tick = 2
cycle = int(lane_height/delta_px_per_tick)
p = 0
enemy_list = []
player_collision_rect = pygame.Rect((20, 400), (60, 100))
player_alive = True

while game_live:
    myclock.tick(FPS)

    # Delete previous content
    screen.fill(mycolors.black)

    # Fill up the streets:
    for i in range(number_of_lanes):
        shift_px_y = delta_px_per_tick*tick%cycle
        screen.blit(lane_image, (lane_width*i, shift_px_y))
        screen.blit(lane_image, (lane_width*i, -lane_height + shift_px_y))

    player_pos_x, player_pos_y = lane_width*(car_current_lane-1) + 20, 400
    screen.blit(car_image, (player_pos_x, player_pos_y))
    player_collision_rect = pygame.Rect((player_pos_x, player_pos_y), (60, 100))
    #pygame.draw.rect(screen, mycolors.black, player_collision_rect, 1)

    # Create enemies
    if random.random() < p:
        starting_lane = random.randint(1, number_of_lanes)
        new_enemy = MyClasses.Enemy(starting_lane=starting_lane)
        #print('Try to spawn new car at lane {}'.format(starting_lane))

        spawning_collision = False
        for enemy in enemy_list:
            if new_enemy.collision_rect.colliderect(enemy.collision_rect):
                spawning_collision = True
                #print('Did not spawn at lane {}'.format(starting_lane))

        if not spawning_collision:
            enemy_list.append(new_enemy)
        p = 0
    else:
        p += round(1 / ((len(enemy_list)+1)*FPS*50),6)

    for i, enemy in enumerate(enemy_list):
        if player_alive:
            enemy.update_position()
        screen.blit(enemy.image, (enemy.pos_x, enemy.pos_y))
        #pygame.draw.rect(screen, mycolors.black, enemy.collision_rect, 1)
        if enemy.pos_y > SCREEN_HEIGHT:
            enemy_list.pop(i)
        if player_collision_rect.colliderect(enemy.collision_rect):
            player_alive = False
            #print("dead at tick {}".format(tick))

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_live = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car_current_lane = max(1, car_current_lane - 1)
            if event.key == pygame.K_RIGHT:
                car_current_lane = min(number_of_lanes, car_current_lane + 1)

    # Show drawings on screen
    pygame.display.flip()
    if player_alive:
        tick += 1

# Quit game after loop
pygame.quit()
quit()
