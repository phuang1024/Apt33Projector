while [ true ]
do
    echo 150 > time_limit.txt
    python screensaver.py
    echo 10 > time_limit.txt
    python image.py fluid.mp4
    echo 150 > time_limit.txt
    python text.py --file next_stops.txt
    echo 30 > time_limit.txt
    python game_of_life.py
    echo 180 > time_limit.txt
    python snake.py --auto
done
