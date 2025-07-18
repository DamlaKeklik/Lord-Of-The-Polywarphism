import pygame
import sys
import random
from button import Button
from wariors import Muhafiz, Okcu, Topcu, Atli, Saglikci

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def options():
    selected_matrix_size = None  # Seçilen matris boyutunu saklamak için değişken
    selected_num_players = None  # Seçilen oyuncu sayısını saklamak için değişken
    human_players = None  # İnsan oyuncuların varlığını saklamak için değişken

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("OPTIONS", True, "black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Draw text for selecting matrix size
        MATRIX_TEXT = get_font(30).render("Select matrix size:", True, "black")
        MATRIX_RECT = MATRIX_TEXT.get_rect(topleft=(50, 200))
        SCREEN.blit(MATRIX_TEXT, MATRIX_RECT)

        # Draw buttons for matrix size selection
        matrix_sizes = ["8x8", "16x16", "24x24", "32x32"]
        matrix_buttons = []
        for i, size in enumerate(matrix_sizes):
            button = Button(image=None, pos=(200 + i * 150, 280), text_input=size, font=get_font(30),
                            base_color="black", hovering_color="green")
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)
            matrix_buttons.append(button)

        # Draw text for selecting number of players
        PLAYER_TEXT = get_font(30).render("Select number of players (1-4):", True, "black")
        PLAYER_RECT = PLAYER_TEXT.get_rect(topleft=(50, 350))
        SCREEN.blit(PLAYER_TEXT, PLAYER_RECT)

        # Draw buttons for number of players selection
        player_buttons = []
        for i in range(1, 5):
            button = Button(image=None, pos=(200 + i * 100, 400), text_input=str(i), font=get_font(30),
                            base_color="black", hovering_color="green")

            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)
            player_buttons.append(button)

        # Draw buttons for selecting human players
        HUMAN_TEXT = get_font(30).render("Human players:", True, "black")
        HUMAN_RECT = HUMAN_TEXT.get_rect(topleft=(50, 470))
        SCREEN.blit(HUMAN_TEXT, HUMAN_RECT)

        human_buttons = []
        for i, option in enumerate(["False", "True"]):
            button = Button(image=None, pos=(200 + i * 200, 520), text_input=option, font=get_font(30),
                            base_color="black", hovering_color="green")
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)
            human_buttons.append(button)

        OPTIONS_BACK = Button(image=None, pos=(640, 600),
                              text_input="BACK", font=get_font(50), base_color="black", hovering_color="green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                for button in matrix_buttons:
                    if button.checkForInput(OPTIONS_MOUSE_POS):
                        # Handle matrix size selection
                        selected_matrix_size = button.display_text
                        print("Selected matrix size:", selected_matrix_size)  # Replace print statement with your logic

                for button in player_buttons:
                    if button.checkForInput(OPTIONS_MOUSE_POS):
                        # Handle number of players selection
                        selected_num_players = int(button.display_text)
                        print("Selected number of players:",
                              selected_num_players)  # Replace print statement with your logic

                for button in human_buttons:
                    if button.checkForInput(OPTIONS_MOUSE_POS):
                        # Handle human players selection
                        human_players = True if button.display_text == "True" else False
                        print("Human players:", human_players)  # Replace print statement with your logic

        pygame.display.update()

        if selected_matrix_size is not None and selected_num_players is not None and human_players is not None:
            play(selected_matrix_size, selected_num_players, human_players)

def play(selected_matrix_size, selected_num_players, human_players=False):
    SCREEN.fill("black")

    # Seçilen matris boyutunda bir matris çiz
    draw_matrix(selected_matrix_size)

    # Oyuncuları yerleştir
    player_resources = place_warriors(selected_matrix_size, selected_num_players)

    # Ekrandaki değişiklikleri güncelle
    pygame.display.update()

    # Oyuncu renkleri
    player_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

    # Her oyuncunun sırası geldiğinde savaşçı seçimini yapmasını sağlayın
    current_player = 1  # Şu anki oyuncuyu takip etmek için bir değişken
    while current_player <= selected_num_players:
        if human_players:
            current_player = select_warrior_human(current_player, selected_matrix_size, player_colors,
                                                  selected_num_players, player_resources)
        else:
            current_player = select_warrior_AI(current_player, selected_matrix_size, player_colors,
                                               selected_num_players, player_resources)
            # Her oyuncu sırası geldiğinde bir savaşçı yerleştirildiğinde yeni bir tur başlat
            if current_player == 1:
                # Burada gerekli ekran temizleme ve diğer işlemleri gerçekleştirebilirsiniz
                player_resources = place_warriors(selected_matrix_size,
                                                  selected_num_players)  # Yeni yerleştirmeleri yap
                pygame.display.update()  # Ekranı güncelle
                # Döngüyü tekrar başlatma yerine, pas geçen oyuncunun sırasını bir sonraki oyuncuya geçirelim
                current_player = (current_player % selected_num_players) + 1

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()


def draw_matrix(matrix_size):
    SCREEN.fill((0, 0, 0))  # Ekranı siyah bir renkle temizle

    # Matris boyutunu ayrıştır
    rows, cols = map(int, matrix_size.split("x"))

    # Ekran boyutları
    screen_width, screen_height = SCREEN.get_size()

    # Matris hücrelerinin boyutunu hesapla
    cell_width = min((screen_width - 10) // cols, (screen_height - 10) // rows)
    cell_height = cell_width

    # Matrisin başlangıç koordinatlarını belirle
    start_x = (screen_width - cols * cell_width) // 2
    start_y = (screen_height - rows * cell_height) // 2

    # Matrisi çiz
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(start_x + col * cell_width, start_y + row * cell_height, cell_width, cell_height)
            pygame.draw.rect(SCREEN, (255, 255, 255), rect, 1)  # Her hücreyi beyaz bir çizgiyle çiz
            pygame.draw.circle(SCREEN, (255, 255, 255), rect.center, 2)  # Her hücrenin merkezine beyaz bir nokta ekle


def place_warriors(matrix_size, num_players):
    # Matris boyutunu ayrıştır
    rows, cols = map(int, matrix_size.split("x"))

    # Matrisin köşe koordinatları
    corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]

    # Matrisin boyutlarına göre hücre boyutunu hesapla
    cell_width = min((1280 - 10) // cols, (720 - 10) // rows)
    cell_height = cell_width

    # Oyuncu renkleri
    player_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

    # Köşelere oyuncuların savaşçılarını yerleştir
    player_resources = [200] * num_players  # Oyuncu kaynaklarını tutmak için bir liste
    for i in range(num_players):
        # Rastgele bir köşe seç
        corner = random.choice(corners)

        # Köşeye oyuncunun muhafızını yerleştir
        print(f"Player {i + 1} places warrior at corner {corner} with color {player_colors[i]}")

        # Köşeyi ekranda göster
        start_x = (1280 - cols * cell_width) // 2
        start_y = (720 - rows * cell_height) // 2
        corner_x, corner_y = corner

        # Savaşçının arkaplan rengini oyuncu rengi olarak ayarla
        pygame.draw.rect(SCREEN, player_colors[i], (start_x + corner_y * cell_width, start_y + corner_x * cell_height, cell_width, cell_height))

        # Muhafiz sınıfından bir savaşçı oluştur
        warrior = Muhafiz()

        # Matrise savaşçıyı yerleştir
        rect = pygame.Rect(start_x + corner_y * cell_width, start_y + corner_x * cell_height, cell_width, cell_height)

        # Seçilen savaşçının baş harfini göster
        font = pygame.font.Font(None, 30)
        text = font.render(warrior.adi[0], True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        SCREEN.blit(text, text_rect)

        # Yerleştirilen köşeyi listeden çıkar
        corners.remove(corner)

        # Köşedeki muhafızın komşularını boyayın
        paint_neighbors(i + 1, corner_x, corner_y, matrix_size, player_colors)

    pygame.display.update()  # Ekranı güncelle
    return player_resources

def select_warrior_human(player, matrix_size, player_colors, selected_num_players, player_resources):
    print(f"Oyuncu {player}, savaşçı seçiyor.")
    warrior_types = ["Muhafiz", "Okcu", "Topcu", "Atli", "Saglikci", "Pas"]  # Pas seçeneği eklendi

    # Matrisin boyutlarına göre hücre boyutunu hesapla
    rows, cols = map(int, matrix_size.split("x"))
    screen_width, screen_height = SCREEN.get_size()
    cell_width = min((screen_width - 10) // cols, (screen_height - 10) // rows)
    cell_height = cell_width

    # Başlangıç koordinatlarını belirle
    start_x = (screen_width - cols * cell_width) // 2
    start_y = (screen_height - rows * cell_height) // 2

    # Matrise yerleştirilen savaşçıları izlemek için bir matris oluştur
    matrix = [[None for _ in range(cols)] for _ in range(rows)]

    # Her oyuncu sırası geldiğinde savaşçı seçimini sağlamak için döngü
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Savaşçının seçilen hücreye uygun olup olmadığını kontrol et
                col = (mouse_x - start_x) // cell_width
                row = (mouse_y - start_y) // cell_height
                if 0 <= row < rows and 0 <= col < cols:
                    # Hücre dolu ise devam et
                    if matrix[row][col] is not None:
                        old_warrior = matrix[row][col]
                        # Eğer hücre doluysa, eski savaşçının üzerine yeni savaşçıyı yerleştir
                        print(f"Yeni savaşçı eski savaşçının üzerine yerleştiriliyor: {old_warrior}")
                        old_warrior_class = eval(old_warrior)()
                        old_warrior_cost = old_warrior_class.kaynak
                        print(f"Eski savaşçının maliyeti: {old_warrior_cost}")
                        refund_amount = int(old_warrior_cost * 0.8)  # %80'i geri ödenecek
                        player_resources[player -1] += refund_amount
                        print(f"%80 geri ödenen miktar: {refund_amount}")
                        print(f"Oyuncunun yeni kaynağı: {player_resources[player-1]}")
                    # Seçilen savaşçıyı döndür
                    print(f"Koordinatlar: {row} {col}")
                    print("1. Muhafiz (10), 2. Okçu (20), 3. Topçu (50), 4. Atli (30), 5. Saglikci (10), 6. Pas")
                    choice = int(input("Seçiminiz (1-6): "))
                    if 1 <= choice <= 6:  # Pas seçeneğini de kontrol et
                        if choice == 6:  # Eğer pas seçildiyse
                            print("Oyuncu elini pas geçti.")
                            # Oyuncu elini pas geçtiğinde bir sonraki oyuncuya sıra geçer
                            player = (player % selected_num_players) + 1
                            print(f"Şimdi sıra Oyuncu {player}'da.")
                            return player
                        else:
                            selected_warrior = warrior_types[choice - 1]
                            print(f"Oyuncu {player}, {selected_warrior} savaşçısını yerleştirildi.")

                            # Savaşçıyı matrise yerleştir
                            rect = pygame.Rect(start_x + col * cell_width, start_y + row * cell_height, cell_width,
                                               cell_height)
                            pygame.draw.rect(SCREEN, player_colors[player - 1], rect)  # Oyuncunun rengiyle arkaplanı doldur
                            pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1)  # Hücreyi çiz
                            font = pygame.font.Font(None, 30)
                            text = font.render(selected_warrior[0], True, (0, 0, 0))
                            text_rect = text.get_rect(center=rect.center)
                            SCREEN.blit(text, text_rect)
                            pygame.display.update()

                            # Seçilen hücreyi işaretle
                            matrix[row][col] = selected_warrior

                            # Seçim yapıldığını işaretle
                            has_selected = True

                            # Seçim yapıldıktan sonra kaynakları artır
                            if has_selected:
                                # Kaynakları güncelle
                                player_resources[player - 1] -= getattr(eval(selected_warrior)(), "kaynak")
                                print(f"Oyuncu {player} kaynağı güncellendi. Yeni kaynak: {player_resources[player - 1]}")

                                # Komşu hücreleri boyayın
                                paint_neighbors(player, row, col, matrix_size, player_colors)

                                # Tüm matris dolana kadar devam et
                                if all(all(cell is not None for cell in row) for row in matrix):
                                    return player

                                # Bir sonraki oyuncunun sırasını belirle
                                player = player % selected_num_players + 1

                                # Her iki oyuncu da seçim yaptıktan sonra kaynakları artır
                                if player == 1:
                                    for i in range(selected_num_players):
                                        player_resources[i] += 10
                                        print(f"Oyuncu {i + 1} kaynaklarına 10 kaynak ekledi. Yeni kaynak: {player_resources[i]}")

                                # Sıradaki oyuncunun seçim yapmasını bekleyin
                                print(f"Oyuncu {player}, savaşçı seçiyor.")

                    else:
                        print("Geçersiz seçim. Lütfen tekrar deneyin.")



def select_warrior_AI(current_player, matrix_size, player_colors, num_players, player_resources):
    print(f"Oyuncu {current_player}, savaşçı seçiyor.")  # Düzeltme: player yerine current_player kullan
    warrior_types = ["Muhafiz", "Okcu", "Topcu", "Atli", "Saglikci"]  # Kullanılabilir savaşçı tipleri

    # Matrisin boyutlarına göre hücre boyutunu hesapla
    rows, cols = map(int, matrix_size.split("x"))
    screen_width, screen_height = SCREEN.get_size()
    cell_width = min((screen_width - 10) // cols, (screen_height - 10) // rows)
    cell_height = cell_width

    # Başlangıç koordinatlarını belirle
    start_x = (screen_width - cols * cell_width) // 2
    start_y = (screen_height - rows * cell_height) // 2

    # Matrise yerleştirilen savaşçıları izlemek için bir matris oluştur
    matrix = [[None for _ in range(cols)] for _ in range(rows)]

    # Matris tamamen dolana kadar savaşçı seçimini sağlamak için döngü
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Savaşçının seçilen hücreye uygun olup olmadığını kontrol et
                col = (mouse_x - start_x) // cell_width
                row = (mouse_y - start_y) // cell_height
                if 0 <= row < rows and 0 <= col < cols:
                    # Hücre dolu ise devam et
                    if matrix[row][col] is not None:
                        continue
                    # Seçilen savaşçıyı döndür
                    print(f"Koordinatlar: {row} {col}")

                    if current_player == 1:  # İlk oyuncu insan kontrolünde
                        print("1. Muhafiz (10), 2. Okçu (20), 3. Topçu (50), 4. Atli (30), 5. Saglikci (10)")
                        choice = int(input("Seçiminiz (1-5): "))
                    else:  # Diğer oyuncular için AI kontrolü
                        choice = random.randint(1, 5)
                        print(f"Oyuncu {current_player} seçtiği savaşçı: {warrior_types[choice - 1]}")

                    if 1 <= choice <= 5:
                        selected_warrior = warrior_types[choice - 1]
                        print(f"Oyuncu {current_player}, {selected_warrior} savaşçısını yerleştirildi.")

                        # Savaşçıyı matrise yerleştir
                        rect = pygame.Rect(start_x + col * cell_width, start_y + row * cell_height, cell_width,
                                           cell_height)
                        pygame.draw.rect(SCREEN, player_colors[current_player - 1], rect)  # Oyuncunun rengiyle arkaplanı doldur
                        pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1)  # Hücreyi çiz
                        font = pygame.font.Font(None, 30)
                        text = font.render(selected_warrior[0], True, (0, 0, 0))
                        text_rect = text.get_rect(center=rect.center)
                        SCREEN.blit(text, text_rect)
                        pygame.display.update()

                        # Seçilen hücreyi işaretle
                        matrix[row][col] = selected_warrior

                        # Kaynakları güncelle
                        player_resources[current_player - 1] -= getattr(eval(selected_warrior)(), "kaynak")
                        print(
                            f"Oyuncu {current_player} kaynağı güncellendi. Yeni kaynak: {player_resources[current_player - 1]}")

                        # Komşu hücreleri boyayın
                        paint_neighbors(current_player, row, col, matrix_size, player_colors)

                        # Tüm matris dolana kadar devam et
                        if all(all(cell is not None for cell in row) for row in matrix):
                            return player_resources

                        # Bir sonraki oyuncunun sırasını belirle
                        current_player = current_player % num_players + 1
                        next_player = current_player if current_player != 1 else num_players

                        # Kullanılan kaynakları ve kalan kaynakları göster
                        used_resources = getattr(eval(selected_warrior)(), 'kaynak')

                        print(f"Kullanılan kaynak: {used_resources}")



                    else:
                        print("Geçersiz seçim. Lütfen tekrar deneyin.")



def paint_neighbors(player, row, col, matrix_size, player_colors):
    # Matrisin boyutlarını al
    rows, cols = map(int, matrix_size.split("x"))

    # Komşuları işaretlemek için bir liste oluştur
    neighbors = [
        (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
        (row, col - 1),                     (row, col + 1),
        (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
    ]

    # Ekranda çizilecek hücre boyutunu hesapla
    screen_width, screen_height = SCREEN.get_size()
    cell_width = min((screen_width - 10) // cols, (screen_height - 10) // rows)
    cell_height = cell_width

    # Başlangıç koordinatlarını belirle
    start_x = (screen_width - cols * cell_width) // 2
    start_y = (screen_height - rows * cell_height) // 2

    # Oyuncunun rengini al
    player_color = player_colors[player - 1]

    # Oyuncunun rengine alfa (saydamlık) ekleyerek yeni bir renk oluştur
    transparent_color = player_color[:3] + (100,)  # Rengin alpha (saydamlık) değerini ayarla

    # Komşu hücrelerin içini yeni saydam renkle boyayın
    for neighbor_row, neighbor_col in neighbors:
        # Komşu hücrelerin geçerli olup olmadığını kontrol et
        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
            # Hücrenin içini oyuncunun saydam rengine boyayın
            rect = pygame.Rect(start_x + neighbor_col * cell_width, start_y + neighbor_row * cell_height, cell_width,
                               cell_height)
            # Yeni bir yüzey oluşturun ve alfa değerini ayarlayarak şeffaflık ekleyin
            transparent_surface = pygame.Surface((cell_width, cell_height), pygame.SRCALPHA)
            transparent_surface.fill(transparent_color)
            SCREEN.blit(transparent_surface, (start_x + neighbor_col * cell_width, start_y + neighbor_row * cell_height))
            pygame.draw.rect(SCREEN, (0, 0, 0), rect, 1)  # Hücreyi çiz
    pygame.display.update()


main_menu()
