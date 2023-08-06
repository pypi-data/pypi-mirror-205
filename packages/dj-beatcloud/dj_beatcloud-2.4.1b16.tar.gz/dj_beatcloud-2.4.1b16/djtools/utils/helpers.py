"""This module contains helper functions that are not specific to any
particular subpackage of this library.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from itertools import product
import logging
import logging.config
import os
from pathlib import Path
from subprocess import check_output
import tempfile
from typing import Any, AsyncGenerator, Dict, List, Optional, Set, Tuple
from unittest import mock

from fuzzywuzzy import fuzz
import spotipy
from tqdm import tqdm

from configs.config import BaseConfig
from spotify.helpers import get_playlist_ids, get_spotify_client


logger = logging.getLogger(__name__)


class MockOpen:
    builtin_open = open

    def __init__(
        self,
        files: List[str],
        user_a: Optional[Tuple[str]] = None,
        user_b: Optional[Tuple[str]] = None,
        content: Optional[str] = "",
        write_only: Optional[bool] = False,
    ):
        self._user_a = user_a 
        self._user_b = user_b 
        self._files = files
        self._content = content
        self._write_only = write_only

    def open(self, *args, **kwargs):
        file_name = os.path.basename(args[0])
        if file_name in self._files:
            if "w" in kwargs.get("mode"):
                return tempfile.TemporaryFile(mode=kwargs["mode"])
            elif not self._write_only:
                return self._file_strategy(file_name, *args, **kwargs)
        return self.builtin_open(*args, **kwargs)
    
    def _file_strategy(self, file_name, *args, **kwargs):
        if self._content:
            data = self._content
        elif file_name == "registered_users.yaml":
            data = (
                f'{{"{self._user_a[0]}": "{self._user_a[1]}", '
                f'"{self._user_b[0]}": "{self._user_b[1]}"}}'
            )
        else:
            data = "{}"

        return mock.mock_open(read_data=data)(*args, **kwargs)


def add_tracks(result: Dict[str, Any]) -> List[str]:
    """Parses a page of Spotify API result tracks and returns a list of the
        track titles and artist names.

    Args:
        result: Paged result of Spotify tracks.

    Returns:
        Spotify track titles and artist names.
    """
    tracks = []
    for track in result["items"]:
        title = track["track"]["name"]
        artists = ", ".join([y["name"] for y in track["track"]["artists"]])
        tracks.append(f"{title} - {artists}")

    return tracks


async def catch(generator: AsyncGenerator, message: Optional[str] = "") -> Any:
    """This function permits one-line try/except logic for comprehensions.

    Args:
        generator: Async generator.
        message: Prefix message for logger warning.

    Returns:
        Return of the AsyncGenerator.
    """
    while True:
        try:
            yield await generator.__anext__()
        except StopAsyncIteration:
            return
        except Exception as exc:
            logger.warning(f"{message}: {exc}" if message else exc)
            continue


def compute_distance(
    spotify_playlist: str,
    spotify_track: str,
    beatcloud_track: str,
    threshold: float,
) -> Tuple[str, float]:
    """Qualifies a match between a Spotify track and a beatcloud track using
        Levenshtein similarity.

    Args:
        spotify_playlist: Playlist that Spotify track belongs to.
        spotify_track: Spotify track title and artist name.
        beatcloud_track: Beatcloud track title and artist name
        threshold: Levenshtein similarity threshold for acceptance.

    Returns:
        Tuple of Spotify playlist, Spotify "TRACK TITLE - ARTIST NAME",
            beatcloud "TRACK TITLE - ARTIST NAME", Levenshtein similarity.
    """
    fuzz_ratio = fuzz.ratio(spotify_track, beatcloud_track)
    if fuzz_ratio >= threshold:
        return spotify_playlist, spotify_track, beatcloud_track, fuzz_ratio


def find_matches(
    spotify_tracks: Dict[str, Set[str]],
    beatcloud_tracks: List[str],
    config: BaseConfig,
) -> List[Tuple[str, float]]:
    """Computes the Levenshtein similarity between the product of all beatcloud
        tracks with all the tracks in the given Spotify playlist(s) and returns
        those that match above a threshold.

    Args:
        spotify_tracks: Spotify track titles and artist names.
        beatcloud_tracks: Beatcloud track titles and artist names.
        config: Configuration object.

    Returns:
        List of tuples of Spotify playlist, Spotify track, Beatcloud track, andl
            Levenshtein distance.
    """
    spotify_tracks = [
        (playlist, track) for playlist, tracks in spotify_tracks.items()
        for track in tracks
    ]
    _product = list(product(spotify_tracks, beatcloud_tracks))
    _temp, beatcloud_tracks = zip(*_product)
    spotify_playlists, spotify_tracks = zip(*_temp)
    fuzz_ratio = config.CHECK_TRACKS_FUZZ_RATIO
    payload = [
        spotify_playlists,
        spotify_tracks,
        beatcloud_tracks,
        [fuzz_ratio] * len(_product),
    ]
    with ThreadPoolExecutor(max_workers=os.cpu_count() * 4) as executor:
        matches = list(
            filter(
                None,
                tqdm(
                    executor.map(compute_distance, *payload),
                    total=len(_product),
                    desc="Matching new and Beatcloud tracks",
                )
            )
        )

    return matches


def get_beatcloud_tracks() -> List[str]:
    """Lists all the music files in S3 and parses out the track titles and
        artist names.
    
    Returns:
        Beatcloud track titles and artist names.
    """
    logger.info("Getting tracks from the beatcloud...")
    cmd = "aws s3 ls --recursive s3://dj.beatcloud.com/dj/music/"
    output = check_output(cmd, shell=True).decode("utf-8").split("\n")
    tracks = [Path(track) for track in output if track]
    logger.info(f"Got {len(tracks)} tracks")

    return tracks


def get_local_tracks(config: BaseConfig) -> Dict[str, List[str]]:
    """Aggregates the files from one or more local directories in a dictionary
        mapped with parent directories.

    Args:
        config: Configuration object.

    Returns:
        Local file names keyed by parent directory.
    """
    local_dir_tracks = {}
    for _dir in config.CHECK_TRACKS_LOCAL_DIRS:
        if not _dir.exists():
            logger.warning(
                f"{_dir} does not exist; will not be able to check its "
                "contents against the beatcloud"
            )
            continue
        files = _dir.rglob("**/*.*")
        local_dir_tracks[_dir] = [_file.stem for _file in files]

    return local_dir_tracks


def get_playlist_tracks(
    spotify: spotipy.Spotify, playlist_id: str
) -> Set[str]:
    """Queries Spotify API for a playlist and pulls tracks from it.

    Args:
        spotify: Spotify client.
        playlist_id: Playlist ID of Spotify playlist to pull tracks from.

    Raises:
        RuntimeError: Playlist_id must correspond with a valid Spotify playlist.

    Returns:
        Spotify track titles and artist names from a given playlist.
    """
    try:
        playlist = spotify.playlist(playlist_id)
    except Exception:
        raise RuntimeError(
            f"Failed to get playlist with ID {playlist_id}"
        ) from Exception

    result = playlist["tracks"]
    tracks = add_tracks(result)

    while result["next"]:
        result = spotify.next(result)
        tracks.extend(add_tracks(result))

    return set(tracks)


def get_spotify_tracks(config: BaseConfig) -> Dict[str, Set[str]]:
    """Aggregates the tracks from one or more Spotify playlists into a
        dictionary mapped with playlist names.

    Args:
        config: Configuration object.
    
    Returns:
        Spotify track titles and artist names keyed by playlist name.
    """
    spotify = get_spotify_client(config)
    playlist_ids = get_playlist_ids()

    playlist_tracks = {}
    for playlist in config.CHECK_TRACKS_SPOTIFY_PLAYLISTS:
        playlist_id = playlist_ids.get(playlist)
        if not playlist_id:
            logger.error(f"{playlist} not in spotify_playlists.yaml")
            continue

        logger.info(f'Getting tracks from Spotify playlist "{playlist}"...')
        playlist_tracks[playlist] = get_playlist_tracks(spotify, playlist_id)
        length = len(playlist_tracks[playlist])
        logger.info(f"Got {length} track{'' if length == 1 else 's'}")

        if config.VERBOSITY > 0:
            for track in playlist_tracks[playlist]:
                logger.info(f"\t{track}")

    return playlist_tracks


def initialize_logger() -> Tuple[logging.Logger, str]:
    """Initializes logger from configuration.

    Returns:
        Tuple containing Logger and associated log file.
    """
    log_file = (
        Path(__file__).parent.parent / "logs" /
        f'{datetime.now().strftime("%Y-%m-%d")}.log'
    )
    log_conf = Path(__file__).parent.parent / "configs" / "logging.conf"
    logging.config.fileConfig(
        fname=log_conf,
        # NOTE(a-rich): the `logfilename` needs a unix-style path.
        defaults={"logfilename": log_file.as_posix()},
        disable_existing_loggers=False,
    )

    return logging.getLogger(__name__), log_file


def mock_exists(files, path):
    for file_name, exists in files:
        if file_name == path.name:
            return exists

    return True
