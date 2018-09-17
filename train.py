import functools
import tensorflow as tf
from core import trainer, input_reader
from core.model_builder import build_man_model
from google.protobuf import text_format
from object_detection.builders import input_reader_builder
from object_detection.protos import input_reader_pb2
from object_detection.protos import model_pb2
from object_detection.protos import pipeline_pb2
from object_detection.protos import train_pb2
import os

os.environ["CUDA_VISIBLE_DEVICES"]="1,2"

tf.logging.set_verbosity(tf.logging.INFO)

flags = tf.app.flags

flags.DEFINE_string('train_dir', 'model/dump',
                    'Directory to save the checkpoints and training summaries.')
flags.DEFINE_string('pipeline_config_path', 'model/ssd_mobilenet_imagenet.config',
                    'Path to a pipeline_pb2.TrainEvalPipelineConfig config '
                    'file. If provided, other configs are ignored')
flags.DEFINE_string('train_config_path', '',
                    'Path to a train_pb2.TrainConfig config file.')
flags.DEFINE_string('input_config_path', '',
                    'Path to an input_reader_pb2.InputReader config file.')
flags.DEFINE_string('model_config_path', '',
                    'Path to a model_pb2.DetectionModel config file.')
flags.DEFINE_string('image_root', '/media/Linux/Research/DataSet/ILSVRC2014_DET/image/ILSVRC2014_DET_train',
                    'Root path to input images')

FLAGS = flags.FLAGS


def get_configs_from_pipeline_file():
  """Reads training configuration from a pipeline_pb2.TrainEvalPipelineConfig.

  Reads training config from file specified by pipeline_config_path flag.

  Returns:
    model_config: model_pb2.DetectionModel
    train_config: train_pb2.TrainConfig
    input_config: input_reader_pb2.InputReader
  """
  pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
  with tf.gfile.GFile(FLAGS.pipeline_config_path, 'r') as f:
    text_format.Merge(f.read(), pipeline_config)

  model_config = pipeline_config.model.ssd
  train_config = pipeline_config.train_config
  input_config = pipeline_config.train_input_reader

  return model_config, train_config, input_config

def main(_):
    model_config, train_config, input_config = get_configs_from_pipeline_file()
    model_fn = functools.partial(
        build_man_model,
        model_config=model_config,
        is_training=True)
    create_input_dict_fn = functools.partial(
        input_reader.read, input_config)
    trainer.train(model_fn, create_input_dict_fn, train_config, FLAGS.train_dir, FLAGS.image_root)






if __name__ == '__main__':
  # update moving average
  tf.app.run()
