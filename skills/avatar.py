import pygame
import threading
import math
import time


class ViviAvatar:
    def __init__(self):
        self.running = False
        self.speaking = False
        self.listening = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("VIVI")
        clock = pygame.time.Clock()

        # Colors
        BG = (15, 15, 25)
        PINK = (255, 105, 180)
        PURPLE = (147, 0, 211)
        WHITE = (255, 255, 255)
        GLOW = (255, 20, 147)

        t = 0
        mouth_open = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.fill(BG)
            t += 0.05

            # Glow effect
            glow_size = int(120 + math.sin(t) * 10)
            glow_surf = pygame.Surface((400, 400), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 20, 147, 30), (200, 180), glow_size)
            screen.blit(glow_surf, (0, 0))

            # Head
            pygame.draw.circle(screen, PINK, (200, 180), 100)

            # Eyes
            eye_y = 160 + int(math.sin(t) * 2)

            # Left eye
            pygame.draw.ellipse(screen, WHITE, (155, eye_y - 15, 30, 30))
            pygame.draw.circle(screen, (50, 0, 80), (170, eye_y), 10)
            pygame.draw.circle(screen, WHITE, (173, eye_y - 3), 3)

            # Right eye
            pygame.draw.ellipse(screen, WHITE, (215, eye_y - 15, 30, 30))
            pygame.draw.circle(screen, (50, 0, 80), (230, eye_y), 10)
            pygame.draw.circle(screen, WHITE, (233, eye_y - 3), 3)

            # Blinking
            if int(t * 10) % 50 == 0:
                pygame.draw.ellipse(screen, PINK, (155, eye_y - 15, 30, 30))
                pygame.draw.ellipse(screen, PINK, (215, eye_y - 15, 30, 30))

            # Nose
            pygame.draw.circle(screen, (255, 150, 200), (200, 185), 4)

            # Mouth
            if self.speaking:
                mouth_open = min(mouth_open + 2, 15)
            else:
                mouth_open = max(mouth_open - 2, 0)

            if mouth_open > 2:
                pygame.draw.ellipse(screen, (180, 0, 60),
                                    (175, 200, 50, mouth_open + 5))
                pygame.draw.ellipse(screen, WHITE,
                                    (178, 202, 44, max(mouth_open - 2, 2)))
            else:
                # Smile
                pygame.draw.arc(screen, (180, 0, 60),
                                (175, 195, 50, 20), math.pi, 2 * math.pi, 3)

            # Cheeks
            cheek_surf = pygame.Surface((400, 400), pygame.SRCALPHA)
            pygame.draw.circle(cheek_surf, (255, 150, 180, 80), (155, 195), 20)
            pygame.draw.circle(cheek_surf, (255, 150, 180, 80), (245, 195), 20)
            screen.blit(cheek_surf, (0, 0))

            # Hair
            pygame.draw.ellipse(screen, PURPLE, (100, 80, 200, 120))
            pygame.draw.ellipse(screen, PINK, (115, 95, 170, 100))

            # Hair strands
            pygame.draw.ellipse(screen, PURPLE, (90, 100, 40, 120))
            pygame.draw.ellipse(screen, PURPLE, (270, 100, 40, 120))

            # Ears
            pygame.draw.circle(screen, PINK, (100, 180), 20)
            pygame.draw.circle(screen, PINK, (300, 180), 20)

            # Status text
            if self.speaking:
                status = "Speaking..."
                color = PINK
            elif self.listening:
                status = "Listening..."
                color = (100, 200, 255)
            else:
                status = "Hey Vivi!"
                color = (150, 150, 150)

            font = pygame.font.SysFont("Arial", 20, bold=True)
            text = font.render(status, True, color)
            screen.blit(text, (200 - text.get_width() // 2, 320))

            # Floating particles
            for i in range(5):
                px = int(200 + math.sin(t + i * 1.2) * 150)
                py = int(200 + math.cos(t * 0.7 + i) * 100)
                alpha = int(abs(math.sin(t + i)) * 150)
                particle_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
                pygame.draw.circle(particle_surf, (255, 105, 180, alpha), (5, 5), 3)
                screen.blit(particle_surf, (px, py))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def set_speaking(self, val):
        self.speaking = val

    def set_listening(self, val):
        self.listening = val

    def stop(self):
        self.running = False


# Global avatar instance
avatar = ViviAvatar()


def start_avatar():
    avatar.start()


def set_speaking(val):
    avatar.set_speaking(val)


def set_listening(val):
    avatar.set_listening(val)

def set_listening(val):
    avatar.set_listening(val)