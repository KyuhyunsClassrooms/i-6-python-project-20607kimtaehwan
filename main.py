# AI 활용 자유 주제 파이썬 미니 프로젝트
# 이름 또는 학번: 
# 프로젝트 주제: 

# ============================================================
# 사용 안내
# ------------------------------------------------------------
# 이 파일은 예시 골격입니다.
# 그대로 제출하지 말고, 반드시 자신의 주제에 맞게 수정하세요.
#
# 필수 조건
# 1. 2차원 리스트 사용
# 2. 함수 2개 이상, 가능하면 3개 이상 분리
# 3. 조건문 사용
# 4. 반복문 사용
# 5. 실행 결과 출력
# ============================================================


# ------------------------------------------------------------
# 1. 데이터 준비: 2차원 리스트
# ------------------------------------------------------------
# 아래 예시는 "활동 추천 프로그램"입니다.
# 자신의 주제에 맞게 data를 만드세요.
#
# 현재 열의 의미:
# 0번 열: 활동 이름
# 1번 열: 필요한 시간(분)
# 2번 열: 추천 기분
# 3번 열: 활동 유형
# ------------------------------------------------------------
# =================================================================
# [1단계] 데이터 구조 정의 (8x8 크기의 방 20개를 관리하는 대리스트)
# =================================================================
# 'W': 벽, '.': 복도, 'P': 링크, 'E': 초록 적, 'R': 빨간 적, 'T': 상자, 'D': 일반문, 'B': 보스문, 'G': 가논, 'Z': 젤다

# 샘플로 3개의 방 구조를 먼저 배치했어. 실제 프로젝트에서는 room_3부터 room_19까지 총 20개를 리스트에 채워 넣으면 돼!
room_0 = [
    ["W","W","W","W","W","W","W","W"],
    ["W","P",".",".","W",".","T","W"], # 첫 방에 상자(T) 배치
    ["W",".","W",".","W",".","W","W"],
    ["W","E","W",".",".",".",".","W"],
    ["W","W","W","W","W",".","W","W"],
    ["W",".",".",".","W",".",".","W"],
    ["W",".","W",".",".",".","W","W"],
    ["W","T","W","W","W","E","D","W"]  # 일반 잠긴 문 'D'
]

room_1 = [
    ["W","W","W","W","W","W","W","W"],
    ["W",".",".",".","W",".","E","W"],
    ["W","E","W",".","W",".","W","W"],
    ["W",".","W",".",".",".",".","W"],
    ["W",".","W","W","W","W","E","W"],
    ["W",".",".",".","T",".",".","W"], # 열쇠나 나침반이 숨겨진 상자
    ["W","W","W","W","W",".","W","W"],
    ["W","R",".",".",".",".","B","W"]  # 보스룸으로 향하는 보스잠긴문 'B'
]

room_2 = [
    ["W","W","W","W","W","W","W","W"],
    ["W",".",".",".",".",".",".","W"],
    ["W",".","W","W","W","W",".","W"],
    ["W",".","W",".",".","W",".","W"],
    ["W",".","W",".","G","W",".","W"], # 최종 보스 가논 'G'
    ["W",".","W","W","W","W",".","W"],
    ["W",".",".",".",".",".",".","W"],
    ["W","W","W","W","W","W","Z","W"]  # 젤다 공주 'Z'
]

# 💡 방 20개를 관리하는 3차원 형태의 대리스트 구조 (나머지 방들은 room_0을 복사해서 인덱스를 채워봐!)
hyrule_castle = [room_0, room_1, room_2] + [room_0 for _ in range(17)] 

# 링크의 상태 및 가방(인벤토리) 변수 설정
current_room = 0
player_row, player_col = 1, 1
player_hp = 30
has_hylian_shield = False
normal_keys = 0             # 일반 열쇠 개수 (D 문 오픈용)
has_boss_key = False        # 보스방 열쇠 보유 여부 (B 문 오픈용)
has_compass = False         # 나침반 보유 여부 (C 키로 활성화)

