#Source : https://github.com/tensorflow/hub/tree/master/tensorflow_hub/tools/make_image_classifier



#Required : 

$ pip install "tensorflow~=2.0"
$ pip install "tensorflow-hub[make_image_classifier]~=0.6"

#Command to train an image classifier model : 

/Users/mmalherbe/.virtualenvs/cv/bin/make_image_classifier  \
  --image_dir /Users/mmalherbe/Desktop/fridgepy/tensortrain/data/ \
  --tfhub_module https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4 \
  --image_size 224 \
  --saved_model_dir /Users/mmalherbe/Desktop/fridgepy/imageclassifier/ \
  --labels_output_file imageclassifier/class_labels.txt \
  --tflite_output_file imageclassifier/new_mobile_model.tflite
