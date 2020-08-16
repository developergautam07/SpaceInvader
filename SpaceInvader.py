import pygame as pg 
import math
import random
import sys

#initialize pygame
pg.mixer.pre_init(44100, 16, 2, 4096)
pg.init() 
clock = pg.time.Clock() 

h = 600 #height
w = 800 #width

# Create the screen
screen = pg.display.set_mode((w, h))

# Background
bg = pg.image.load("data\\spacebg.png").convert_alpha()
pg.mixer.music.load("data\\sibg.wav")
pg.mixer.music.play(-1)


# Title & icon
pg.display.set_caption("Space Invader")
img = pg.image.load("data\\ufo.png").convert_alpha()
pg.display.set_icon(img)

# Player
player_img = pg.image.load("data\\player.png").convert_alpha()
player_x = (w / 2) - 64
player_y = h - 100
player_vel = 1

# Obsticle
ob_img = pg.image.load("data\\obsticle.png").convert_alpha()
def o_x(): 
	return random.randint(64, (w - 65))
ob_x = o_x() 
ob_y = 0
ob_vel = 1
ob_active = False


# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_vel = []
enemy_count = 7
enemy_rip = pg.mixer.Sound("data\\explode.wav")

for i in range(enemy_count):
	enemy_img.append(pg.image.load("data\\enemy.png").convert_alpha())
	enemy_x.append(random.randint(64, (w - 65)))
	enemy_y.append(random.randint(64, (h / 4))) 
	enemy_vel.append(1)

# Bullet
bullet_img = pg.image.load("data\\bullet.png").convert_alpha()
bullet_y = h - 100
bullet_vel = 2
bullet_fire = False # Bullet fired or not
bullet_x = player_x
bullet_sfx = pg.mixer.Sound("data\\laser.wav")

# Score
score_val = 0
font = pg.font.Font('data\\FreeSansBold.ttf', 32)
text_x = 10
text_y = 10

def game_over():
	'''Function to display game over text'''
	global score_val
	gov = True
	while gov:	
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
		screen.fill((100, 100, 100))
		pg.mixer.music.stop()
		gov_font = pg.font.Font('data\\FreeSansBold.ttf', 64)
		gov_text = gov_font.render("GAME OVER !!!", True, (255, 0, 0))
		sr_text = gov_font.render(f"Score: {score_val}", True, (0, 0, 255))
		con_text = font.render("Press c to continue", True, (0, 255, 0))
		screen.blit(gov_text, ((w//2) - 200, (h//2) - 100))
		screen.blit(sr_text, ((w//2) - 110, (h//2)))
		screen.blit(con_text, ((w//2) - 120, (h//2) + 100))
		keys = pg.key.get_pressed()
		if keys[pg.K_c]:
			score_val = 0
			pg.mixer.music.play(-1)
			gov = False
		pg.display.update()

def player(x, y):
	'''function to create player'''
	screen.blit(player_img, (int(x), int(y)))

def enemy(x, y, i):
	'''function to create enemy'''
	screen.blit(enemy_img[i], (int(x), int(y)))

def bullet(x, y):
	'''function to create bullet'''
	global bullet_fire
	bullet_fire = True
	screen.blit(bullet_img, (int(x) + 24, int(y) + 10))

def obsticle(x, y):
	global ob_active
	ob_active = True
	screen.blit(ob_img, (x, y))

def detect_collision(x1, x2, y1, y2):
	'''function to check collision'''
	dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) # Distance formula
	if dist <= 32:
		return True
	else:
		return False

def show_score(x, y):
	'''function to display score'''
	score = font.render(f"Score: {score_val}", True, (255, 255, 255))
	screen.blit(score, (x, y))

# Game Loop
gov = False
running = True
while running:
	pg.time.delay(1)
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False


	screen.blit(bg, (0, 0))
	player(player_x, player_y)
	show_score(text_x, text_y)

	# obsticle
	if (score_val >= 10 and score_val < 20) and not ob_active:
		obsticle(ob_x, ob_y)
		if (w - 65) < ob_x <= 64:
				ob_x += 10
	if score_val > 25 and not ob_active:
		obsticle(ob_x, ob_y)
		if (w - 65) < ob_x <= 64:
				ob_x += 10

	if ob_active:
		obsticle(ob_x, ob_y)
		ob_y += ob_vel
		if ob_y >= h:
			ob_y = -3
			ob_active = False
			if (w - 65) < ob_x <= 64:
				ob_x += 10

	ob_dist = detect_collision(player_x, ob_x, player_y, ob_y)
	if ob_dist:
		ob_y = 2000
		enemy_rip.play()
		game_over()

	if not gov:
		# player movement
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT] and player_x > player_vel:
			player_x -= player_vel
		if keys[pg.K_RIGHT] and player_x < (w - 64):
			player_x += player_vel

		# bullet fire
		if keys[pg.K_SPACE] and not bullet_fire:
			bullet_sfx.play()
			bullet_x = player_x
			bullet(bullet_x, bullet_y)
		if bullet_fire:
			bullet(bullet_x, bullet_y)
			bullet_y -= bullet_vel
		if bullet_y <= 0:
			bullet_y = h - 100
			bullet_fire = False 

		# enemy movement
		for i in range(enemy_count):
			enemy(enemy_x[i], enemy_y[i], i)	
			enemy_x[i] += enemy_vel[i]
			if enemy_x[i] <= 0:
				enemy_vel[i] = 0.3
				enemy_y[i] += 30
			if enemy_x[i] >= (w - 64):
				enemy_vel[i] = -0.3
				enemy_y[i] += 30

			# Collision of bullet with enemy
			collision = detect_collision(enemy_x[i], bullet_x, enemy_y[i], bullet_y)
			if collision:
				enemy_rip.play()
				bullet_y = h - 100
				bullet_fire = False
				score_val += 1
				print(score_val)
				enemy_x[i] = random.randint(64, (w - 65))
				enemy_y[i] = random.randint(64, (h / 4))

			# Game Over
			if enemy_y[i] > (h - 160):
				for j in range(enemy_count):
					enemy_y[j] = 1000
				game_over()
				break

		
		pg.display.update()