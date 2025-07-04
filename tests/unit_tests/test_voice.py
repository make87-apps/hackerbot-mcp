################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.13
#
# This module contains the unit tests for the Base class.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################

import unittest
from unittest.mock import patch, MagicMock
from hackerbot.base import Base
import numpy as np

class TestHackerbotVoice(unittest.TestCase):
    @patch("builtins.print")
    @patch("numpy.frombuffer", return_value=np.array([1, 2, 3], dtype=np.int16))
    @patch("hackerbot.base.sd.OutputStream")
    @patch("hackerbot.base.PiperVoice.load")
    @patch("hackerbot.base.TTSHelper.get_or_download_model", return_value="/fake/model/path")
    def test_speak_success(self, mock_get_model, mock_load, mock_stream, mock_frombuffer, mock_print):
        base = Base(self.mock_controller)

        # Setup mock voice
        mock_voice = MagicMock()
        mock_voice.config.sample_rate = 22050
        mock_voice.synthesize_stream_raw.return_value = (b'\x00\x01' for _ in range(3))
        mock_load.return_value = mock_voice

        # Setup the stream mock with a write counter
        mock_stream_instance = MagicMock()

        write_call_counter = []

        def write_side_effect(data):
            write_call_counter.append(1)

        mock_stream_instance.write.side_effect = write_side_effect
        mock_stream.return_value.__enter__.return_value = mock_stream_instance

        # Run
        base.speak("dummy_model", "hello world")

        # Assert
        self.assertFalse(self.mock_controller.log_error.called)
        mock_print.assert_called_once_with("Finished speaking.")

    @patch("hackerbot.base.TTSHelper.get_or_download_model", return_value="/fake/model/path")
    @patch("hackerbot.base.PiperVoice.load", side_effect=Exception("load failed"))
    def test_speak_model_load_failure(self, mock_load, mock_get_model):
        base = Base(self.mock_controller)
        base.speak("bad_model", "test")
        self.mock_controller.log_error.assert_called_once()
        self.assertIn("Failed to load voice model", self.mock_controller.log_error.call_args[0][0])

    @patch("hackerbot.base.TTSHelper.get_or_download_model", return_value="/fake/model/path")
    @patch("hackerbot.base.sd.OutputStream", side_effect=Exception("stream init failed"))
    @patch("hackerbot.base.PiperVoice.load")
    def test_speak_stream_init_failure(self, mock_load, mock_stream, mock_get_model):
        mock_voice = MagicMock()
        mock_voice.config.sample_rate = 16000
        mock_load.return_value = mock_voice

        base = Base(self.mock_controller)

        base.speak("model", "test")
        self.mock_controller.log_error.assert_called_once()
        self.assertIn("Failed to initialize audio stream", self.mock_controller.log_error.call_args[0][0])

    @patch("hackerbot.base.TTSHelper.get_or_download_model", return_value="/fake/model/path")
    @patch("numpy.frombuffer", side_effect=Exception("conversion failed"))
    @patch("hackerbot.base.sd.OutputStream")
    @patch("hackerbot.base.PiperVoice.load")
    def test_speak_audio_conversion_failure(self, mock_load, mock_stream, mock_frombuffer, mock_get_model):
        mock_voice = MagicMock()
        mock_voice.config.sample_rate = 16000
        mock_voice.synthesize_stream_raw.return_value = [b'\x01\x02']

        mock_load.return_value = mock_voice
        base = Base(self.mock_controller)
        base.speak("model", "test")

        self.mock_controller.log_error.assert_any_call("Error writing audio data to stream: conversion failed")