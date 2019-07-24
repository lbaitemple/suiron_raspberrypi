These files are used to run the pi car
2. To start the webcam we will use 
```
git clone https://github.com/jacksonliam/mjpg-streamer
cd /mjpg-streamer/mjpg-streamer-experimental
sudo ./mjpg_streamer -i "./input_uvc.so -f 10 -r 148x102 -n -y" -o "./output_http.so -w ./www -p 8080"
```
