#Command to train an image classifier model : 

make_image_classifier \
  --image_dir /Users/mmalherbe/Desktop/fridgepy/tensortrain/tensorflow_image_classifier/tffiles/classifier/data \
  --tfhub_module https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4 \
  --image_size 224 \
  --saved_model_dir /Users/mmalherbe/Desktop/fridgepy/imageclassifier/ \
  --labels_output_file class_labels.txt \
  --tflite_output_file new_mobile_model.tflite
