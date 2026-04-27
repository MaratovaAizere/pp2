import pygame, random
from constants import *
from TSIS.tsis3.racer import (Player, Enemy, Coin, PowerUp,
                     OilSpill, Pothole, Barrier, SpeedBump,
                     NitroStrip, SlowStrip, NitroBooster)
from ui import draw_hud

DIFF_MULT = {"easy": 0.7, "normal": 1.0, "hard": 1.5}


def run_game(surface, clock, bg_image, player_images, enemy_image,
             crash_sound, settings, username):
    """Run one game session. Returns {score, distance, coins}."""

    diff     = settings.get("difficulty", "normal")
    mult     = DIFF_MULT[diff]
    sound_on = settings.get("sound", True)

    player = Player(player_images[settings.get("car_color", "blue")])

    # ── Enemy pool ────────────────────────────────────────────────────────────
    enemies_group = pygame.sprite.Group()
    all_sprites   = pygame.sprite.Group()
    all_sprites.add(player)

    current_speed = BASE_SPEED * mult   # bootstrapped before first spawn

    def spawn_enemy():
        e = Enemy(enemy_image, current_speed, player.rect)
        enemies_group.add(e)
        all_sprites.add(e)

    spawn_enemy()

    coin = Coin(current_speed)

    # ── Counters ──────────────────────────────────────────────────────────────
    score      = 0
    coin_count = 0
    distance   = 0
    start_tick = pygame.time.get_ticks()

    # ── Object lists ──────────────────────────────────────────────────────────
    obstacles      = []   # lane hazards
    powerups       = []   # collectible power-ups
    road_events    = []   # NitroStrip | SlowStrip full-road tiles
    nitro_boosters = []   # NitroBooster collectibles

    now = pygame.time.get_ticks()
    next_obstacle      = now + int(3000  / mult)
    next_powerup       = now + int(5000  / mult)
    next_road_event    = now + int(10000 / mult)
    next_nitro_booster = now + int(7000  / mult)

    active_powerup_label = ""
    road_y = 0

    # ── Music ─────────────────────────────────────────────────────────────────
    if sound_on:
        try:
            pygame.mixer.music.load("background.wav")
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    # ── Main loop ─────────────────────────────────────────────────────────────
    running = True
    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit

        # ── Difficulty scaling ─────────────────────────────────────────────
        tier          = coin_count // SPEED_UP_EVERY
        current_speed = (BASE_SPEED + tier * SPEED_INCREMENT) * mult
        coin.speed    = current_speed
        player.set_base_speed(5 + tier)

        for e in enemies_group:
            e.speed = current_speed

        desired = min(MAX_ENEMIES_START + coin_count // ENEMY_ADD_EVERY, 4)
        while len(enemies_group) < desired:
            spawn_enemy()

        # ── Spawn lane obstacles ───────────────────────────────────────────
        if now >= next_obstacle:
            kind = random.choices(
                ["oil", "pothole", "barrier", "bump"],
                weights=[3, 3, 2, 1]
            )[0]
            if kind == "oil":
                obs = OilSpill(current_speed, player.rect)
            elif kind == "pothole":
                obs = Pothole(current_speed, player.rect)
            elif kind == "barrier":
                obs = Barrier(current_speed, player.rect)
            else:
                obs = SpeedBump(current_speed, player.rect)
            obstacles.append(obs)
            next_obstacle = now + int(random.randint(1800, 3500) / mult)

        # ── Spawn power-up (one on screen at a time) ───────────────────────
        if now >= next_powerup and not any(p.active for p in powerups):
            powerups.append(PowerUp(current_speed, player.rect))
            next_powerup = now + int(random.randint(6000, 10000) / mult)

        # ── Spawn road event (NitroStrip or SlowStrip) ────────────────────
        if now >= next_road_event:
            kind = random.choice(["nitro", "slow"])
            if kind == "nitro":
                road_events.append(NitroStrip(current_speed))
            else:
                road_events.append(SlowStrip(current_speed))
            next_road_event = now + int(random.randint(9000, 16000) / mult)

        # ── Spawn nitro booster collectible ────────────────────────────────
        if now >= next_nitro_booster and not any(b.active for b in nitro_boosters):
            nitro_boosters.append(NitroBooster(current_speed, player.rect))
            next_nitro_booster = now + int(random.randint(8000, 14000) / mult)

        # ── Move everything ───────────────────────────────────────────────
        player.move()
        player.update_powerups()
        for e in enemies_group:
            e.move(player.rect)
        coin.move()
        for obs in obstacles:      obs.move()
        for pu  in powerups:       pu.move()
        for re  in road_events:    re.move()
        for nb  in nitro_boosters: nb.move()

        obstacles      = [o for o in obstacles      if o.active]
        powerups       = [p for p in powerups        if p.active]
        road_events    = [r for r in road_events     if r.active]
        nitro_boosters = [b for b in nitro_boosters  if b.active]

        # ── Distance ──────────────────────────────────────────────────────
        distance = (now - start_tick) // 100
        road_y   = (road_y + current_speed) % SCREEN_HEIGHT

        # ── Coin collision ────────────────────────────────────────────────
        if player.rect.colliderect(coin.get_rect()):
            coin_count += 1
            score      += coin.value
            coin        = Coin(current_speed)

        # ── Nitro booster collision ───────────────────────────────────────
        for nb in nitro_boosters[:]:
            if nb.active and player.rect.colliderect(nb.get_rect()):
                nb.active = False
                player.activate_nitro()
                active_powerup_label = "Nitro Boost!"
                score += 10

        # ── Power-up collision ────────────────────────────────────────────
        for pu in powerups[:]:
            if pu.active and player.rect.colliderect(pu.get_rect()):
                pu.active = False
                if pu.kind == "nitro":
                    player.activate_nitro()
                    active_powerup_label = "Nitro!"
                elif pu.kind == "shield":
                    player.shield = True
                    active_powerup_label = "Shield"
                elif pu.kind == "repair":
                    obstacles.clear()
                    active_powerup_label = "Repair!"
                score += 20

        # Clear stale labels
        if active_powerup_label in ("Nitro!", "Nitro Boost!", "Nitro Strip!") and not player.nitro:
            active_powerup_label = ""
        if active_powerup_label == "Repair!" and not player.slowed:
            active_powerup_label = ""
        if active_powerup_label == "Shield" and not player.shield:
            active_powerup_label = ""
        if active_powerup_label == "Slowed!" and not player.slowed:
            active_powerup_label = ""

        # ── Road event collision (NitroStrip / SlowStrip) ─────────────────
        for re in road_events[:]:
            if re.active and player.rect.colliderect(re.get_rect()):
                if isinstance(re, NitroStrip):
                    player.activate_nitro()
                    active_powerup_label = "Nitro Strip!"
                elif isinstance(re, SlowStrip):
                    player.activate_slow()
                    active_powerup_label = "Slowed!"
                re.active = False

        # ── Lane obstacle collision ───────────────────────────────────────
        for obs in obstacles[:]:
            if player.rect.colliderect(obs.get_rect()):
                if obs.is_lethal():
                    if player.shield:
                        player.shield = False
                        active_powerup_label = ""
                        obs.active = False
                    else:
                        running = False
                        break
                else:
                    obs.apply_effect(player)
                    obs.active = False
                    if active_powerup_label == "":
                        active_powerup_label = "Slowed!"

        # ── Enemy collision ───────────────────────────────────────────────
        if pygame.sprite.spritecollideany(player, enemies_group):
            if player.shield:
                player.shield = False
                active_powerup_label = ""
                for e in list(enemies_group):
                    if player.rect.colliderect(e.rect):
                        e.safe_reset(player.rect)
            else:
                running = False

        # ── Render ────────────────────────────────────────────────────────
        surface.blit(bg_image, (0, road_y - SCREEN_HEIGHT))
        surface.blit(bg_image, (0, road_y))

        for re  in road_events:    re.draw(surface)
        for obs in obstacles:      obs.draw(surface)
        for nb  in nitro_boosters: nb.draw(surface)
        for pu  in powerups:       pu.draw(surface)
        coin.draw(surface)

        for entity in all_sprites:
            surface.blit(entity.image, entity.rect)

        nitro_ms_left = max(0, player.nitro_end - now) if player.nitro else 0
        draw_hud(surface, score, coin_count, distance,
                 player.shield, player.nitro, nitro_ms_left, active_powerup_label)

        pygame.display.flip()
        clock.tick(FPS)

    # ── Crash ─────────────────────────────────────────────────────────────
    pygame.mixer.music.stop()
    if sound_on:
        try:
            crash_sound.play()
            pygame.time.wait(600)
        except Exception:
            pass

    return {"score": score, "distance": distance, "coins": coin_count}