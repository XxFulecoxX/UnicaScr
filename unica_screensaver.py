import pygame
import os
import random
import sys
import math

# ============================================================
# UNICA RANDOM ANIMATION SCREENSAVER
# ============================================================

LOGO_FOLDER = "logos"
AUDIO_FOLDER = "audio"

AUDIO_FILE = "audio.mp3"

DISPLAY_TIME = 3.0
ANIMATION_TIME = 1.5

BACKGROUND = (0, 0, 0)

SUPPORTED_IMAGES = (
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".webp"
)

# ============================================================
# INITIALIZE
# ============================================================

pygame.init()

try:
    pygame.mixer.init()
    AUDIO_ENABLED = True
except Exception as error:
    print("Audio system could not start:", error)
    AUDIO_ENABLED = False

screen = pygame.display.set_mode(
    (0, 0),
    pygame.FULLSCREEN
)

pygame.display.set_caption(
    "Unica Random Screensaver"
)

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

clock = pygame.time.Clock()

# ============================================================
# FIND LOGOS
# ============================================================

def find_logos():

    if not os.path.exists(LOGO_FOLDER):
        os.makedirs(LOGO_FOLDER)

    files = []

    for filename in os.listdir(LOGO_FOLDER):

        if not filename.lower().endswith(
            SUPPORTED_IMAGES
        ):
            continue

        if "unica" not in filename.lower():
            continue

        files.append(
            os.path.join(
                LOGO_FOLDER,
                filename
            )
        )

    files.sort()

    return files


logo_files = find_logos()

if not logo_files:

    print()
    print("ERROR: No Unica logos found!")
    print()
    print("Put your Unica images inside:")
    print(LOGO_FOLDER)
    print()

    pygame.quit()
    sys.exit()


# ============================================================
# AUDIO
# ============================================================

def start_audio():

    if not AUDIO_ENABLED:
        return

    audio_path = os.path.join(
        AUDIO_FOLDER,
        AUDIO_FILE
    )

    if not os.path.exists(audio_path):

        print()
        print("No audio.mp3 found.")
        print("Expected:")
        print(audio_path)
        print()

        return

    try:

        pygame.mixer.music.load(
            audio_path
        )

        # -1 = loop forever
        pygame.mixer.music.play(-1)

        print(
            "Audio looping:",
            audio_path
        )

    except Exception as error:

        print(
            "Audio error:",
            error
        )


# ============================================================
# LOAD LOGOS
# ============================================================

logos = []

for filename in logo_files:

    try:

        image = pygame.image.load(
            filename
        ).convert_alpha()

        logos.append(
            (
                os.path.basename(filename),
                image
            )
        )

        print(
            "[LOGO]",
            os.path.basename(filename)
        )

    except Exception as error:

        print(
            "[ERROR]",
            filename,
            error
        )


if not logos:

    print("No logos could be loaded.")

    pygame.quit()
    sys.exit()


# ============================================================
# SCALE LOGO
# ============================================================

def prepare_logo(image):

    width, height = image.get_size()

    max_width = int(
        SCREEN_WIDTH * 0.75
    )

    max_height = int(
        SCREEN_HEIGHT * 0.75
    )

    scale = min(
        max_width / width,
        max_height / height
    )

    new_width = max(
        1,
        int(width * scale)
    )

    new_height = max(
        1,
        int(height * scale)
    )

    return pygame.transform.smoothscale(
        image,
        (
            new_width,
            new_height
        )
    )


# ============================================================
# EXIT
# ============================================================

def check_exit():

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            pygame.mixer.music.stop()

            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            pygame.mixer.music.stop()

            pygame.quit()
            sys.exit()

        if event.type == pygame.QUIT:

            pygame.mixer.music.stop()

            pygame.quit()
            sys.exit()


# ============================================================
# CREATE SHARDS
# ============================================================

def create_shards(image):

    shards = []

    width, height = image.get_size()

    columns = 8
    rows = 6

    shard_width = width / columns
    shard_height = height / rows

    center_x = width / 2
    center_y = height / 2

    for row in range(rows):

        for column in range(columns):

            x = int(
                column * shard_width
            )

            y = int(
                row * shard_height
            )

            w = int(
                shard_width + 1
            )

            h = int(
                shard_height + 1
            )

            shard = pygame.Surface(
                (w, h),
                pygame.SRCALPHA
            )

            shard.blit(
                image,
                (-x, -y)
            )

            shard_center_x = (
                x +
                shard_width / 2
            )

            shard_center_y = (
                y +
                shard_height / 2
            )

            dx = (
                shard_center_x -
                center_x
            )

            dy = (
                shard_center_y -
                center_y
            )

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance == 0:
                distance = 1

            direction_x = dx / distance
            direction_y = dy / distance

            speed = random.uniform(
                150,
                450
            )

            shards.append(
                {
                    "image": shard,
                    "x": x,
                    "y": y,
                    "vx": direction_x * speed,
                    "vy": direction_y * speed,
                    "rotation": random.uniform(
                        -30,
                        30
                    ),
                    "rotation_speed": random.uniform(
                        -500,
                        500
                    )
                }
            )

    return shards


