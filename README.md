# About

## Setup
Setup your environment following the instructions here:
https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html


python model_main_tf2.py --model_dir=models\ssd_mobilenet_v2_fpnlite_320 --pipeline_config_path=models\ssd_mobilenet_v2_fpnlite_320\pipeline.config

python model_main_tf2.py --model_dir=models\centernet_resnet101_v1_fpn --pipeline_config_path=models\centernet_resnet101_v1_fpn\pipeline.config
python exporter_main_v2.py --input_type image_tensor --pipeline_config_path models\ssd_mobilenet_v2_fpnlite_320\pipeline.config --trained_checkpoint_dir models\ssd_mobilenet_v2_fpnlite_320 --output_directory exported-models\head_detector