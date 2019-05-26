
let i=6
files=`ls -lrt *.png`
for f in $files;do mv $f img$i.png;let i=$i+1; done

ffmpeg -r 6 -f image2 -i img%d.png -vcodec libx264 -crf 25  test.mp4
