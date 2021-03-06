'''@file loss_evaluator.py
contains the LossEvaluator class'''

import tensorflow as tf
import evaluator
from nabu.neuralnetworks.loss_computers import loss_computer_factory

class LossEvaluator(evaluator.Evaluator):
    '''The Decoder Evaluator is used to evaluate a decoder'''

    def __init__(self, conf, dataconf, model, output_name):
        '''Evaluator constructor

        Args:
            conf: the evaluator configuration as a ConfigParser
            dataconf: the database configuration
            model: the model to be evaluated
            output_name: the name of the output of the model to concider
        '''


        super(LossEvaluator, self).__init__(conf, dataconf, model, output_name)
        self.loss_computer = loss_computer_factory.factory(
		conf.get('evaluator','loss_type'))(
		int(conf.get('evaluator','batch_size')))


    def _get_outputs(self, inputs, input_seq_length):
        '''compute the validation logits for a batch of data

        Args:
            inputs: the inputs to the neural network, this is a list of
                [batch_size x ...] tensors
            input_seq_length: The sequence lengths of the input utterances, this
                is a list of [batch_size] vectors

        Returns:
            the outputs'''

        with tf.name_scope('evaluate_loss'):
            logits = self.model(
                inputs, input_seq_length, False)

        return logits


    def compute_loss(self, targets, logits, seq_length):
        '''compute the validation loss for a batch of data

        Args:
            targets: a dictionary of [batch_size x time x ...] tensor containing
                the targets
            logits: a dictionary of [batch_size x time x ...] tensor containing
                the logits
            seq_length: a dictionary of [batch_size] vectors containing
                the sequence lengths

        Returns:
            the loss as a scalar'''

        with tf.name_scope('evaluate_loss'):
            loss, norm = self.loss_computer(targets, logits, seq_length)

        return loss, norm
