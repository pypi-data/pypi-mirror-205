import json
import os
import warnings
from typing import List, Tuple, Union, Callable
from itertools import chain
from .stabilization import valid_ts

__all__ = ['result_to_srt_vtt', 'result_to_ass', 'save_as_json', 'load_result']


def _save_as_file(content: str, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Saved: {os.path.abspath(path)}')


def _get_segments(result: (dict, list), min_dur: float, reverse_text: Union[bool, tuple] = False):
    if isinstance(result, dict):
        if reverse_text:
            warnings.warn(f'[reverse_text]=True only applies to WhisperResult but result is {type(result)}')
        return result.get('segments')
    elif not isinstance(result, list) and callable(getattr(result, 'segments_to_dicts', None)):
        return result.apply_min_dur(min_dur, inplace=False).segments_to_dicts(reverse_text=reverse_text)
    return result


def sec2hhmmss(seconds: (float, int)):
    mm, ss = divmod(seconds, 60)
    hh, mm = divmod(mm, 60)
    return hh, mm, ss


def sec2vtt(seconds: (float, int)) -> str:
    hh, mm, ss = sec2hhmmss(seconds)
    return f'{hh:0>2.0f}:{mm:0>2.0f}:{ss:0>6.3f}'


def sec2srt(seconds: (float, int)) -> str:
    return sec2vtt(seconds).replace(".", ",")


def sec2ass(seconds: (float, int)) -> str:
    hh, mm, ss = sec2hhmmss(seconds)
    return f'{hh:0>1.0f}:{mm:0>2.0f}:{ss:0>2.2f}'


def segment2vttblock(segment: dict, strip=True) -> str:
    return f'{sec2vtt(segment["start"])} --> {sec2vtt(segment["end"])}\n' \
           f'{segment["text"].strip() if strip else segment["text"]}'


def segment2srtblock(segment: dict, idx: int, strip=True) -> str:
    return f'{idx}\n{sec2srt(segment["start"])} --> {sec2srt(segment["end"])}\n' \
           f'{segment["text"].strip() if strip else segment["text"]}'


def segment2assblock(segment: dict, idx: int, strip=True) -> str:
    return f'Dialogue: {idx},{sec2ass(segment["start"])},{sec2ass(segment["end"])},Default,,0,0,0,,' \
           f'{segment["text"].strip() if strip else segment["text"]}'


def words2segments(words: List[dict], tag: Tuple[str, str], reverse_text: bool = False) -> List[dict]:
    def add_tag(idx: int):
        return ''.join(
            (
                f" {tag[0]}{w['word'][1:]}{tag[1]}"
                if w['word'].startswith(' ') else
                f"{tag[0]}{w['word']}{tag[1]}"
            )
            if w['word'] not in ('', ' ') and idx_ == idx else
            w['word']
            for idx_, w in idx_filled_words
        )

    filled_words = []
    for i, word in enumerate(words):
        curr_end = round(word['end'], 3)
        filled_words.append(dict(word=word['word'], start=round(word['start'], 3), end=curr_end))
        if word != words[-1]:
            next_start = round(words[i + 1]['start'], 3)
            if next_start - curr_end != 0:
                filled_words.append(dict(word='', start=curr_end, end=next_start))
    idx_filled_words = list(enumerate(filled_words))
    if reverse_text:
        idx_filled_words = list(reversed(idx_filled_words))

    segments = [dict(text=add_tag(i), start=filled_words[i]['start'], end=filled_words[i]['end'])
                for i in range(len(filled_words))]
    return segments


def to_word_level_segments(segments: List[dict], tag: Tuple[str, str]) -> List[dict]:
    return list(
        chain.from_iterable(
            words2segments(s['words'], tag, reverse_text=s.get('reversed_text'))
            for s in segments
        )
    )


def to_word_level(segments: List[dict]) -> List[dict]:
    return [dict(text=w['word'], start=w['start'], end=w['end']) for s in segments for w in s['words']]


def _confirm_word_level(segments: List[dict]) -> bool:
    if not all(bool(s.get('words')) for s in segments):
        warnings.warn('Result is missing word timestamps. Word-level timing cannot be exported. '
                      'Use "word_level=False" to avoid this warning')
        return False
    return True


def _preprocess_args(result: (dict, list),
                     segment_level: bool,
                     word_level: bool,
                     min_dur: float,
                     reverse_text: Union[bool, tuple] = False):
    assert segment_level or word_level, '`segment_level` or `word_level` must be True'
    segments = _get_segments(result, min_dur, reverse_text=reverse_text)
    if word_level:
        word_level = _confirm_word_level(segments)
    return segments, segment_level, word_level


def result_to_any(result: (dict, list),
                  filepath: str = None,
                  filetype: str = None,
                  segments2blocks: Callable = None,
                  segment_level=True,
                  word_level=True,
                  min_dur: float = 0.02,
                  tag: Tuple[str, str] = None,
                  default_tag: Tuple[str, str] = None,
                  strip=True,
                  reverse_text: Union[bool, tuple] = False):
    """

    Generate file from result to display segment-level and/or word-level timestamp.

    Returns
    -------
    string of content if no [filepath] is provided, else None

    """
    segments, segment_level, word_level = _preprocess_args(
        result, segment_level, word_level, min_dur, reverse_text=reverse_text
    )

    if filetype is None:
        filetype = os.path.splitext(filepath)[-1][1:] or 'srt'
    if filetype.lower() not in ('srt', 'vtt', 'ass', 'tsv'):
        raise NotImplementedError(f'{filetype} not supported')

    if filepath and not filepath.lower().endswith(f'.{filetype}'):
        filepath += f'.{filetype}'

    if word_level and segment_level:
        if tag is None:
            if default_tag is None:
                tag = ('<font color="#00ff00">', '</font>') if filetype == 'srt' else ('<u>', '</u>')
            else:
                tag = default_tag
        segments = to_word_level_segments(segments, tag)
    elif word_level:
        segments = to_word_level(segments)

    valid_ts(segments)

    if segments2blocks is None:
        sub_str = '\n\n'.join(segment2srtblock(s, i, strip=strip) for i, s in enumerate(segments))
    else:
        sub_str = segments2blocks(segments)

    if filepath:
        _save_as_file(sub_str, filepath)
    else:
        return sub_str


def result_to_srt_vtt(result: (dict, list),
                      filepath: str = None,
                      segment_level=True,
                      word_level=True,
                      min_dur: float = 0.02,
                      tag: Tuple[str, str] = None,
                      vtt: bool = None,
                      strip=True,
                      reverse_text: Union[bool, tuple] = False):
    """

    Generate SRT/VTT from result to display segment-level and/or word-level timestamp.

    Parameters
    ----------
    result: (dict, list)
        result from modified model
    filepath: str:
        path to save file. if no path is specified, the content will be returned as a str instead
    segment_level: bool:
        whether to use segment-level timestamps in output (default: True)
    word_level: bool
        whether to use word-level timestamps in output (default: True)
    min_dur: float
        minimum duration any word/segment is allowed to have. (default: 0.02)
        if the duration is less than this threshold, the word/segments will be merged with adjacent word/segments.
    tag: Tuple[str, str]
        tag used to change the properties a word at its timestamp
        SRT Default: '<font color="#00ff00">', '</font>'
        VTT Default: '<u>', '</u>'
    vtt: bool
        whether to output VTT (default: False if no [filepath] is specified, else determined by [filepath] extension)
    strip: bool
        whether to remove spaces before and after text on each segment for output (default: True)
    reverse_text: Union[bool, tuple]
        whether to reverse the order of words for each segment (default: False)
        or provide the [prepend_punctuations] and [append_punctuations] as tuple pair instead of True
        to match transcription settings (if True, the default punctuations will be used)
        Note: This will not fix RTL text not displaying tags properly which is an issue with video player.
                VLC seems to not suffer from this issue.

    Returns
    -------
    string of content if no [filepath] is provided, else None

    """
    is_srt = (filepath is None or not filepath.lower().endswith('.vtt')) if vtt is None else not vtt
    if is_srt:
        segments2blocks = None
    else:
        def segments2blocks(segments):
            return 'WEBVTT\n\n' + '\n\n'.join(segment2vttblock(s, strip=strip) for i, s in enumerate(segments))
    return result_to_any(
        result=result,
        filepath=filepath,
        filetype=('vtt', 'srt')[is_srt],
        segments2blocks=segments2blocks,
        segment_level=segment_level,
        word_level=word_level,
        min_dur=min_dur,
        tag=tag,
        strip=strip,
        reverse_text=reverse_text
    )


def result_to_ass(result: (dict, list),
                  filepath: str = None,
                  segment_level=True,
                  word_level=True,
                  min_dur: float = 0.02,
                  tag: Tuple[str, str] = None,
                  font: str = None,
                  font_size: int = 24,
                  strip=True,
                  reverse_text: Union[bool, tuple] = False,
                  **kwargs):
    """

    Generate Advanced SubStation Alpha (ASS) file from result to display segment-level and/or word-level timestamp.

    Note: ass file is used in the same way as srt, vtt, etc.

    Parameters
    ----------
    result: (dict, list)
        result from modified model
    filepath: str:
        path to save file. if no path is specified, the content will be returned as a str instead
    segment_level: bool:
        whether to use segment-level timestamps in output (default: True)
    word_level: bool
        whether to use word-level timestamps in output (default: True)
    min_dur: float
        minimum duration any word/segment is allowed to have. (default: 0.02)
        if the duration is less than this threshold, the word/segments will be merged with adjacent word/segments.
    tag: Tuple[str, str]
        tag used to change the properties a word at its timestamp (default: '{\\1c&HFF00&}', '{\\r}')
    font: str
        word font (default: Arial)
    font_size: int
        word font size (default: 48)
    strip: bool
        whether to remove spaces before and after text on each segment for output (default: True)
    reverse_text: Union[bool, tuple]
        whether to reverse the order of words for each segment (default: False)
        or provide the [prepend_punctuations] and [append_punctuations] as tuple pair instead of True
        to match transcription settings (if True, the default punctuations will be used)
        Note: This will not fix RTL text not displaying tags properly which is an issue with video player.
                VLC seems to not suffer from this issue.
    kwargs:
        used for format styles:
        'Name', 'Fontname', 'Fontsize', 'PrimaryColour', 'SecondaryColour', 'OutlineColour', 'BackColour', 'Bold',
        'Italic', 'Underline', 'StrikeOut', 'ScaleX', 'ScaleY', 'Spacing', 'Angle', 'BorderStyle', 'Outline',
        'Shadow', 'Alignment', 'MarginL', 'MarginR', 'MarginV', 'Encoding'

    Returns
    -------
    string of content if no [filepath] is provided, else None

    """

    def segments2blocks(segments):
        fmt_style_dict = {'Name': 'Default', 'Fontname': 'Arial', 'Fontsize': '48', 'PrimaryColour': '&Hffffff',
                          'SecondaryColour': '&Hffffff', 'OutlineColour': '&H0', 'BackColour': '&H0', 'Bold': '0',
                          'Italic': '0', 'Underline': '0', 'StrikeOut': '0', 'ScaleX': '100', 'ScaleY': '100',
                          'Spacing': '0', 'Angle': '0', 'BorderStyle': '1', 'Outline': '1', 'Shadow': '0',
                          'Alignment': '2', 'MarginL': '10', 'MarginR': '10', 'MarginV': '10', 'Encoding': '0'}

        for k, v in filter(lambda x: 'colour' in x[0].lower() and not str(x[1]).startswith('&H'), kwargs.items()):
            kwargs[k] = f'&H{kwargs[k]}'

        fmt_style_dict.update((k, v) for k, v in kwargs.items() if k in fmt_style_dict)

        if font:
            fmt_style_dict.update(Fontname=font)
        if font_size:
            fmt_style_dict.update(Fontsize=font_size)

        fmts = f'Format: {", ".join(map(str, fmt_style_dict.keys()))}'

        styles = f'Style: {",".join(map(str, fmt_style_dict.values()))}'

        sub_str = f'[Script Info]\nScriptType: v4.00+\nPlayResX: 384\nPlayResY: 288\nScaledBorderAndShadow: yes\n\n' \
                  f'[V4+ Styles]\n{fmts}\n{styles}\n\n' \
                  f'[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n\n'

        sub_str += '\n'.join(segment2assblock(s, i, strip=strip) for i, s in enumerate(segments))

        return sub_str

    return result_to_any(
        result=result,
        filepath=filepath,
        filetype='ass',
        segments2blocks=segments2blocks,
        segment_level=segment_level,
        word_level=word_level,
        min_dur=min_dur,
        tag=tag,
        default_tag=(r'{\1c&' + 'HFF00&' + '}', r'{\r}'),
        strip=strip,
        reverse_text=reverse_text
    )


def save_as_json(result: dict, path: str):
    """
    Save result as json.
    """
    if not isinstance(result, dict) and callable(getattr(result, 'to_dict')):
        result = result.to_dict()
    if not path.lower().endswith('.json'):
        path += '.json'
    result = json.dumps(result, allow_nan=True)
    _save_as_file(result, path)


def load_result(json_path: str):
    """
    Load result saved as json.
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)