# =================================================================
# [2단계] 함수 분리 - 16x16 복도 스크린 시각화 및 나침반 탐색 함수
# =================================================================
def display_game(room_num, map_data, hp, shield, n_keys, b_key, compass):
    """
    8x8 데이터를 가로 2칸씩 출력하여 16x16 복도 스크린 효과를 내는 출력 함수
    """
    print(f"\n▲ [하이랄 던전 - {room_num}번 방] ▲")
    for row in map_data:
        for cell in row:
            if cell == "W": print("🧱🧱", end="")
            elif cell == "P": print("🗡️ ", end="")
            elif cell == "E": print("👿 ", end="")
            elif cell == "R": print("🔴 ", end="")
            elif cell == "T": print("📦 ", end="")
            elif cell == "D": print("🚪 ", end="") # 일반 문
            elif cell == "B": print("😈 ", end="") # 보스 문
            elif cell == "G": print("🐗 ", end="")
            elif cell == "Z": print("👑 ", end="")
            else: print(". .", end="") # 💡 길(`.`)을 복도처럼 가로로 2칸 연속 출력! (16x16 효과)
        print()
    print(f"\n❤️ 체력: {hp}/30 | 🛡️ 방패: {'유' if shield else '무'} | 🔑 일반열쇠: {n_keys}개 | 😈 보스열쇠: {'유' if b_key else '무'}")
    print(f"🧭 나침반: {'보유(C키로 지도스캔)' if compass else '미보유'}")
    print("=" * 45)

def use_compass(castle_data):
    """
    나침반 전용 데이터 탐색 알고리즘 (3중 반복문 및 조건문 필수 조건 충족)
    """
    print("\n🧭 [나침반 스캔] 전체 20개 방의 에너지를 동기화하여 탐색합니다...")
    for r_idx in range(len(castle_data)):
        box_count = 0
        has_boss = False
        for r in range(8):
            for c in range(8):
                if castle_data[r_idx][r][c] == "T": box_count += 1
                elif castle_data[r_idx][r][c] == "G": has_boss = True
        
        if box_count > 0 or has_boss:
            print(f"📍 [{r_idx}번 방] -> 보물상자(열쇠/포션 등): {box_count}개 감지", end="")
            if has_boss: print(" | ⚠️ 대마왕 가논의 강력한 암흑 기운 감지!")
            else: print()

# =================================================================
# [3~4단계] 메인 게임 루프 (반복문)
# =================================================================
game_running = True

