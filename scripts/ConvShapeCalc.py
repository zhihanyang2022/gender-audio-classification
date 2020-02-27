"""
ConvShapeCalc.py
Zhihan Yang
"""

import numpy as np
import torch
import torch.nn as nn
from flatten import Flatten

def fmap_shape_from_tuple(input_shape:tuple, out_channels:int, kernel_size:int, stride:int, padding:int, dilation:int=1, downsize=True, output_padding=None):
    """
    Compute the size of feature maps given the input size.

    param: input_size: a tuple with format (channel, height, width)

    References:
    * https://pytorch.org/docs/stable/nn.html#conv2d
    * https://pytorch.org/docs/stable/nn.html#maxpool2d
    """

    if downsize:
        formula = lambda x : np.floor((x + 2 * padding - dilation * (kernel_size - 1) - 1) / stride + 1)
    else:
        formula = lambda x : np.ceil((x - 1) * stride - 2 * padding + kernel_size + output_padding)

    h, w = input_shape[1], input_shape[2]
    h_out, w_out = formula(h), formula(w)
    shape_out = (int(out_channels), int(h_out), int(w_out))
    print('Output shape: ', shape_out)

    return shape_out

def fmap_shape_from_layer(layer, input_shape):
    """
    Print and return the shape of a layer's output feature.

    * Caution: For different layer types, this function works slightly differently (see the if-else statements in the function body for more information).
    * Caution: In order to make this function unresponsive to certain layers (e.g. do not print the input shape because the summary of that layer is not yet implemented), make sure all print statements are placed under the if-else statements.

    * Use case: The output shape returned can then be passed into the same function but applied to a subsequent layer.
    * Use case: When defining model classes that inherit from torch.nn.Modules, it might be more convenient to use the `fmap_shape_from_sequential` function.

    param: layer: an instance of a PyTorch layer class
    param: input shape: a tuple with format (channel, height, width)

    return: the output shape
    """

    # route for Conv2d layers
    if isinstance(layer, torch.nn.modules.conv.Conv2d):
        print('* Input shape: {}'.format(input_shape), end=' -> ')
        print('{}'.format('Conv2d'), end=' -> ')
        return fmap_shape_from_tuple(input_shape, out_channels=layer.out_channels, kernel_size=layer.kernel_size[0], stride=layer.stride[0], padding=layer.padding[0], dilation=layer.dilation[0])

    # route for MaxPool2d layers
    elif isinstance(layer, torch.nn.modules.pooling.MaxPool2d):
        print('* Input shape: {}'.format(input_shape), end=' -> ')
        print('{}'.format('MaxPool2d'), end=' -> ')
        return fmap_shape_from_tuple(input_shape, out_channels=input_shape[0], kernel_size=layer.kernel_size, stride=layer.stride, padding=layer.padding, dilation=layer.dilation)

    elif isinstance(layer, torch.nn.modules.conv.ConvTranspose2d):
        print('* Input shape: {}'.format(input_shape), end=' -> ')
        print('{}'.format('ConvTranpose2d'), end=' -> ')
        return fmap_shape_from_tuple(input_shape, out_channels=layer.out_channels, kernel_size=layer.kernel_size[0], stride=layer.stride[0], padding=layer.padding[0], dilation=layer.dilation[0], downsize=False, output_padding=layer.output_padding[0])

    elif isinstance(layer, Flatten):
        print('* Input shape: {}'.format(input_shape), end=' -> ')
        print('{}'.format('Flatten'), end=' -> ')
        print('Output shape:', np.prod(input_shape))
        return np.prod(input_shape)

    elif isinstance(layer, torch.nn.Linear):
        print('* Input shape: {}'.format(input_shape), end=' -> ')
        print('{}'.format('Linear'), end=' -> ')
        print('Output shape:', layer.out_features)
        return layer.out_features

    else:  # this condition is for layers that do not change their input shapes, e.g, ReLU
        return input_shape

def fmap_shape_from_sequential(sequential, input_shape):
    for layer in sequential:
        input_shape = fmap_shape_from_layer(layer, input_shape)
    return input_shape
