import pygame, math, random
from button import Button

def run(category_words, images, background, click_sound, limb_sound):
    W, H = 850, 500
    window = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Hangman Game")

    # for starting the game theme when the round begins
    pygame.mixer.music.stop()
    pygame.mixer.music.load("theme.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    hangman_status = 0
    word = random.choice(category_words)  # for picking a word from the selected category
    guessed = []
    bloody_red = (139, 0, 0)
    bone_white = (245, 245, 220)

    # for preparing the letter buttons
    radius = 20
    gap = 15
    letters = []
    startx = round((W - (radius * 2 + gap) * 13) / 2)
    starty = 400
    A = 65
    for i in range(26):
        x = startx + gap * 2 + ((radius * 2 + gap) * (i % 13))
        y = starty + ((i // 13) * (gap + radius * 2))
        letters.append([x, y, chr(A + i), True])

    # For loading  fonts
    pixel_font_path = "joystix monospace.otf"
    letter_font = pygame.font.Font(pixel_font_path, 30)
    word_font = pygame.font.Font(pixel_font_path, 30)
    title_font = pygame.font.Font(pixel_font_path, 30)

    FPS = 60
    clock = pygame.time.Clock()
    running = True
    result = None

    def draw():
        # For drawing the background and current skeleton stage
        window.blit(background, (0, 0))
        window.blit(images[hangman_status], (0, 0))

        # for drawing the title
        text = title_font.render("HANGMAN BY GROUP 3", True, bone_white)
        window.blit(text, (W/2 - text.get_width()/2, 20))

        # for drawing the word with guessed letters
        display_word = "".join([ltr+" " if ltr in guessed else "_ " for ltr in word])
        text = word_font.render(display_word, True, bloody_red)
        window.blit(text, (20, 280))

        # for drawing the letter buttons
        for x, y, ltr, visible in letters:
            if visible:
                pygame.draw.circle(window, bone_white, (x, y), radius, 3)
                text = letter_font.render(ltr, True, bloody_red)
                window.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

        pygame.display.update()

    def end_screen(message):
        # for showing the end screen with options
        while True:
            window.fill(bone_white)
            text = word_font.render(message, True, bloody_red)
            window.blit(text, (W/2 - text.get_width()/2, 150))

            play_again_btn = Button(image=None, pos=(W/2, 250),
                                    text_input="PLAY AGAIN", font=word_font,
                                    base_color="Black", hovering_color="Green")
            menu_btn = Button(image=None, pos=(W/2, 320),
                              text_input="MAIN MENU", font=word_font,
                              base_color="Black", hovering_color="Red")

            mouse_pos = pygame.mouse.get_pos()
            for btn in [play_again_btn, menu_btn]:
                btn.changeColor(mouse_pos)
                btn.update(window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_sound.play()
                    if play_again_btn.checkForInput(mouse_pos):
                        return "category"
                    if menu_btn.checkForInput(mouse_pos):
                        return "main_menu"

            pygame.display.update()

    def handle_win():
        limb_sound.stop()
        pygame.mixer.music.stop()
        window.fill(bone_white)
        text = word_font.render("YOU WON!", True, bloody_red)
        window.blit(text, (W//2 - text.get_width()//2, H//2 - text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.mixer.music.load("menu.mp3")
        pygame.mixer.music.play(-1)
        return "YOU WON!"

    def handle_loss():
        limb_sound.stop()
        pygame.mixer.music.stop()
        # Shows final skeleton image first
        draw()
        pygame.display.update()
        pygame.time.delay(1000)  # pause so limb 6 is visible

        # Then show loss message
        window.fill(bone_white)
        text = word_font.render("YOU LOST!", True, bloody_red)
        window.blit(text, (W//2 - text.get_width()//2, H//2 - text.get_height()//2))
        pygame.display.update()
        pygame.time.delay(2000)

        pygame.mixer.music.load("menu.mp3")
        pygame.mixer.music.play(-1)
        return "YOU LOST!"

    # for running the main loop for a round
    while running:
        clock.tick(FPS)
        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - mousex)**2 + (y - mousey)**2)
                        if dis < radius:
                            letter[3] = False
                            click_sound.play()
                            guessed.append(ltr.upper())
                            if ltr not in word:
                                hangman_status = min(hangman_status + 1, 6)
                                if hangman_status == 5:
                                    pygame.mixer.music.stop()
                                    limb_sound.play()
                                    draw()
                                    pygame.display.update()

        # Check win
        won = all(letter in guessed for letter in word)
        if won:
            running = False
            # Reveal all letters before showing win
            guessed = list(word)
            draw()
            pygame.display.update()
            pygame.time.delay(1000)
            result = handle_win()

        # Check loss
        if hangman_status >= 6:
            running = False
            result = handle_loss()

    if result:
        return end_screen(result)
    return "main_menu"

