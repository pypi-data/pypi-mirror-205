"""
Copyright 2022  Salvatore Barone <salvatore.barone@unina.it>
                Filippo Ferrandino <fi.ferrandino@studenti.unina.it>

This is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation; either version 3 of the License, or any later version.

This is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
RMEncoder; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA 02110-1301, USA.
"""
import numpy as np
import tensorflow as tf
from numba import cuda
from inspectnn.BaseLayer import BaseLayer
from inspectnn.Conv.Conv_kernel_tflite import convolve_tflite_occorenza,convolve_tflite, convolve_tflite_padding,convolve_tflite_fake,convolve_tflite_mf, convolve_tflite_padding_mf,convolve_tflite_fake_mf
from inspectnn.Conv.ConvLayer import ConvLayer

class ConvLayer_TFLITE(ConvLayer):
    def __init__(self, stride = (1, 1), padding = (0,0),padding_type='valid', activation = "relu", quant_nbits = 8, multiplier = BaseLayer.default_multiplier, name = "Conv_TFlite",offset=[128,128],print_output=None):
        super().__init__(stride=stride,activation=activation, quant_nbits=quant_nbits, multiplier=multiplier, name=name,print_output=print_output,padding=padding,offset=offset)
        self.padding_type = padding_type
        self.idx_multiply = None

    def __deepcopy__(self, memo = None):
        return ConvLayer_TFLITE(stride = self.stride, padding = self.padding, activation = self.activation, quant_nbits = self.quant_nbits, multiplier = self.multiplier, name = self.name)

    def forward_pass(self, **kwargs):
        #TODO: rinominare variabili

        A_global_mem = self.pre_layer.results 

        #TODO: rinominare M
        
        #print(self.name,'dati input',A_global_mem.copy_to_host()[0][0])
        if(self.idx_multiply is None):

            if (self.normal_kernel):
                cuda.synchronize()
                convolve_tflite_occorenza[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.n_channels,self.k_mul,self.k_filtri,self.k_bias,self.M,128,128,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,self.occorenza)
            elif (self.fake_kernel):
                cuda.synchronize()
                convolve_tflite_fake[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.n_channels,self.k_mul,self.k_filtri,self.k_bias,self.M,128,128,
                                                            self.activation,self.output_mul,self.output_offset,self.stride)
            else:
                value_null = self.pre_layer.output_offset
                cuda.synchronize()
                convolve_tflite_padding[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.n_channels,self.k_mul,self.k_filtri,self.k_bias,self.M,128,128,
                                                                                self.activation,self.output_mul,self.output_offset,value_null,self.stride)
        else:
            #print(self.name,self.idx_multiply)
            idxm = cuda.to_device(np.ascontiguousarray(self.idx_multiply))
            if (self.normal_kernel):
                cuda.synchronize()
                convolve_tflite_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.n_channels,self.k_mul,self.k_filtri,self.k_bias,self.all_M,128,128,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm)
            elif (self.fake_kernel):
                cuda.synchronize()
                convolve_tflite_fake_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.n_channels,self.k_mul,self.k_filtri,self.k_bias,self.all_M,128,128,
                                                            self.activation,self.output_mul,self.output_offset,self.stride,idxm)
            else:
                value_null = self.pre_layer.output_offset
                cuda.synchronize()
                convolve_tflite_padding_mf[self.griddim, self.blockdim](self.results,A_global_mem,self.kernel_global_mem,self.n_channels,self.k_mul,self.k_filtri,self.k_bias,self.all_M,128,128,
                                                                                self.activation,self.output_mul,self.output_offset,value_null,self.stride,idxm)
     
        
        #TODO: calcolare grid_dim per quant 3d

        #print(self.name,"out",self.results.copy_to_host()[0][3])
        #print(self.name,"max out",np.max(self.results.copy_to_host()))
        #print(np.max(self.results.copy_to_host()),np.min(self.results.copy_to_host()))
        
        if self.gpu_output_memory == False:
            self.outputv[:,:,:] = self.results.copy_to_host()            
    
    def load_weights(self, **kwargs):
        #TODO: sfrutare anche super().load_weights(**kwargs)

        self.enable_gpu = kwargs["enable_gpu"] 
        self.input_shape= kwargs["input_shape"]
        self.kernel_shape = np.shape(kwargs["weights"])        
        self.output_shape = kwargs["output_shape"]
    
        self.n_channels=self.kernel_shape[0]
        self.n_filter = self.n_channels
        self.quanto_k = None
        self.quanto_b = None

        
        #TODO: considera che è sempre su gpu
        if self.enable_gpu:
            self.use_gpu=True
            self.M = self.multiplier
            #TODO: parametrizare il k
            self.blockdim = (2,2,4)
            self.griddim = (self.output_shape[0] // self.blockdim[0] + 1, self.output_shape[1] // self.blockdim[1] + 1,self.output_shape[2] // (self.blockdim[2]*1) + 1)#,n_channels)
            self.occorenza = cuda.to_device(np.zeros((self.n_filter,256,256),dtype=np.int32))
            self.kernel_global_mem = cuda.to_device(np.array(kwargs["weights"],dtype=np.int8))
            self.results = cuda.device_array(self.output_shape, dtype=np.int8)

            self.gpu_input_memory = kwargs["gpu_input_memory"]

            if ( kwargs["quant_data"] is not None):
                self.quantization=True
                self.quanto_b = cuda.to_device(np.ascontiguousarray(kwargs["quant_bias"]))
                self.quanto_k = cuda.to_device(np.ascontiguousarray(kwargs["quant_data"]))

                self.k_mul = cuda.to_device(np.ascontiguousarray(kwargs["quant_data"]*kwargs["quant_input_k"]))#TODO:parametrizare il 255
                self.k_filtri = cuda.to_device(np.ascontiguousarray(np.sum(kwargs["weights"],(1,2,3))*kwargs["quant_data"]*kwargs["quant_input_offset"]*kwargs["quant_input_k"]))#TODO:parametrizare il diviso 2 con alfa input+offest input
                self.k_bias = cuda.to_device(np.ascontiguousarray(kwargs["biases"]*kwargs["quant_bias"]))

                self.output_mul= 1/kwargs["quant_output_k"]
                self.output_offset= kwargs["quant_output_offset"]

            if self.print_output:
                self.outputv = np.zeros(self.output_shape)              
        else:
            self.convkernel, self.biases =kwargs["weights"], kwargs["biases"]
            self.outputv = np.zeros(self.output_shape)
        
        #TODO: valutare se spostare nella convLayerBase
        self.padding_kernel = (self.padding_type != 'valid')#mannagia
        self.fake_kernel = (kwargs["weights"].shape[1] == 1 and kwargs["weights"].shape[2] == 1)
        self.normal_kernel = not self.padding_kernel and not self.fake_kernel
        self.activation = (self.activation == "relu" or self.activation == "Relu")
        if True:#None == self.gpu_input_memory:#TODO:parametrizare meglio
                self.outputv = np.zeros(self.output_shape,dtype=np.int32)          
        return self.output_shape
  