# ============================================================
# SHATTER ANIMATION
# ============================================================

def animation_shatter(
    current_logo,
    next_logo
):

    shards = create_shards(
        current_logo
    )

    logo_width, logo_height = (
        current_logo.get_size()
    )

    logo_x = (
        SCREEN_WIDTH -
        logo_width
    ) // 2

    logo_y = (
        SCREEN_HEIGHT -
        logo_height
    ) // 2

    start = pygame.time.get_ticks()

    while True:

        check_exit()

        elapsed = (
            pygame.time.get_ticks() -
            start
        ) / 1000

        progress = min(
            elapsed / ANIMATION_TIME,
            1
        )

        screen.fill(
            BACKGROUND
        )

        # ----------------------------------------------------
        # NEXT LOGO
        # ----------------------------------------------------

        next_width, next_height = (
            next_logo.get_size()
        )

        flip = abs(
            math.cos(
                progress * math.pi
            )
        )

        draw_width = max(
            1,
            int(
                next_width * flip
            )
        )

        new_logo = pygame.transform.smoothscale(
            next_logo,
            (
                draw_width,
                next_height
            )
        )

        new_logo.set_alpha(
            int(
                255 * progress
            )
        )

        screen.blit(
            new_logo,
            (
                (
                    SCREEN_WIDTH -
                    draw_width
                ) // 2,

                (
                    SCREEN_HEIGHT -
                    next_height
                ) // 2
            )
        )

        # ----------------------------------------------------
        # OLD LOGO SHARDS
        # ----------------------------------------------------

        for shard in shards:

            dt = 1 / 60

            shard["x"] += (
                shard["vx"] * dt
            )

            shard["y"] += (
                shard["vy"] * dt
            )

            shard["rotation"] += (
                shard["rotation_speed"] * dt
            )

            rotated = pygame.transform.rotate(
                shard["image"],
                shard["rotation"]
            )

            rotated.set_alpha(
                int(
                    255 *
                    (1 - progress)
                )
            )

            shard_x = (
                logo_x +
                shard["x"] +
                (
                    shard["image"].get_width() -
                    rotated.get_width()
                ) / 2
            )

            shard_y = (
                logo_y +
                shard["y"] +
                (
                    shard["image"].get_height() -
                    rotated.get_height()
                ) / 2
            )

            screen.blit(
                rotated,
                (
                    int(shard_x),
                    int(shard_y)
                )
            )

        pygame.display.flip()

        clock.tick(60)

        if progress >= 1:
            break


# ============================================================
# 3D FLIP ANIMATION
# ============================================================

def animation_flip(
    current_logo,
    next_logo
):

    start = pygame.time.get_ticks()

    while True:

        check_exit()

        elapsed = (
            pygame.time.get_ticks() -
            start
        ) / 1000

        progress = min(
            elapsed / ANIMATION_TIME,
            1
        )

        screen.fill(
            BACKGROUND
        )

        # ----------------------------------------------------
        # CURRENT LOGO
        # ----------------------------------------------------

        current_scale = max(
            0.01,
            math.cos(
                progress *
                math.pi / 2
            )
        )

        current_width = max(
            1,
            int(
                current_logo.get_width() *
                current_scale
            )
        )

        current = pygame.transform.smoothscale(
            current_logo,
            (
                current_width,
                current_logo.get_height()
            )
        )

        screen.blit(
            current,
            (
                (
                    SCREEN_WIDTH -
                    current_width
                ) // 2,

                (
                    SCREEN_HEIGHT -
                    current_logo.get_height()
                ) // 2
            )
        )

        # ----------------------------------------------------
        # NEXT LOGO
        # ----------------------------------------------------

        next_scale = max(
            0.01,
            math.sin(
                progress *
                math.pi / 2
            )
        )

        next_width = max(
            1,
            int(
                next_logo.get_width() *
                next_scale
            )
        )

        new_logo = pygame.transform.smoothscale(
            next_logo,
            (
                next_width,
                next_logo.get_height()
            )
        )

        screen.blit(
            new_logo,
            (
                (
                    SCREEN_WIDTH -
                    next_width
                ) // 2,

                (
                    SCREEN_HEIGHT -
                    next_logo.get_height()
                ) // 2
            )
        )

        pygame.display.flip()

        clock.tick(60)

        if progress >= 1:
            break


# ============================================================
# SPIN ANIMATION
# ============================================================

