from classes import *
from esc import menu
from part import *


def check_camera(arrow, board):
    if pygame.display.Info().current_w * 0.05 >= arrow.pos[0]:
        board.camera_update((0, -5))
    if pygame.display.Info().current_w * 0.95 <= arrow.pos[0]:
        board.camera_update((0, 5))
    if pygame.display.Info().current_h * 0.05 >= arrow.pos[1]:
        board.camera_update((-5, 0))
    if pygame.display.Info().current_h * 0.95 <= arrow.pos[1]:
        board.camera_update((5, 0))


def print_info(players):
    for player in players:
        print(player.name + ':')
        for objects in player.own:
            print(objects.__class__.__name__, objects.get_coords())
        print()


def update_players(players, player):
    for i in range(len(players)):
        if players[i].color == player.color:
            players[i] = player
    return players


def check_player(players, color):
    check_main_town = False
    for player in players:
        if player.color == color:
            for object in player.own:
                if object.__class__ == Town and object.is_main_town:
                    check_main_town = True
    return check_main_town


def check_active_players(players, color):
    for player in players:
        if player.color == color:
            continue
        if player.active:
            return True
    return False


def game(width, height, screen, arrow, music_box, lvl_name):
    FPS = 120
    WIDTH = width
    HEIGHT = height
    running = True

    newturnanimation = AnimatedSprite(newturnanim, 15, count=1)

    clock = pygame.time.Clock()
    board = Board()
    board.board, players, cur_player = load_level(lvl_name)
    board.set_up(players, cur_player)
    hud = Hud((width, height))
    next_player_index = players.index(cur_player) + 1

    blow = Explotion(screen, 10, 50, False, (255, 255, 255), (255, 255, 255))

    next_player = players[next_player_index % len(players)]
    cur_player.update()

    button_town = Button((WIDTH - 275, 30), 'Build Town')
    button_gun = Button((WIDTH - 275, 90), 'Set Gun')
    button_block = Button((WIDTH - 275, 150), 'Set Block')
    button_destroy = Button((WIDTH - 275, 210), 'Destroy')
    button_end_turn = Button((WIDTH - 275, HEIGHT - 80), 'End Turn')

    buttons = [button_town, button_gun, button_block, button_destroy, button_end_turn]
    pygame.mouse.set_visible(0)

    hud.set_turned_text(cur_player.name, cur_player)
    arrow.changed_turn(cur_player)

    x1, y1, mouse_x, mouse_y = 0, 0, 0, 0
    blow_x, blow_y = 0, 0
    choosen = '.'
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    board.change_delta(5)
                elif event.button == 4:
                    board.change_delta(-5)
                else:
                    click.play()

                    for button in buttons:
                        if button.check(event.pos):
                            button.press()
                            choosen = button.text
                    x1, y1 = board.get_click(event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button != 5 and event.button != 4:
                    if board.get_click(event.pos) == (x1, y1) and board.on_screen(event.pos, (width, height)):
                        if x1 is not None and y1 is not None and cur_player.actions > 0:
                            if board.board[x1][y1] is None or board.board[x1][y1].player == cur_player.color:
                                if board.prepared == 'destroy' and board.board[x1][y1] is not None:
                                    cur_player.own.pop(cur_player.own.index(board.board[x1][y1]))
                                    board.destroy_object(x1, y1)
                                    players = update_players(players, cur_player)
                                    if not check_player(players, cur_player.color):
                                        cur_player.active = False
                                        for objects in cur_player.own:
                                            if objects:
                                                x, y = objects.get_coords()
                                                board.destroy_object(x, y)
                                        newturnanimation.activate()
                                        arrow.change_mode('Default')

                                        cur_player = next_player
                                        arrow.changed_turn(cur_player)
                                        next_player_index += 1
                                        next_player = players[next_player_index % len(players)]
                                        while not cur_player.active:
                                            cur_player = next_player
                                            arrow.changed_turn(cur_player)
                                            next_player_index += 1
                                            next_player = players[next_player_index % len(players)]
                                        cur_player.actions_update()
                                        board.turned_player = cur_player
                                        hud.set_turned_text(cur_player.name, cur_player)
                                        board.choosed_gun = None
                                        newturn.play()
                                        for player in players:
                                            if not check_active_players(players, player.color):
                                                win(player.color, screen, width, height)
                                                running = False
                                        players = update_players(players, cur_player)
                                    cur_player.use_action()
                                    hud.update_actions()
                                elif board.board[x1][y1] is not None:
                                    if board.board[x1][y1].to_be_built != board.board[x1][y1].build_actions:
                                        board.board[x1][y1].build()
                                        cur_player.use_action()
                                        hud.update_actions()
                                    elif board.board[x1][y1].__class__.__name__ == 'Gun':
                                        board.choosed_gun = board.board[x1][y1]

                                elif board.prepared is not None and board.board[x1][y1] is None and board.possible(y1,
                                                                                                                   x1,
                                                                                                                   cur_player.color):
                                    game_object = board.prepared(x1, y1, cur_player.color, all_sprites)
                                    board.board[x1][y1] = game_object
                                    board.prepared = None
                                    board.board[x1][y1].build_actions = 1
                                    cur_player.add_own(game_object)
                                    cur_player.use_action()
                                    players = update_players(players, cur_player)
                                    hud.update_actions()
                                    arrow.change_mode('Default')
                            elif board.choosed_gun is not None and board.board[x1][y1].player != cur_player.color:
                                if board.board[x1][y1].player != board.choosed_gun.player and board.choosed_gun.can_attack((x1, y1)):
                                    shot.play()
                                    board.board[x1][y1].life -= 1
                                    blow_x, blow_y = event.pos
                                    blow.reload()
                                    if board.board[x1][y1].life == 0:
                                        objects_player = None
                                        for i in range(len(players)):
                                            if players[i].color == board.board[x1][y1].player:
                                                objects_player = players[i]
                                        objects_player.own.pop(objects_player.own.index(board.board[x1][y1]))
                                        board.destroy_object(x1, y1)
                                        if not check_player(players, objects_player.color):
                                            objects_player.active = False
                                            for objects in objects_player.own:
                                                if objects:
                                                    x, y = objects.get_coords()
                                                    board.destroy_object(x, y)
                                            if not check_active_players(players, cur_player.color):
                                                win(cur_player.color, screen, width, height)
                                                running = False
                                            players = update_players(players, objects_player)
                                        players = update_players(players, objects_player)
                                        players = update_players(players, cur_player)
                                    board.choosed_gun = None
                                    cur_player.use_action()
                                    hud.update_actions()

                    for button in buttons:
                        if button.check(event.pos) and button.pressed:
                            if choosen == 'Build Town':
                                board.prepare_to_set_object(Town)
                                arrow.change_mode(choosen.split()[1])
                            if choosen == 'Set Gun':
                                board.prepare_to_set_object(Gun)
                                arrow.change_mode(choosen.split()[1])
                            if choosen == 'Set Block':
                                board.prepare_to_set_object(Block)
                                arrow.change_mode(choosen.split()[1])
                            if choosen == 'Destroy':
                                board.prepare_to_destroy_object()
                                arrow.change_mode(choosen)
                            if choosen == 'End Turn':
                                newturnanimation.activate()
                                arrow.change_mode('Default')

                                cur_player = next_player
                                arrow.changed_turn(cur_player)
                                next_player_index += 1
                                next_player = players[next_player_index % len(players)]
                                while not cur_player.active:
                                    cur_player = next_player
                                    arrow.changed_turn(cur_player)
                                    next_player_index += 1
                                    next_player = players[next_player_index % len(players)]
                                cur_player.actions_update()
                                board.turned_player = cur_player
                                hud.set_turned_text(cur_player.name, cur_player)
                                board.choosed_gun = None
                                newturn.play()

                            button.unpress()

                    choosen = '.'
            if event.type == pygame.MOUSEMOTION:
                arrow.change_pos(event.pos)
                for button in buttons:
                    if button.check(event.pos):
                        button.crossing()
                    else:
                        button.crossed = False
                x1, y1 = board.get_click(event.pos)
                if x1 is not None and y1 is not None:
                    hud.draw_info(event.pos, screen, board.board[x1][y1])
                    board.crossing((x1, y1))
                else:
                    board.crossing((None, None))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not menu(width, height, screen, arrow, music_box, board):
                        running = False
                    arrow.change_mode('Default')
        check_camera(arrow, board)
        screen.fill((0, 0, 0))
        board.buildanim.update()
        board.render(screen)
        board.render_crossing(screen)
        hud.update_hud(screen)
        if not (x1 == y1 is None):
            hud.draw_info((x1, y1), screen, board.board[x1][y1])
        for temp_button in buttons:
            temp_button.render(screen)
        newturnanimation.update()
        if newturnanimation.active:
            screen.blit(newturnanimation.image, (0, 0))
        blow.action(blow_x, blow_y)
        music_box.check()
        arrow.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
        # print_info(players)
    arrow.change_mode('Default')
