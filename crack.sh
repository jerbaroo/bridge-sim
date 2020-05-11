# Stress strength plot.
./cli.sh --shorten-paths true --mesh full --save-to crack/ss validate stress-strength
./cli.sh --shorten-paths true --mesh full --save-to crack/ss validate stress-strength --top

# arpi's mid-span
./cli.sh --shorten-paths true --mesh full --save-to crack/mid-span verify truck1-contour --rt ytrans --x 56 --crack-x 48 --length 14 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/mid-span verify truck1-contour --rt ytrans --x 56 --crack-x 48 --length 14 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/mid-span verify truck1-contour --rt strain --x 56 --crack-x 48 --length 14 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/mid-span verify truck1-contour --rt strain --x 56 --crack-x 48 --length 14 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/mid-span verify truck1-contour --rt strain-z --x 56 --crack-x 48 --length 14 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/mid-span verify truck1-contour --rt strain-z --x 56 --crack-x 48 --length 14 --outline --wheels

# full mid-span
./cli.sh --shorten-paths true --mesh full --save-to crack/full-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 41.25 --length 20 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/full-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 41.25 --length 20 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/full-mid-span verify truck1-contour --rt strain --x 55 --crack-x 41.25 --length 20 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/full-mid-span verify truck1-contour --rt strain --x 55 --crack-x 41.25 --length 20 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/full-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 41.25 --length 20 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/full-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 41.25 --length 20 --outline --wheels

# 5m mid-span
./cli.sh --shorten-paths true --mesh full --save-to crack/5m-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 50 --length 5 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/5m-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 50 --length 5 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/5m-mid-span verify truck1-contour --rt strain --x 55 --crack-x 50 --length 5 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/5m-mid-span verify truck1-contour --rt strain --x 55 --crack-x 50 --length 5 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/5m-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 50 --length 5 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/5m-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 50 --length 5 --outline --wheels

# 3m mid-span
./cli.sh --shorten-paths true --mesh full --save-to crack/3m-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 50 --length 3 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/3m-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 50 --length 3 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/3m-mid-span verify truck1-contour --rt strain --x 55 --crack-x 50 --length 3 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/3m-mid-span verify truck1-contour --rt strain --x 55 --crack-x 50 --length 3 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/3m-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 50 --length 3 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/3m-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 50 --length 3 --outline --wheels

# 1m mid-span
./cli.sh --shorten-paths true --mesh full --save-to crack/1m-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 50 --length 1 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/1m-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 50 --length 1 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/1m-mid-span verify truck1-contour --rt strain --x 55 --crack-x 50 --length 1 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/1m-mid-span verify truck1-contour --rt strain --x 55 --crack-x 50 --length 1 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/1m-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 50 --length 1 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/1m-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 50 --length 1 --outline --wheels

# 0.5m mid-span
./cli.sh --shorten-paths true --mesh full --save-to crack/05m-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 50 --length 0.5 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/05m-mid-span verify truck1-contour --rt ytrans --x 55 --crack-x 50 --length 0.5 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/05m-mid-span verify truck1-contour --rt strain --x 55 --crack-x 50 --length 0.5 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/05m-mid-span verify truck1-contour --rt strain --x 55 --crack-x 50 --length 0.5 --outline --wheels
./cli.sh --shorten-paths true --mesh full --save-to crack/05m-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 50 --length 0.5 --outline --wheels --temp
./cli.sh --shorten-paths true --mesh full --save-to crack/05m-mid-span verify truck1-contour --rt strain-z --x 55 --crack-x 50 --length 0.5 --outline --wheels
