import pygame, sys
from button import Button
import hangman   # import your Hangman function

pygame.init()
pygame.mixer.init()

# ---------------- SCREEN SETUP ----------------
SCREEN = pygame.display.set_mode((850, 500))
pygame.display.set_caption("Menu")

# ---------------- BACKGROUND ----------------
BG = pygame.image.load("yehey.png")
BG = pygame.transform.scale(BG, (850, 500))

# ---------------- PRELOAD ASSETS ----------------
# I load skeleton images, background, and sounds once to avoid lag
skeleton_images = [pygame.transform.scale(pygame.image.load(f"skeleton{i}.png"), (850, 500)) for i in range(7)]
background = pygame.transform.scale(pygame.image.load("stage.png"), (850, 500))
click_sound = pygame.mixer.Sound("boom.wav")       # short click sound
limb_sound = pygame.mixer.Sound("limb.mp3")        # limb sound effect

# ---------------- MENU MUSIC ----------------
pygame.mixer.music.load("menu.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# ---------------- FONT HELPER ----------------
def get_font(size):
    return pygame.font.Font("joystix monospace.otf", size)

# ---------------- CATEGORY MENU ----------------
def category_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        CAT_MOUSE_POS = pygame.mouse.get_pos()
        center_x = SCREEN.get_width() // 2

        # Title
        CAT_TEXT = get_font(60).render("SELECT CATEGORY", True, "#b68f40")
        SCREEN.blit(CAT_TEXT, CAT_TEXT.get_rect(center=(center_x, 80)))

        # Category buttons
        fruits_btn = Button(image=None, pos=(center_x, 180),
                            text_input="FRUITS", font=get_font(40),
                            base_color="White", hovering_color="Green")
        games_btn = Button(image=None, pos=(center_x, 260),
                           text_input="GAMES", font=get_font(40),
                           base_color="White", hovering_color="Green")
        group3_mem = Button(image=None, pos=(center_x, 340),
                             text_input="GROUP3 MEMBERS", font=get_font(40),
                             base_color="White", hovering_color="Green")
        back_btn = Button(image=None, pos=(center_x, 420),
                          text_input="BACK", font=get_font(40),
                          base_color="White", hovering_color="Red")

        # Update button states
        for button in [fruits_btn, games_btn, group3_mem, back_btn]:
            button.changeColor(CAT_MOUSE_POS)
            button.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fruits_btn.checkForInput(CAT_MOUSE_POS):
                    click_sound.play()
                    result = hangman.run(["APPLE","MANGO","BANANA","ORANGE"],
                                         skeleton_images, background, click_sound, limb_sound)
                elif games_btn.checkForInput(CAT_MOUSE_POS):
                    click_sound.play()
                    result = hangman.run(["MINECRAFT","ROBLOX","VALORANT","FORTNITE"],
                                         skeleton_images, background, click_sound, limb_sound)
                elif group3_mem.checkForInput(CAT_MOUSE_POS):
                    click_sound.play()
                    result = hangman.run(["THANIEL","AYEN","MARC","MITUDA","JUAN", "AZALEA", "GIMEL","JOSEPH","SEBIDO"],
                                         skeleton_images, background, click_sound, limb_sound)
                elif back_btn.checkForInput(CAT_MOUSE_POS):
                    click_sound.play()
                    return

                # Handle return values from hangman
                if result == "category":
                    continue
                elif result == "main_menu":
                    pygame.mixer.music.load("menu.mp3")
                    pygame.mixer.music.play(-1)
                    return
                elif result == "quit":
                    pygame.quit(); sys.exit()

        pygame.display.update()

# ---------------- INSTRUCTIONS MENU ----------------
def instructions():
    while True:
        SCREEN.blit(BG, (0, 0))
        INSTR_MOUSE_POS = pygame.mouse.get_pos()
        center_x = SCREEN.get_width() // 2

        # Title
        INSTR_TEXT = get_font(50).render("HOW TO PLAY", True, "#b68f40")
        SCREEN.blit(INSTR_TEXT, INSTR_TEXT.get_rect(center=(center_x, 80)))

        # Instruction lines
        lines = [
            "1. Select a category to start.",
            "2. Guess letters by clicking the buttons.",
            "3. Correct guesses reveal the word.",
            "4. Wrong guesses add to the skeleton.",
            "5. Win by guessing the word before",
            "   the skeleton is complete!"
        ]
        y_offset = 160
        for line in lines:
            text = get_font(25).render(line, True, "White")
            SCREEN.blit(text, text.get_rect(center=(center_x, y_offset)))
            y_offset += 40

        # Back button
        BACK_BUTTON = Button(image=None, pos=(center_x, 420),
                             text_input="BACK", font=get_font(40),
                             base_color="White", hovering_color="Green")
        BACK_BUTTON.changeColor(INSTR_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(INSTR_MOUSE_POS):
                    click_sound.play()
                    return

        pygame.display.update()

# ---------------- MAIN MENU ----------------
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        center_x = SCREEN.get_width() // 2

        # Title
        MENU_TEXT = get_font(70).render("MAIN MENU", True, "#b68f40")
        SCREEN.blit(MENU_TEXT, MENU_TEXT.get_rect(center=(center_x, 80)))

        # Buttons
        PLAY_BUTTON = Button(image=None, pos=(center_x, 180),
                             text_input="PLAY", font=get_font(50),
                             base_color="White", hovering_color="Green")
        INSTR_BUTTON = Button(image=None, pos=(center_x, 260),
                              text_input="INSTRUCTIONS", font=get_font(40),
                              base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=None, pos=(center_x, 340),
                             text_input="QUIT", font=get_font(50),
                             base_color="White", hovering_color="Red")

        # Update button states
        for button in [PLAY_BUTTON, INSTR_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    result = category_menu()
                    if result == "quit":
                        pygame.quit(); sys.exit()
                    elif result == "main_menu":
                        return
                if INSTR_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    instructions()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    pygame.quit(); sys.exit()

        pygame.display.update()

# ---------------- START PROGRAM ----------------
main_menu()