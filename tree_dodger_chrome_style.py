import tkinter as tk
import random

# TREE DODGER - Chrome Dino style, but YOU control the trees!
# SPACE: make the approaching tree jump over the dino
# R: restart after Game Over

WIDTH = 900
HEIGHT = 380
GROUND_Y = 290

root = tk.Tk()
root.title("Tree Dodger - You Control the Trees!")
root.resizable(False, False)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                   bg="#f5f5f5", highlightthickness=0)
canvas.pack()

# Game settings
dino_x = 145
dino_y = GROUND_Y
tree_x = WIDTH + 100
tree_jump_height = 0
tree_jump_velocity = 0
tree_is_jumping = False
tree_was_counted = False
score = 0
speed = 7
frame = 0
game_over = False
space_down = False


def draw_dino():
    """Draw the dino in a fixed position, with animated running legs."""
    # Body
    canvas.create_rectangle(dino_x - 28, dino_y - 48,
                            dino_x + 22, dino_y - 12,
                            fill="#444444", outline="#222222", width=2)
    # Neck and head
    canvas.create_rectangle(dino_x + 7, dino_y - 76,
                            dino_x + 35, dino_y - 39,
                            fill="#444444", outline="#222222", width=2)
    canvas.create_rectangle(dino_x + 25, dino_y - 66,
                            dino_x + 47, dino_y - 55,
                            fill="#444444", outline="#222222", width=2)
    # Eye
    canvas.create_oval(dino_x + 25, dino_y - 70,
                       dino_x + 31, dino_y - 64,
                       fill="white", outline="")
    canvas.create_oval(dino_x + 28, dino_y - 69,
                       dino_x + 30, dino_y - 66,
                       fill="black", outline="")
    # Tail
    canvas.create_polygon(dino_x - 27, dino_y - 39,
                          dino_x - 49, dino_y - 29,
                          dino_x - 27, dino_y - 23,
                          fill="#444444", outline="#222222")
    # Running legs
    if frame % 2 == 0:
        canvas.create_line(dino_x - 12, dino_y - 13,
                           dino_x - 19, dino_y,
                           fill="#222222", width=6)
        canvas.create_line(dino_x + 12, dino_y - 13,
                           dino_x + 19, dino_y,
                           fill="#222222", width=6)
    else:
        canvas.create_line(dino_x - 12, dino_y - 13,
                           dino_x - 4, dino_y,
                           fill="#222222", width=6)
        canvas.create_line(dino_x + 12, dino_y - 13,
                           dino_x + 5, dino_y,
                           fill="#222222", width=6)


def draw_tree():
    """Draw the tree. Its position moves left; SPACE makes it jump."""
    # The tree's ground position is fixed vertically unless it jumps.
    ground_base = GROUND_Y - tree_jump_height

    # Trunk
    canvas.create_rectangle(tree_x - 9, ground_base - 48,
                            tree_x + 9, ground_base,
                            fill="#80502b", outline="#56351d", width=2)
    # Leaves
    canvas.create_oval(tree_x - 31, ground_base - 103,
                       tree_x + 31, ground_base - 43,
                       fill="#27883b", outline="#155b27", width=2)
    canvas.create_oval(tree_x - 23, ground_base - 119,
                       tree_x + 23, ground_base - 66,
                       fill="#35a34a", outline="#155b27", width=2)


def draw_scene():
    canvas.delete("all")

    # Sky and ground
    canvas.create_rectangle(0, 0, WIDTH, GROUND_Y,
                            fill="#f5f5f5", outline="")
    canvas.create_line(0, GROUND_Y, WIDTH, GROUND_Y,
                       fill="#555555", width=3)

    # Moving ground marks create the original side-scrolling feeling
    for x in range(-80, WIDTH + 80, 80):
        mark_x = (x - frame * speed) % (WIDTH + 80)
        canvas.create_line(mark_x, GROUND_Y + 12,
                           mark_x + 25, GROUND_Y + 12,
                           fill="#aaaaaa", width=2)

    canvas.create_text(WIDTH - 25, 25, text=f"SCORE: {score}",
                       anchor="e", font=("Arial", 17, "bold"),
                       fill="#333333")

    draw_dino()
    draw_tree()

    if game_over:
        canvas.create_rectangle(220, 105, 680, 225,
                                fill="white", outline="#333333", width=3)
        canvas.create_text(WIDTH // 2, 145, text="GAME OVER",
                           font=("Arial", 30, "bold"), fill="#c62828")
        canvas.create_text(WIDTH // 2, 190,
                           text=f"Score: {score}     Press R to restart",
                           font=("Arial", 15), fill="#333333")
    else:
        canvas.create_text(
            WIDTH // 2, 350,
            text="SPACE TO JUMP",
            font=("Arial", 12), fill="#444444"
        )


def make_tree_jump(event=None):
    """SPACE TO JUMP."""
    global tree_jump_velocity, tree_is_jumping, space_down

    if game_over or space_down:
        return

    space_down = True

    # Only let the player trigger the tree when it is approaching.
    # This prevents jumping too early while the tree is far away.
    if not tree_is_jumping and dino_x + 35 < tree_x < dino_x + 260:
        tree_jump_velocity = 15
        tree_is_jumping = True


def release_space(event=None):
    global space_down
    space_down = False


def reset_game(event=None):
    global dino_x, tree_x, tree_jump_height, tree_jump_velocity
    global tree_is_jumping, tree_was_counted
    global score, speed, frame, game_over, space_down

    if game_over:
        dino_x = 145
        tree_x = WIDTH + 100
        tree_jump_height = 0
        tree_jump_velocity = 0
        tree_is_jumping = False
        tree_was_counted = False
        score = 0
        speed = 7
        frame = 0
        game_over = False
        space_down = False
        draw_scene()
        update_game()


def update_game():
    global tree_x, tree_jump_height, tree_jump_velocity
    global tree_is_jumping, tree_was_counted
    global score, speed, frame, game_over

    if game_over:
        return

    frame += 1

    # Tree moves toward the stationary dino, like obstacles in Chrome Dino.
    tree_x -= speed

    # Apply the tree's jump and gravity.
    if tree_is_jumping:
        tree_jump_height += tree_jump_velocity
        tree_jump_velocity -= 0.75

        if tree_jump_height <= 0:
            tree_jump_height = 0
            tree_jump_velocity = 0
            tree_is_jumping = False

    # Collision: the tree must be high enough when it reaches the dino.
    # The tree's trunk/leaves are treated as one obstacle.
    horizontal_overlap = (tree_x - 31 < dino_x + 30 and
                          tree_x + 31 > dino_x - 25)
    tree_clears_dino = tree_jump_height > 78

    if horizontal_overlap and not tree_clears_dino:
        game_over = True

    # Once the tree has passed the dino, give a point and create another.
    if tree_x < dino_x - 55 and not tree_was_counted:
        score += 1
        tree_was_counted = True
        if score % 5 == 0:
            speed += 0.7

    if tree_x < -70:
        tree_x = WIDTH + random.randint(180, 320)
        tree_jump_height = 0
        tree_jump_velocity = 0
        tree_is_jumping = False
        tree_was_counted = False

    draw_scene()

    if not game_over:
        root.after(25, update_game)


root.bind("<KeyPress-space>", make_tree_jump)
root.bind("<KeyRelease-space>", release_space)
root.bind("<KeyPress-r>", reset_game)
root.bind("<KeyPress-R>", reset_game)

draw_scene()
update_game()
root.mainloop()
