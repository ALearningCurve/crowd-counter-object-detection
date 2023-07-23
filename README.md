# About

![example detection](exampleImages\example1.png) ![example detection](exampleImages\example2.png) ![example detection](exampleImages\example3.png)

Are you curious about when the Northeastern student center is the busiest? Well that is what I am to discover in this project. 
Using a public webcam in the student center ([see here for yourself]('http://129.10.161.241/mjpg/video.mjpg')), I aim to capture a frame of what the webcam sees (see `./videoscraper.py`),
and then train an object detection model to count the number of heads. Interestingly, we have to train our own object detection model as the angle and quality of the
webcam is very different compared to other training datasets. For that reason, I trained the model to recognize the heads of people in the student center as often people are sitting or talking with others so their bodies are obscured, but their heads are not!

## How to run the webcam scraper
1. Create a virtual environment
2. Run `pip install -r scraper_requirements.txt` to install the requirement for the image scraper
3. Run `python videoscraper.py 10 days=7`
    - The first argument (`10`) in this example is the number of minutes between each capture
    - The second argument (`days=7`) is the duration of time to run the scraper for
    - NOTE: I recommend running this on a raspberry pi of some sort as it requires little processing power and needs to be running 24/7 since you are capturing real time data

## How to train and evaluate the model yourself
0. Setup your environment following the instructions here: https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html
1. Train and label data in the TensorFlow/workspace/head_counter/images test and train directories (I used the `labelImg` library and labeled the heads in the image)
2. make labels
    - run `python TensorFlow\scripts\preprocessing\generate_tfrecord.py -x TensorFlow\workspace\head_detector\images\train -l TensorFlow\workspace\head_detector\annotations\label_map.pbtxt -o TensorFlow\workspace\head_detector\annotations\train.record`
    - run `python TensorFlow\scripts\preprocessing\generate_tfrecord.py -x TensorFlow\workspace\head_detector\images\test -l TensorFlow\workspace\head_detector\annotations\label_map.pbtxt -o TensorFlow\workspace\head_detector\annotations\test.record`
    - I only used 1 label, `head`, so if you make multiple labels you will have to update the pipeline config to reflect that
3. cd into the `TensorFlow\workspace\head_detector` folder
3. train the model `python model_main_tf2.py --model_dir=models\centernet_resnet101_v1_fpn --pipeline_config_path=models\centernet_resnet101_v1_fpn\pipeline.config`
4. export the model `python exporter_main_v2.py --input_type image_tensor --pipeline_config_path models\ssd_mobilenet_v2_fpnlite_320\pipeline.config --trained_checkpoint_dir models\ssd_mobilenet_v2_fpnlite_320 --output_directory exported-models\head_detector`
5. run `test_with_exported.ipynb` which will load the model, detect heads in all image in the `frames` directory, and plot the detected results

Alternatively, you can skip steps 0-4 and just use the model located at `TensorFlow\workspace\head_detector\exported-models\head_detector\saved_model`, which is the export of the model I trained myself

Note: I found that running the `./crop.ipynb` notebook is useful before labeling data as the raw screenshot taken by the video scraper include very pixelated heads in the distance which may confuse the detector. Although we are only looking at a smaller subset of the image, we can still analyze the overall busyness of the student center by comparing the relative amount of people in the images.