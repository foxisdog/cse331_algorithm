ulimit -s unlimited

python3 ./kmeans_heldkarp.py ./datasets/a280.csv
python3 ./2app.py ./datasets/a280.csv
python3 ./christo3.py ./datasets/a280.csv
python3 ./christo5.py ./datasets/a280.csv

python3 ./kmeans_heldkarp.py ./datasets/xql662.csv
python3 ./2app.py ./datasets/xql662.csv
python3 ./christo3.py ./datasets/xql662.csv
# python3 ./christo5.py ./datasets/xql662.csv

python3 ./kmeans_heldkarp.py ./datasets/kz9976.csv
python3 ./2app.py ./datasets/kz9976.csv
python3 ./christo3.py ./datasets/kz9976.csv
# python3 ./christo5.py ./datasets/kz9976.csv

python3 ./kmeans_heldkarp.py ./datasets/mona-lisa100K.csv
python3 ./2app.py ./datasets/mona-lisa100K.csv
# python3 ./christo3.py ./datasets/mona-lisa100K.csv
# python3 ./christo5.py ./datasets/mona-lisa100K.csv