while game_running and player_hp > 0:
    display_game(current_room, hyrule_castle[current_room], player_hp, has_hylian_shield, normal_keys, has_boss_key, has_compass)
    
    move = input("이동(W,A,S,D) 또는 아이템 사용(C:나침반): ").upper()
    
    # [특수 입력] 나침반 기능 작동 예외 처리
    if move == "C":
        if has_compass:
            use_compass(hyrule_castle)
        else:
            print("❌ 아직 나침반 아이템이 없습니다! 보물상자(📦)를 찾아보세요.")
        continue
        
    next_row, next_col = player_row, player_col
    if move == "W": next_row -= 1
    elif move == "S": next_row += 1
    elif move == "A": next_col -= 1
    elif move == "D": next_col += 1
    else:
        print("❌ 잘못된 입력입니다!")
        continue

    # 8x8 맵 안에서의 벽 충돌 검사
    if hyrule_castle[current_room][next_row][next_col] != "W":
        target = hyrule_castle[current_room][next_row][next_col]
        
        # [적과의 전투] 마스터 소드는 기본 보유 상태이므로 즉시 격파하지만, 등급별로 데미지를 입음
        if target == "E":
            print("\n💥 초록 경비병👿과의 전투! 마스터 소드로 즉시 처치했습니다.")
            damage = 4
            if has_hylian_shield: damage -= 2
            player_hp -= damage
            print(f"❤️ 하일리아의 방패 효과로 체력이 {damage}만 감소했습니다.")
            
        elif target == "R":
            print("\n💥 빨간 정예 경비병🔴과의 전투! 마스터 소드로 처치했으나 공격이 매섭습니다.")
            damage = 8
            if has_hylian_shield: damage -= 4
            player_hp -= damage
            print(f"❤️ 하일리아의 방패 효과로 체력이 {damage}만 감소했습니다.")

        # [보물상자 시스템] 여는 순서에 따라 획득하는 아이템이 정교하게 분기됨
        elif target == "T":
            print("\n📦 보물상자를 열었습니다!")
            if not has_hylian_shield:
                print("🛡️ '하일리아의 방패'를 획득했습니다! 경비병들의 공격을 방어합니다.")
                has_hylian_shield = True
            elif not has_compass:
                print("🧭 '나침반'을 획득했습니다! 이제 복도에서 [C]키를 눌러 전체 던전을 스캔할 수 있습니다.")
                has_compass = True
            elif normal_keys < 1: # 필요한 만큼 열쇠 수량 조절 가능
                print("🔑 '던전 일반 열쇠'를 얻었습니다! 잠긴 일반 문(🚪)을 열 수 있습니다.")
                normal_keys += 1
            elif not has_boss_key:
                print("😈 '보스방 열쇠'를 얻었습니다! 가논이 숨어있는 보스 문(😈)을 열 수 있습니다.")
                has_boss_key = True
            else:
                print("🧪 '빨간 포션'을 발견해 마셨습니다! 체력이 15 회복됩니다.")
                player_hp = min(30, player_hp + 15)

        # 💡 [미션 1] 일반 문('D')을 만났을 때 일반 열쇠(normal_keys)를 소모하고 방을 전환하는 코드를 완성해봐!
        elif target == "D":
            if normal_keys > 0:
                print("\n🔑 찰칵! 일반 열쇠를 써서 잠긴 문을 열고 다음 방으로 넘어갑니다.")
                normal_keys -= 1
                hyrule_castle[current_room][player_row][player_col] = "."
                # 여기에 다음 방 번호로 가산 처리하고 좌표를 초기화하는 코드를 적어봐!
                current_room += 1
                player_row, player_col = 1, 1
                hyrule_castle[current_room][player_row][player_col] = "P"
                continue
            else:
                print("\n🔒 문이 잠겨있습니다! 다른 복도의 보물상자에서 일반 열쇠(🔑)를 찾아오세요.")
                continue

        # 💡 [미션 2] 보스 문('B')을 만났을 때 보스 열쇠(has_boss_key)가 있는지 검사하는 조건문을 완성해봐!
        elif target == "B":
            pass # 네가 직접 elif 문 안쪽을 조건 검사와 방 번호 이동 코드로 채워야 할 곳!

        # 최종 보스전 및 엔딩
        elif target == "G":
            print("\n🔥 [FINAL BATTLE] 대마왕 가논🐗과의 최종 결전! 기본 장착된 마스터 소드로 가논을 영원히 봉인합니다!")
            hyrule_castle[current_room][next_row][next_col] = "." # 가논 소멸
            
        elif target == "Z":
            print("\n👑 축하합니다! 젤다 공주를 구출하고 20개의 방으로 이뤄진 하이랄 던전을 돌파했습니다! 👑")
            game_running = False

        # 💡 [미션 3] 링크를 2차원 지도 상에서 정상 이동시키는 리스트 좌표 업데이트 코드를 채워넣어봐!
        hyrule_castle[current_room][player_row][player_col] = "."
        player_row, player_col = next_row, next_col
        hyrule_castle[current_room][player_row][player_col] = "P"

    else:
        print("W 벽에 부딪혀 지나갈 수 없습니다!")

if player_hp <= 0:
    print("\n💀 링크의 체력이 다했습니다... 게임 오버! 💀")