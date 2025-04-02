while [ true ]
do
    python screensaver.py --limit 180
    python image.py fluid.mp4 --limit 10
    python text.py --file next_stops.txt --limit 180
    python game_of_life.py --limit 30
    python snake.py --auto --limit 180
done
