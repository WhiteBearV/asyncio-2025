import time
from datetime import timedelta
import asyncio

speed = 100 # speed
Judit_time = 5/speed # Judit time move
Opponent_time = 55/speed # Opponent time move
opponents = 24 # Number of opponnents
move_pairs = 30 # Number of move pairs

async def game(x):

# Again notice that I declare the main() function as a async function
    board_start_time = time.perf_counter()
    for i in range(move_pairs):
        # print(f"BOARD-{x} {1+1} Judit thinking of making a move.")
        # Don't use time.sleep in a async function. I'm using it because in reality you aren't thinking about making a
        # move on 24 boards at the same time, and so I need to block the event loop.
        time.sleep(Judit_time)
        print(f"BOARD-{x+1} {i+1} Judit made a move with {int(Judit_time*speed)} secs.")
        # Here our opponent is making their turn and now we can move onto the next board.
        await asyncio.sleep(Opponent_time)
        print(f"BOARD-{x+1} {1+1} Opponent made move with {int (Opponent_time*speed)} secs.")
    print(f"BOARD-{x+1} >>>>>>>>>>>>>>>>> Finished move in {(time.perf_counter() - board_start_time)*speed:.1f} secs.\n")
    return {
    'calculated_board_time': (time.perf_counter() - board_start_time)*speed
        }
async def main():
# Again same structure as in async-io.py
    tasks = []
    for i in range(opponents):
        tasks += [game(i)]
    await asyncio.gather(*tasks)
    print(f"Board exhibition finished for {opponents} opponents in {timedelta(seconds=speed*round(time.perf_counter() - start_time))} hr.")

if __name__ == "__main__":
    print(f"Number of games: {opponents} games.")
    print(f"Number of move: {move_pairs} pairs.")
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Finished in {round(time.perf_counter() - start_time)} secs.")



# import asyncio
# import time
# from datetime import timedelta

# speed = 10000
# Judit_time = 5 / speed
# Opponent_time = 55 / speed
# opponent = 24
# move_pairs = 30

# async def play_game(board_id):
#     board_start_time = time.perf_counter()
#     calc_board_time = 0

#     for i in range(move_pairs):
#         await asyncio.sleep(Judit_time)
#         calc_board_time += Judit_time
#         print(f"Board-{board_id + 1} {i + 1} Judit made move with {int(Judit_time * speed):.1f} sec.")

#         await asyncio.sleep(Opponent_time)
#         print(f"Board-{board_id + 1} {i + 1} Opponent made move with {int(Opponent_time * speed):.1f} sec.")
#         calc_board_time += Opponent_time

#     real_duration = (time.perf_counter() - board_start_time)
#     print(f"BOARD-{board_id + 1} - >>>>>>>>>>>>>>>> Finished move in {real_duration * speed:.1f} secs")
#     print(f"BOARD-{board_id + 1} - >>>>>>>>>>>>>>>> Finished move in {calc_board_time * speed:.1f} secs (calculated)\n")
#     return real_duration, calc_board_time

# async def main():
#     print(f"Number of games: {opponent} games.")
#     print(f"Number of move: {move_pairs} pairs.\n")

#     start_time = time.perf_counter()

#     results = await asyncio.gather(*(play_game(i) for i in range(opponent)))

#     total_real_time = sum(r[0] for r in results)
#     total_calc_time = sum(r[1] for r in results)

#     print(f"Board exhibition finished for {opponent} opponents in {timedelta(seconds=round (total_real_time*speed))} hr.")
#     print(f"Board exhibition finished for {opponent} opponents in {timedelta(seconds=round (total_calc_time*speed))} hr. (calculated)")
#     print(f"Finished in {round(time.perf_counter() - start_time)} secs.")

# if __name__ == "__main__":
#     asyncio.run(main())