import pygame , random , time , unicodedata

pygame.init() # Initialize PyGame
pygame.mixer.init() # Initialize PyGame Mixer

# Read all lines from the Words.txt file
# to obtain our word list
with open("words.txt" , "r" , encoding="utf-8") as file:
    WORDS = file.readlines()

# Program constants and global variables
WIDTH = HEIGHT = 640
CLOCK = pygame.time.Clock()

FONT = pygame.font.SysFont("consolas", 24)
BIG_FONT = pygame.font.SysFont("consolas", 36)

BACKSPACE = pygame.mixer.Sound("./sounds/backspace.wav")
SPACE = pygame.mixer.Sound("./sounds/space.wav")
ENTER = pygame.mixer.Sound("./sounds/enter.wav")

KEY = "real"

INPUT = ""; EXPECTED_INPUT = random.choice(WORDS)
START_TIME = None; END_TIME = None
WORD_COUNT = 0; CORRECT_WORDS = 0; MAX_WORDS = 7
DONE_TYPING = False

# Create the PyGame window with fixed width and height
# and set the window title to 'Speed Typer'
SCREEN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Speed Typer")

# Normalize unicode values
def normalize(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8").lower().strip()

running = True
while running:
    
    CLOCK.tick(60)

    SCREEN.fill((30 , 30 , 30))

    # Title text
    title = BIG_FONT.render("Yazı Yazma Testi", True, (255, 153, 20))
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # If typing is not finished, display
    # the expected word and user input
    if not DONE_TYPING:
        prompt = FONT.render(EXPECTED_INPUT, True, (255, 255, 255))
        SCREEN.blit(prompt, ((WIDTH - prompt.get_width()) // 2 , 120))

        # Each character of the user input is indexed.
        # If the character matches the expected input
        # at the same index, it is drawn in green,
        # otherwise in red.
        writtenWidth = sum(FONT.size(c)[0] for c in INPUT) # Sum the width of typed characters
        remainingWidth = sum(FONT.size(c)[0] for c in EXPECTED_INPUT[len(INPUT):]) # Sum width of remaining characters
        totalWidth = writtenWidth + remainingWidth # Calculate total width

        # Subtract total word width from screen width and divide by two
        # to properly center the word
        x = (WIDTH - totalWidth) // 2 ; y = HEIGHT // 2
        for i, char in enumerate(INPUT):
            if i < len(EXPECTED_INPUT):
                color = (0, 255, 0) if char == EXPECTED_INPUT[i] else (255, 50, 50)
            else:
                color = (255, 50, 50)  # Extra characters are shown in red
            charSurf = FONT.render(char, True, color)
            SCREEN.blit(charSurf, (x , y))
            x += charSurf.get_width()

        # Using the lengths of user input and expected input,
        # create a range of remaining characters and draw them
        # in gray (characters not yet typed by the user)
        for i in range(len(INPUT), len(EXPECTED_INPUT)):
            charSurf = FONT.render(EXPECTED_INPUT[i], True, (150, 150, 150))
            SCREEN.blit(charSurf, (x , y))
            x += charSurf.get_width()

    # As long as the start time is set and typing
    # is not marked as finished, this block
    # displays the elapsed time

    # When typing is finished,
    # total time, words per minute,
    # and correct word count are displayed
    if START_TIME and not DONE_TYPING:
        elapsed = time.time() - START_TIME
        timer = FONT.render(f"Süre: {round(elapsed, 1)} sn", True, (200, 200, 255))
        SCREEN.blit(timer, (WIDTH // 2 - timer.get_width() // 2 , 70))
    elif DONE_TYPING:
        elapsed = END_TIME - START_TIME
        wpm = CORRECT_WORDS / (elapsed / 60)

        resultFirstLine = FONT.render(f"Toplam Süre: {round(elapsed, 2)} sn", True, (36, 145, 255))
        SCREEN.blit(resultFirstLine , ((WIDTH - resultFirstLine.get_width()) // 2 , 250))

        resultSecondLine = FONT.render(
            f"Doğru Kelime: {CORRECT_WORDS} | Hız: {str(wpm)[:4]} WPM ",
            True,
            (36, 145, 255)
        )
        SCREEN.blit(resultSecondLine , ((WIDTH - resultSecondLine.get_width()) // 2 , 290))

        prompt = FONT.render("Yeniden başlamak için Enter'a bas.", True, (169, 190, 212))
        SCREEN.blit(prompt, ((WIDTH - prompt.get_width()) // 2 , 330))

    pygame.display.update() # Update the screen

    # Poll events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Triggered when a key is pressed
        # If typing is finished and Enter is pressed,
        # the program resets and starts over
        elif event.type == pygame.KEYDOWN:
            if DONE_TYPING:
                if event.key == pygame.K_RETURN:

                    ENTER.play()
                    
                    INPUT = ""; EXPECTED_INPUT = random.choice(WORDS)
                    START_TIME = None; END_TIME = None
                    WORD_COUNT = 0; CORRECT_WORDS = 0
                    DONE_TYPING = False

                continue
            
            # Set start time if not already set
            if not START_TIME:
                START_TIME = time.time()

            if event.key == pygame.K_BACKSPACE: # When backspace is pressed, remove the last character
                BACKSPACE.play()
                INPUT = INPUT[:-1]

            # When space is pressed, word count increases
            # User input and expected input are normalized and compared
            # If they match, correct word count increases
            elif event.key == pygame.K_SPACE:
                SPACE.play()
                WORD_COUNT += 1
                if normalize(INPUT.strip()) == normalize(EXPECTED_INPUT):
                    CORRECT_WORDS += 1
                
                INPUT = ""
                if WORD_COUNT >= MAX_WORDS: # If max word count is reached, typing is finished
                    DONE_TYPING = True
                    END_TIME = time.time() # Set end time when typing is completed
                    break

                EXPECTED_INPUT = random.choice(WORDS) # Load a new expected word and continue

            else:
                pygame.mixer.Sound(f'./sounds/{random.randint(1,5)}{KEY}.wav').play()
                # If the key produces a printable character,
                # convert it to lowercase and add it to user input
                if event.unicode.isprintable():
                    INPUT += event.unicode.lower()

pygame.quit() # Exit PyGame when the loop ends
