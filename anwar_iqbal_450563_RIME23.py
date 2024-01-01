import tkinter as tk
import random
import time

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x420")  # Increased height to accommodate scores and timer
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, bg="black", width=400, height=400)
        self.canvas.pack()

        self.player_snake = [(100, 100), (90, 100), (80, 100)]
        self.ai_snake = [(300, 300), (310, 300), (320, 300)]
        self.player_direction = "Right"
        self.ai_direction = "Left"
        self.player_score = 0
        self.ai_score = 0

        self.food = None
        self.obstacles = self.create_obstacles()

        self.master.bind("<KeyPress>", self.handle_keypress)

        self.game_over_flag = False
        self.restart_flag = False
        self.time_limit = 60
        self.start_time = time.time()
        self.update()

    def create_food(self):
        if not self.food:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            self.food = self.canvas.create_oval(x, y, x + 20, y + 20, fill="yellow")

    def create_obstacles(self):
        obstacles = []
        for _ in range(5):
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            obstacle = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red")
            obstacles.append(obstacle)
        return obstacles

    def move_snake(self, snake, direction):
        if self.game_over_flag:
            return

        head = snake[0]
        if direction == "Right":
            new_head = (head[0] + 20, head[1])
        elif direction == "Left":
            new_head = (head[0] - 20, head[1])
        elif direction == "Up":
            new_head = (head[0], head[1] - 20)
        elif direction == "Down":
            new_head = (head[0], head[1] + 20)

        if not self.check_collision(new_head):
            snake.insert(0, new_head)
            snake.pop()
        else:
            self.game_over()

    def move_ai_snake(self):
        if self.game_over_flag:
            return

        head = self.ai_snake[0]

        if self.food:
            food_coords = self.canvas.coords(self.food)
            if head[0] < food_coords[0]:
                self.ai_direction = "Right"
            elif head[0] > food_coords[0]:
                self.ai_direction = "Left"
            elif head[1] < food_coords[1]:
                self.ai_direction = "Down"
            elif head[1] > food_coords[1]:
                self.ai_direction = "Up"

        new_head = None

        while True:
            if self.ai_direction == "Right":
                new_head = (head[0] + 20, head[1])
            elif self.ai_direction == "Left":
                new_head = (head[0] - 20, head[1])
            elif self.ai_direction == "Up":
                new_head = (head[0], head[1] - 20)
            elif self.ai_direction == "Down":
                new_head = (head[0], head[1] + 20)

            if not self.check_collision(new_head, ai=True):
                break
            else:
                self.ai_direction = random.choice(["Right", "Left", "Up", "Down"])

        self.ai_snake.insert(0, new_head)
        self.ai_snake.pop()

    def check_collision(self, position, ai=False):
        if position[0] < 0 or position[0] >= 400 or position[1] < 0 or position[1] >= 400:
            return True

        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            if position[0] == obstacle_coords[0] and position[1] == obstacle_coords[1]:
                return True

        if not ai and position in self.ai_snake:
            return True
        elif ai and position in self.player_snake:
            return True

        return False

    def update(self):
        self.move_snake(self.player_snake, self.player_direction)
        self.move_ai_snake()

        head = self.player_snake[0]
        head_ai = self.ai_snake[0]

        self.canvas.delete("player_snake")
        for segment in self.player_snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="blue", tags="player_snake")

        self.canvas.delete("ai_snake")
        for segment in self.ai_snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="red", tags="ai_snake")

        self.create_food()

        if self.food:
            food_coords = self.canvas.coords(self.food)
            if head[0] == food_coords[0] and head[1] == food_coords[1]:
                self.player_snake.append((0, 0))
                self.canvas.delete(self.food)
                self.food = None
                self.player_score += 1

            if head_ai[0] == food_coords[0] and head_ai[1] == food_coords[1]:
                self.ai_snake.append((0, 0))
                self.canvas.delete(self.food)
                self.food = None
                self.ai_score += 1

        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, self.time_limit - elapsed_time)
        if not self.game_over_flag and remaining_time > 0:
            if self.player_score >= 10 or self.ai_score >= 10:
                self.game_over()
            else:
                self.master.after(200, self.update)
        else:
            self.game_over()

        self.show_score()

    def handle_keypress(self, event):
        if self.restart_flag and event.keysym == "Return":
            self.restart_game()
        elif not self.restart_flag and not self.game_over_flag:
            if event.keysym == "Right" and not self.player_direction == "Left":
                self.player_direction = "Right"
            elif event.keysym == "Left" and not self.player_direction == "Right":
                self.player_direction = "Left"
            elif event.keysym == "Up" and not self.player_direction == "Down":
                self.player_direction = "Up"
            elif event.keysym == "Down" and not self.player_direction == "Up":
                self.player_direction = "Down"

    def restart_game(self):
        self.player_snake = [(100, 100), (90, 100), (80, 100)]
        self.ai_snake = [(300, 300), (310, 300), (320, 300)]
        self.player_direction = "Right"
        self.ai_direction = "Left"
        self.player_score = 0
        self.ai_score = 0

        # Delete existing food and obstacles
        if self.food:
            self.canvas.delete(self.food)
            self.food = None
        for obstacle in self.obstacles:
            self.canvas.delete(obstacle)
        self.obstacles = self.create_obstacles()

        self.game_over_flag = False
        self.restart_flag = False
        self.start_time = time.time()

        self.canvas.delete("game_over")

        self.master.bind("<KeyPress>", self.handle_keypress)
        self.update()

    def show_score(self):
        self.canvas.delete("score_text")
        self.canvas.delete("time_text")

        score_color = "white" if not self.game_over_flag else "white"
        time_color = "white" if not self.game_over_flag else "white"

        score_text = f"Your Score: {self.player_score}, AI Score: {self.ai_score}"
        self.canvas.create_text(20, 10, text=score_text, fill=score_color, font=("Helvetica", 12), anchor="w", tags="score_text")

        time_text = f"Time Left: {max(0, self.time_limit - int(time.time() - self.start_time))}s"
        self.canvas.create_text(200, 420, text=time_text, fill=time_color, font=("Helvetica", 12), anchor="w", tags="time_text")

    def game_over(self):
        if not self.game_over_flag:
            winner_text = ""
            if self.player_score > self.ai_score:
                winner_text = "Congratulations! You Win!"
            elif self.player_score < self.ai_score:
                winner_text = "Sorry! AI Wins!"
            else:
                winner_text = "It's a Tie!"

            self.canvas.create_rectangle(0, 0, 400, 400, fill="black", tags="game_over")
            self.canvas.create_text(200, 200, text="Game Over! Press Enter to play again", fill="red", font=("Helvetica", 16), tags="game_over")
            self.canvas.create_text(200, 220, text=winner_text, fill="red", font=("Helvetica", 16), tags="game_over")

            self.game_over_flag = True
            self.restart_flag = True

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()


















