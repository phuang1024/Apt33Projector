while [ true ]
do
    echo 120 > time_limit.txt
    python screensaver.py
    echo 30 > time_limit.txt
    python image.py fluid.mp4
    echo 120 > time_limit.txt
    python text.py --file next_stops.txt
    echo 30 > time_limit.txt
    python game_of_life.py
    echo 90 > time_limit.txt
    python snake.py --auto
done
