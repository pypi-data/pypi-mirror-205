from batch_normalization_folding.TensorFlow.back_forth import check_layer
from batch_normalization_folding.TensorFlow.modify_bn_graph import remove_folded_layers
from batch_normalization_folding.TensorFlow.add_biases import (
    complete_model,
    check_if_need_completion,
)
from batch_normalization_folding.TensorFlow.update_fold_weights import fold_weights
from batch_normalization_folding.TensorFlow.deep_copy import deep_copy_a_model
from batch_normalization_folding.TensorFlow.concat_handler import (
    handle_concatenation_layer,
    get_graph_as_dict,
    reverse_graph,
)
from typing import Dict, Tuple
import tensorflow as tf


def should_be_folded(model: tf.keras.Model) -> bool:
    """
    if a model does not contain any bn layers let's not touch it

    Args:
        model: model to study
    """
    should_be_folded = False
    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.BatchNormalization):
            should_be_folded = True
    return should_be_folded


def fold_tensorflow_model(
    model: tf.keras.Model, verbose: bool
) -> Tuple[tf.keras.Model, str]:
    """
    In this functio nwe fold the model
    But we also update the batchnorm statistics adequately
    """
    if not should_be_folded(model=model):
        if verbose:
            print("\r+" + "-" * 36 + "+")
            print(f"| {model.name.center(34).replace('_', ' ')} |")
            print("\r+" + "-" * 36 + "+")
            print(f"| BN layers folded         | " f'{f"{0}".center(7):<7} |')
            print(
                f"| BN layers not folded     | "
                f'{f"{len(model.layers)}".center(7):<7} |'
            )
            print("+" + "-" * 36 + "+")
        return model, ""
    model_to_fold = deep_copy_a_model(model=model)
    backward_graph = get_graph_as_dict(model=model_to_fold)
    forward_graph = reverse_graph(graph=backward_graph)
    fold_dict = {}
    unfolded_layers = 0
    for layer in model_to_fold.layers:
        if isinstance(layer, tf.keras.layers.BatchNormalization):
            foldeable, roots, leaves, forward = check_layer(
                model=model_to_fold,
                layer=layer,
                forward_graph=forward_graph,
                backward_graph=backward_graph,
            )
            if foldeable:
                fold_dict[layer.name] = (roots, leaves, forward)
            else:
                unfolded_layers += 1
    fold_dict = handle_concatenation_layer(
        model=model, fold_dict=fold_dict, graph_as_dict=forward_graph
    )
    layers_to_complete = check_if_need_completion(model=model, fold_dict=fold_dict)
    if verbose:
        print("\r+" + "-" * 36 + "+")
        print(f"| {model.name.center(34).replace('_', ' ')} |")
        print("\r+" + "-" * 36 + "+")
        print(f"| BN layers folded         | " f'{f"{len(fold_dict)}".center(7):<7} |')
        print(f"| BN layers not folded     | " f'{f"{unfolded_layers}".center(7):<7} |')
        print("+" + "-" * 36 + "+")
    if len(layers_to_complete) != 0:
        model_to_fold = complete_model(
            model=model_to_fold, layers_to_complete=layers_to_complete
        )
    fold_weights(model=model_to_fold, fold_dict=fold_dict)
    model_to_fold = remove_folded_layers(
        model=model_to_fold,
        backward_graph=get_graph_as_dict(model=model_to_fold),
        fold_dict=fold_dict,
    )
    return model_to_fold, f"{len(fold_dict)}/{unfolded_layers}"
