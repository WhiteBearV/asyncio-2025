import time
from datetime import timedelta


speed = 1000
Judit_time = 5 / speed
Opponent_time = 55 / speed
Opponent = 24 # Number of opponents or Num of Games
move_pairs = 30 

#(5(Judit_time)+55(Opponent_time))*30(move_pairs) = 1800 second

def game(x):
#Loops (move pairs) times to sinulate both players making a move
    board_start_time = time.perf_counter()
    calculated_board_start_time = 0
    for i in range(move_pairs): 
        time.sleep(Judit_time)
        calculated_board_start_time = calculated_board_start_time + Judit_time
        print(f"BOARD-{x+1} {i+1} Judit made a nove with {int (Judit_time*speed)} secs.")
    # The opponent thinks for 5 seconds.
        time.sleep(Opponent_time)
        print (f"BOARD-{x+1} {i+1} Opponent sade sove wit {int(Opponent_time*speed)} secs.")
        calculated_board_start_time = calculated_board_start_time + Opponent_time
    print(f"B0ARD- {x+1} ->>>>>>>>>>>>> Finished Bove in {(time.perf_counter() - board_start_time)*speed:.1f} secs")
    print(f"BOARD-{x+1} ->>>>>>>>>>>>>> Finished move in {calculated_board_start_time *speed:.1f} secs(calculated) \n")
    return [(time.perf_counter() - board_start_time), calculated_board_start_time]


if __name__ == "__main__":
    print("Number of boards: , {Opponent} game")
    print("Nomber of move pairs: , {move_pairs} pairs")
    start_time = time.perf_counter()

    board_times = 0
    calculated_board_times = 0
    for board in range(Opponent):
        board_times += game(board)[0]
        calculated_board_times += game(board)[1]

    print(f"Board exhibition finished for {Opponent} opponents in {timedelta(seconds=round (board_times*speed))} hr.")
    print(f"Board exhibition finished for {Opponent} opponents in {timedelta(seconds=round (calculated_board_times*speed))} hr. (calculated)")
    print(f"Finished in {round(time.perf_counter() - start_time)} secs.")

