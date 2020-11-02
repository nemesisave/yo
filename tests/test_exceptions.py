# -*- coding: utf-8 -*-
import pytest
from unittest import mock

from pytube import YouTube
from pytube.exceptions import LiveStreamError
from pytube.exceptions import RegexMatchError
from pytube.exceptions import VideoUnavailable
from pytube.exceptions import VideoPrivate


def test_video_unavailable():
    try:
        raise VideoUnavailable(video_id="YLnZklYFe7E")
    except VideoUnavailable as e:
        assert e.video_id == "YLnZklYFe7E"  # noqa: PT017
        assert str(e) == "YLnZklYFe7E is unavailable"


def test_regex_match_error():
    try:
        raise RegexMatchError(caller="hello", pattern="*")
    except RegexMatchError as e:
        assert str(e) == "hello: could not find match for *"


def test_live_stream_error():
    try:
        raise LiveStreamError(video_id="YLnZklYFe7E")
    except LiveStreamError as e:
        assert e.video_id == "YLnZklYFe7E"  # noqa: PT017
        assert str(e) == "YLnZklYFe7E is streaming live and cannot be loaded"


def test_private_error():
    try:
        raise VideoPrivate('mRe-514tGMg')
    except VideoPrivate as e:
        assert e.video_id == 'mRe-514tGMg'
        assert str(e) == 'mRe-514tGMg is a private video'


def test_raises_video_private(private):
    with pytest.raises(VideoPrivate):
        with mock.patch('pytube.request.urlopen') as mock_url_open:
            # Mock the responses to YouTube
            mock_url_open_object = mock.Mock()
            mock_url_open_object.read.side_effect = [
                private['watch_html'].encode('utf-8'),
            ]
            mock_url_open.return_value = mock_url_open_object
            YouTube('https://youtube.com/watch?v=mRe-514tGMg')
