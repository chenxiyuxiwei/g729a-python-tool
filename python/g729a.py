from typing import *
import ctypes
import wave
import os

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
PATH = os.path.dirname(current_file_path)

import os
g729a_lib_path = ''
if os.name == 'nt':
    # g729a_lib_path = './libg729a.dll'
    g729a_lib_path = PATH + "\\" + 'libg729a.dll'
elif os.name == 'posix':
    # g729a_lib_path = './libg729a.so'
    g729a_lib_path = PATH + "\\" + 'libg729a.so'
else:
    raise RuntimeError("Unknown OS")


class G729Acoder:
    SAMPLES_IN_FRAME = 80
    BYTES_IN_COMPRESSED_FRAME = 10
    def __init__(
        self, 
        f_stateSize: Callable[[], int], 
        f_init: Callable[[Any], int], 
        f_process: Callable[[Any, Any, Any], int],
        inputSize: int,
        outputSize: int
    ) -> None:
        self._state = (ctypes.c_byte * f_stateSize())()
        if f_init(self._state) != 0:
            raise RuntimeError("G729 init state function " + f_init.__name__ + " returned error")
        self._f_process = f_process
        self.inputSize = inputSize
        self.outputSize = outputSize

    def process(self, input: bytearray) -> bytearray:
        if len(input) != self.inputSize:
            raise RuntimeError("G729: incorrect input size in process(). Expected: " + str(self.inputSize) +". Got: " + str(len(input)))
        inData = (ctypes.c_byte * len(input))(*input)
        outData = (ctypes.c_byte * self.outputSize)()
        if self._f_process(self._state, inData, outData) != 0:
            raise RuntimeError("G729 process function " + self._f_process.__name__ + " returned error")
        return bytearray(outData)


class G729Aencoder(G729Acoder):
    def __init__(self) -> None:
        g729aLib = ctypes.CDLL(g729a_lib_path)
        super().__init__(
            g729aLib.G729A_Encoder_Get_Size,
            g729aLib.G729A_Encoder_Init,
            g729aLib.G729A_Encoder_Process,
            self.SAMPLES_IN_FRAME*2,
            self.BYTES_IN_COMPRESSED_FRAME
        )


class G729Adecoder(G729Acoder):
    def __init__(self) -> None:
        g729aLib = ctypes.CDLL(g729a_lib_path)
        super().__init__(
            g729aLib.G729A_Decoder_Get_Size,
            g729aLib.G729A_Decoder_Init,
            g729aLib.G729A_Decoder_Process,
            self.BYTES_IN_COMPRESSED_FRAME,
            self.SAMPLES_IN_FRAME*2
        )


def convert_wav_to_g729(coder: G729Acoder, infile_path: str, outfile_path: str) -> None:
    with open(infile_path, 'rb') as infile, open(outfile_path, 'wb') as outfile:
        while True:
            buff = infile.read(coder.inputSize)
            if not buff:
                # End of file
                break
            if len(buff) < coder.inputSize:
                # Handle partial frame - pad with zeros
                buff = buff.ljust(coder.inputSize, b'\0')
            processed_data = coder.process(bytearray(buff))
            outfile.write(processed_data)
    print('Done.')


def write_pcm_to_wav(pcm_data: bytes, sample_rate: int, num_channels: int, sample_width: int, wav_file_path: str):
    with wave.open(wav_file_path, 'wb') as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data)


def convert_g729_to_wav(g729_decoder: G729Adecoder, g729_file_path: str, wav_file_path: str):
    pcm_data = bytearray()
    with open(g729_file_path, 'rb') as g729_file:
        while True:
            input_data = g729_file.read(g729_decoder.inputSize)
            if not input_data:
                break
            output_data = g729_decoder.process(bytearray(input_data))
            pcm_data.extend(output_data)
    write_pcm_to_wav(pcm_data, sample_rate=8000, num_channels=1, sample_width=2, wav_file_path=wav_file_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4 or (sys.argv[1] != 'encode' and sys.argv[1] != 'decode'):
        print('Usage: ./' + sys.argv[0] + ' encode/decode in_file out_file')
        exit(0)

    coder = G729Aencoder() if sys.argv[1] == 'encode' else G729Adecoder() # type: G729Acoder
    
    with open(sys.argv[2], 'rb') as infile, open(sys.argv[3], 'wb') as outfile:
        while True:
            buff = infile.read(coder.inputSize)
            if len(buff) < coder.inputSize:
                break
            outfile.write(coder.process(bytearray(buff)))
    print('Done.')