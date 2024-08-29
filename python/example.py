from g729a import *


def wav_to_g729(wav_file_path, g729_file_path):
    # 创建 G.729 编码器
    encoder = G729Aencoder()

    convert_wav_to_g729(encoder, wav_file_path, g729_file_path)


def g729_to_wav(g729_file_path, wav_file_path):
    # 创建 G.729 解码器
    decoder = G729Adecoder()

    convert_g729_to_wav(decoder, g729_file_path, wav_file_path)


# g729_to_wav('outputs/output.g729', 'inputs/input1.wav')
wav_to_g729('inputs/input.wav', 'outputs/output1.g729')