def animation_spin(
    current_logo,
    next_logo
):

    start = pygame.time.get_ticks()

    while True:

        check_exit()

        elapsed = (
            pygame.time.get_ticks() -
            start
        ) / 1000

        progress = min(
            elapsed / ANIMATION_TIME,
            1
        )

        screen.fill(
            BACKGROUND
        )

        if progress < 0.5:

            p = progress * 2

            scale = 1 - p

            angle = p * 180

            image = pygame.transform.rotozoom(
                current_logo,
                angle,
                max(
                    0.01,
                    scale
                )
            )

        else:

            p = (
                progress -
                0.5
            ) * 2

            scale = p

            angle = (
                1 - p
            ) * 180

            image = pygame.transform.rotozoom(
                next_logo,
                angle,
                max(
                    0.01,
                    scale
                )
            )

        rect = image.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )
        )

        screen.blit(
            image,
            rect
        )

        pygame.display.flip()

        clock.tick(60)

        if progress >= 1:
            break


# ============================================================
# ZOOM ANIMATION
# ============================================================

def animation_zoom(
    current_logo,
    next_logo
):

    start = pygame.time.get_ticks()

    while True:

        check_exit()

        elapsed = (
            pygame.time.get_ticks() -
            start
        ) / 1000

        progress = min(
            elapsed / ANIMATION_TIME,
            1
        )

        screen.fill(
            BACKGROUND
        )

        if progress < 0.5:

            p = progress * 2

            scale = 1 + (
                p * 3
            )

            image = pygame.transform.smoothscale(
                current_logo,
                (
                    max(
                        1,
                        int(
                            current_logo.get_width() *
                            scale
                        )
                    ),
                    max(
                        1,
                        int(
                            current_logo.get_height() *
                            scale
                        )
                    )
                )
            )

        else:

            p = (
                progress -
                0.5
            ) * 2

            scale = 4 - (
                p * 3
            )

            image = pygame.transform.smoothscale(
                next_logo,
                (
                    max(
                        1,
                        int(
                            next_logo.get_width() *
                            scale
                        )
                    ),
                    max(
                        1,
                        int(
                            next_logo.get_height() *
                            scale
                        )
                    )
                )
            )

        rect = image.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )
        )

        screen.blit(
            image,
            rect
        )

        pygame.display.flip()

        clock.tick(60)

        if progress >= 1:
            break


# ============================================================
# RANDOM ANIMATION
# ============================================================

def random_animation(
    current_logo,
    next_logo
):

    animations = [
        (
            "SHATTER",
            animation_shatter
        ),
        (
            "3D FLIP",
            animation_flip
        ),
        (
            "SPIN",
            animation_spin
        ),
        (
            "ZOOM",
            animation_zoom
        )
    ]

    name, function = random.choice(
        animations
    )

    print(
        "Animation:",
        name
    )

    function(
        current_logo,
        next_logo
    )


# ============================================================
# PREPARE LOGOS
# ============================================================

prepared_logos = []

for filename, image in logos:

    prepared_logos.append(
        (
            filename,
            prepare_logo(image)
        )
    )


# ============================================================
# STARTUP
# ============================================================

print()
print("==============================")
print("   UNICA RANDOM SCREENSAVER")
print("==============================")
print()

print(
    "Loaded",
    len(prepared_logos),
    "logos."
)

print(
    "Animations:",
    "SHATTER / 3D FLIP / SPIN / ZOOM"
)

print(
    "Audio:",
    "audio\\audio.mp3"
)

print()
print(
    "Press any key or click to exit."
)
print()


# ============================================================
# START AUDIO ONCE
# ============================================================

start_audio()


# ============================================================
# FIRST RANDOM LOGO
# ============================================================

current_index = random.randrange(
    len(prepared_logos)
)

current_name, current_logo = (
    prepared_logos[current_index]
)

screen.fill(
    BACKGROUND
)

rect = current_logo.get_rect(
    center=(
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2
    )
)

screen.blit(
    current_logo,
    rect
)

pygame.display.flip()


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    # --------------------------------------------------------
    # HOLD LOGO
    # --------------------------------------------------------

    start_time = pygame.time.get_ticks()

    while (
        pygame.time.get_ticks() -
        start_time
        <
        DISPLAY_TIME * 1000
    ):

        check_exit()

        clock.tick(60)

    # --------------------------------------------------------
    # CHOOSE DIFFERENT LOGO
    # --------------------------------------------------------

    possible_indices = [
        i
        for i in range(
            len(prepared_logos)
        )
        if i != current_index
    ]

    if possible_indices:

        next_index = random.choice(
            possible_indices
        )

    else:

        next_index = current_index

    next_name, next_logo = (
        prepared_logos[next_index]
    )

    # --------------------------------------------------------
    # RANDOM ANIMATION
    # --------------------------------------------------------

    print(
        current_name,
        "→",
        next_name
    )

    random_animation(
        current_logo,
        next_logo
    )

    # --------------------------------------------------------
    # UPDATE CURRENT LOGO
    # --------------------------------------------------------

    current_index = next_index

    current_name = next_name

    current_logo = next_logo