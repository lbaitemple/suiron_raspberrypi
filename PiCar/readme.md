These files are used to run the pi car
to start the webcam we will use 
cd /mjpg-streamer/mjpg-streamer-experimental
sudo ./mjpg_streamer -i "./input_uvc.so -f 10 -r 148x102 -n -y" -o "./output_http.so -w ./www -p 8080"
