from typing import List, Tuple, Optional
import enum
from math import modf
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json
import pandas as pd
import numpy as np

from redvox.common import date_time_utils as dtu
from redvox.common.errors import RedVoxExceptions, RedVoxError
from redvox.api1000.wrapped_redvox_packet.sensors.audio import AudioCodec
from redvox.api1000.wrapped_redvox_packet.sensors.location import LocationProvider
from redvox.api1000.wrapped_redvox_packet.sensors.image import ImageCodec
from redvox.api1000.wrapped_redvox_packet.station_information import NetworkType, PowerState, CellServiceState

# default maximum number of points required to brute force calculating gap timestamps
DEFAULT_MAX_BRUTE_FORCE_GAP_TIMESTAMPS: int = 5000
# percent of packet duration/sample rate required for gap to be considered a whole unit
DEFAULT_GAP_UPPER_LIMIT: float = 0.8
# percent of packet duration/sample rate required for gap to be considered nothing
DEFAULT_GAP_LOWER_LIMIT: float = 0.02
# columns for audio dataframe
AUDIO_DF_COLUMNS = ["timestamps", "unaltered_timestamps", "microphone"]
# columns that cannot be interpolated
NON_INTERPOLATED_COLUMNS = ["compressed_audio", "image"]
# columns that are not numeric but can be interpolated
NON_NUMERIC_COLUMNS = ["location_provider", "image_codec", "audio_codec",
                       "network_type", "power_state", "cell_service"]


# noinspection Mypy,DuplicatedCode
class DataPointCreationMode(enum.Enum):
    """
    Type of data point to create
    """

    NAN: int = 0
    COPY: int = 1
    INTERPOLATE: int = 2

    @staticmethod
    def list_names() -> List[str]:
        return [n.name for n in DataPointCreationMode]


@dataclass_json()
@dataclass
class GapPadResult:
    """
    The result of filling gaps or padding a time series
    """
    result_df: Optional[pd.DataFrame] = None
    gaps: List[Tuple[float, float]] = field(default_factory=lambda: [])
    errors: RedVoxExceptions = field(default_factory=lambda: RedVoxExceptions("GapPadResult"))

    def add_error(self, error: str):
        """
        add an error to the result
        :param error: error message to add
        """
        self.errors.append(error)


def calc_evenly_sampled_timestamps(
        start: float, samples: int, sample_interval_micros: float
) -> np.array:
    """
    given a start time, calculates samples amount of evenly spaced timestamps at rate_hz

    :param start: float, start timestamp in microseconds
    :param samples: int, number of samples
    :param sample_interval_micros: float, sample interval in microseconds
    :return: np.array with number of samples timestamps, evenly spaced starting at start
    """
    return start + (np.arange(0, samples) * sample_interval_micros)


def check_gap_list(gaps: List[Tuple[float, float]], start_timestamp: float = None,
                   end_timestamp: float = None) -> List[Tuple[float, float]]:
    """
    removes any gaps where end time <= start time, consolidates overlapping gaps, and ensures that no gap
    starts or ends before start_timestamp and starts or ends after end_timestamp.  All timestamps are in
    microseconds since epoch UTC

    :param gaps: list of gaps to check
    :param start_timestamp: lowest possible timestamp for a gap to start at
    :param end_timestamp: lowest possible timestamp for a gap to end at
    :return: list of correct, valid gaps
    """
    return_gaps: List[Tuple[float, float]] = []
    for gap in gaps:
        if start_timestamp:
            gap = (np.max([start_timestamp, gap[0]]), np.max([start_timestamp, gap[1]]))
        if end_timestamp:
            gap = (np.min([end_timestamp, gap[0]]), np.min([end_timestamp, gap[1]]))
        if gap[0] < gap[1]:
            if len(return_gaps) < 1:
                return_gaps.append(gap)
            for a, r_g in enumerate(return_gaps):
                if (gap[0] < r_g[0] and gap[1] < r_g[0]) or (gap[0] > r_g[1] and gap[1] > r_g[1]):
                    return_gaps.append(gap)
                    break
                else:
                    if gap[0] < r_g[0] < gap[1]:
                        r_g = (gap[0], r_g[1])
                    if gap[0] < r_g[1] < gap[1]:
                        r_g = (r_g[0], gap[1])
                    return_gaps[a] = r_g
    return return_gaps


def pad_data(
        expected_start: float,
        expected_end: float,
        data_df: pd.DataFrame,
        sample_interval_micros: float,
) -> pd.DataFrame:
    """
    Pad the start and end of the dataframe with np.nan

    :param expected_start: timestamp indicating start time of the data to pad from
    :param expected_end: timestamp indicating end time of the data to pad from
    :param data_df: dataframe with timestamps as column "timestamps"
    :param sample_interval_micros: constant sample interval in microseconds
    :return: dataframe padded with np.nans in front and back to meet full size of expected start and end
    """
    # extract the necessary information to pad the data
    data_time_stamps = data_df["timestamps"].to_numpy()
    first_data_timestamp = data_time_stamps[0]
    last_data_timestamp = data_time_stamps[-1]
    result_df = data_df.copy()
    result_before_update_length = len(result_df) - 1
    # FRONT/END GAP FILL!  calculate the samples missing based on inputs
    if expected_start < first_data_timestamp:
        start_diff = first_data_timestamp - expected_start
        num_missing_samples = int(start_diff / sample_interval_micros)
        if num_missing_samples > 0:
            # add the gap data to the result dataframe
            result_df = add_dataless_timestamps_to_df(
                result_df,
                0,
                sample_interval_micros,
                num_missing_samples,
                True
            )
    if expected_end > last_data_timestamp:
        last_diff = expected_end - last_data_timestamp
        num_missing_samples = int(last_diff / sample_interval_micros)
        if num_missing_samples > 0:
            # add the gap data to the result dataframe
            result_df = add_dataless_timestamps_to_df(
                result_df,
                result_before_update_length,
                sample_interval_micros,
                num_missing_samples
            )
    return result_df.sort_values("timestamps", ignore_index=True)


def fill_gaps(
        data_df: pd.DataFrame,
        gaps: List[Tuple[float, float]],
        sample_interval_micros: float,
        copy: bool = False
) -> pd.DataFrame:
    """
    fills gaps in the dataframe with np.nan or interpolated values by interpolating timestamps based on the
    calculated sample interval

    :param data_df: dataframe with timestamps as column "timestamps"
    :param gaps: list of tuples of known non-inclusive start and end timestamps of the gaps
    :param sample_interval_micros: known sample interval of the data points
    :param copy: if True, copy the data points, otherwise interpolate from edges, default False
    :return: dataframe without gaps
    """
    # extract the necessary information to compute gap size and gap timestamps
    data_time_stamps = data_df["timestamps"].to_numpy()
    if len(data_time_stamps) > 1:
        result_df = data_df.copy()
        data_duration = data_time_stamps[-1] - data_time_stamps[0]
        expected_samples = (np.floor(data_duration / sample_interval_micros)
                            + (1 if data_duration % sample_interval_micros >=
                               sample_interval_micros * DEFAULT_GAP_UPPER_LIMIT else 0)) + 1
        if expected_samples > len(data_time_stamps):
            if copy:
                pcm = DataPointCreationMode["COPY"]
            else:
                pcm = DataPointCreationMode["NAN"]
            # make it safe to alter the gap values
            my_gaps = check_gap_list(gaps, data_time_stamps[0], data_time_stamps[-1])
            for gap in my_gaps:
                # if timestamps are around gaps, we have to update the values
                before_start = np.argwhere([t <= gap[0] for t in data_time_stamps])
                after_end = np.argwhere([t >= gap[1] for t in data_time_stamps])
                if len(before_start) > 0:
                    before_start = before_start[-1][0]
                    # sim = gap[0] - data_time_stamps[before_start]
                    # result_df = add_data_points_to_df(result_df, before_start, sim, point_creation_mode=pcm)
                    gap = (data_time_stamps[before_start], gap[1])
                else:
                    before_start = None
                if len(after_end) > 0:
                    after_end = after_end[0][0]
                    # sim = gap[1] - data_time_stamps[after_end]
                    gap = (gap[0], data_time_stamps[after_end])
                else:
                    after_end = None
                num_new_points = int((gap[1] - gap[0]) / sample_interval_micros) - 1
                if before_start is not None:
                    result_df = add_data_points_to_df(result_df, before_start, sample_interval_micros,
                                                      num_new_points, pcm)
                elif after_end is not None:
                    result_df = add_data_points_to_df(result_df, after_end, -sample_interval_micros,
                                                      num_new_points, pcm)
        return result_df.sort_values("timestamps", ignore_index=True)
    return data_df


def fill_audio_gaps(
        packet_data: List[Tuple[float, np.array]],
        sample_interval_micros: float,
        gap_upper_limit: float = DEFAULT_GAP_UPPER_LIMIT,
        gap_lower_limit: float = DEFAULT_GAP_LOWER_LIMIT
) -> GapPadResult:
    """
    fills gaps in the dataframe with np.nan by interpolating timestamps based on the expected sample interval
      * ignores gaps with duration less than or equal to packet length * gap_lower_limit
      * converts gaps with duration greater than or equal to packet length * gap_upper_limit into a multiple of
        packet length

    :param packet_data: list of tuples, each tuple containing two pieces of packet information:
        * packet_start_timestamps: float of packet start timestamp in microseconds
        * audio_data: array of data points
    :param sample_interval_micros: sample interval in microseconds
    :param gap_upper_limit: percentage of packet length required to confirm gap is at least 1 packet,
                            default DEFAULT_GAP_UPPER_LIMIT
    :param gap_lower_limit: percentage of packet length required to disregard gap, default DEFAULT_GAP_LOWER_LIMIT
    :return: dataframe without gaps and the list of timestamps of the non-inclusive start and end of the gaps
    """
    result_array = [[], [], []]
    last_data_timestamp: Optional[float] = None
    gaps = []
    for packet in packet_data:
        samples_in_packet = len(packet[1])
        start_ts = packet[0]
        packet_length = sample_interval_micros * samples_in_packet
        if last_data_timestamp:
            last_data_timestamp += sample_interval_micros
            # check if start_ts is close to the last timestamp in data_timestamps
            last_timestamp_diff = start_ts - last_data_timestamp
            if last_timestamp_diff > gap_lower_limit * packet_length:
                fractional_packet, num_packets = modf(last_timestamp_diff /
                                                      (samples_in_packet * sample_interval_micros))
                if fractional_packet >= gap_upper_limit:
                    num_samples = samples_in_packet * (num_packets + 1)
                else:
                    num_samples = np.max([np.floor((fractional_packet + num_packets) * samples_in_packet), 1])
                gap_ts = calc_evenly_sampled_timestamps(last_data_timestamp, num_samples, sample_interval_micros)
                gap_array = [gap_ts, np.full(len(gap_ts), np.nan)]
                start_ts = gap_ts[-1] + sample_interval_micros
                gaps.append((last_data_timestamp, start_ts))
                result_array[0].extend(gap_array[0])
                result_array[1].extend(gap_array[0])
                result_array[2].extend(gap_array[1])
            elif last_timestamp_diff < -gap_lower_limit * packet_length:
                result = GapPadResult()
                result.add_error(f"Packet start timestamp: {dtu.microseconds_to_seconds(start_ts)} "
                                 f"is before last timestamp of previous "
                                 f"packet: {dtu.microseconds_to_seconds(last_data_timestamp)}")
                return result
        estimated_ts = calc_evenly_sampled_timestamps(start_ts, samples_in_packet, sample_interval_micros)
        last_data_timestamp = estimated_ts[-1]
        result_array[0].extend(estimated_ts)
        result_array[1].extend(estimated_ts)
        result_array[2].extend(packet[1])
    return GapPadResult(pd.DataFrame(np.transpose(result_array), columns=AUDIO_DF_COLUMNS), gaps)


def add_data_points_to_df(dataframe: pd.DataFrame,
                          start_index: int,
                          sample_interval_micros: float,
                          num_samples_to_add: int = 1,
                          point_creation_mode: DataPointCreationMode = DataPointCreationMode.COPY,
                          ) -> pd.DataFrame:
    """
    adds data points to the end of the dataframe, starting from the index specified.
        Note:
            * dataframe must not be empty
            * start_index must be non-negative and less than the length of dataframe
            * num_samples_to_add must be greater than 0
            * points are added onto the end and the result is not sorted
        Options for point_creation_mode are:
            * NAN: default values and nans
            * COPY: copies of the start data point
            * INTERPOLATE: interpolated values between start data point and adjacent point

    :param dataframe: dataframe to add dataless timestamps to
    :param start_index: index of the dataframe to use as starting point for creating new values
    :param sample_interval_micros: sample interval in microseconds of the timestamps; use negative values to
                                    add points before the start_index
    :param num_samples_to_add: the number of timestamps to create, default 1
    :param point_creation_mode: the mode of point creation to use
    :return: updated dataframe with synthetic data points
    """
    if len(dataframe) > start_index and len(dataframe) > 0 and num_samples_to_add > 0:
        start_timestamp = dataframe["timestamps"].iloc[start_index]
        t = start_timestamp + np.arange(1, num_samples_to_add + 1) * sample_interval_micros
        # interpolate mode only uses the first created timestamp
        if point_creation_mode == DataPointCreationMode.COPY:
            empty_df = dataframe.iloc[start_index].copy()
            for column_index in dataframe.columns:
                if column_index in NON_INTERPOLATED_COLUMNS:
                    empty_df[column_index] = np.nan
            empty_df["timestamps"] = t[0]
        elif point_creation_mode == DataPointCreationMode.INTERPOLATE:
            start_point = dataframe.iloc[start_index]
            numeric_start = start_point[[col for col in dataframe.columns
                                         if col not in NON_INTERPOLATED_COLUMNS + NON_NUMERIC_COLUMNS]]
            non_numeric_start = start_point[[col for col in dataframe.columns if col in NON_NUMERIC_COLUMNS]]
            end_point = dataframe.iloc[start_index + (1 if sample_interval_micros > 0 else -1)]
            numeric_end = end_point[[col for col in dataframe.columns
                                     if col not in NON_INTERPOLATED_COLUMNS + NON_NUMERIC_COLUMNS]]
            non_numeric_end = end_point[[col for col in dataframe.columns if col in NON_NUMERIC_COLUMNS]]
            if np.abs(start_point["timestamps"] - t[0]) <= np.abs(end_point["timestamps"] - t[0]):
                non_numeric_diff = non_numeric_start
            else:
                non_numeric_diff = non_numeric_end
            numeric_diff = numeric_end - numeric_start
            numeric_diff = \
                (numeric_diff / numeric_diff["timestamps"]) * \
                (t - numeric_start) + numeric_start
            empty_df = pd.concat([numeric_diff, non_numeric_diff])
        else:
            empty_df = pd.DataFrame(np.full([num_samples_to_add, len(dataframe.columns)], np.nan),
                                    columns=dataframe.columns)
            for column_index in dataframe.columns:
                if column_index == "timestamps":
                    empty_df[column_index] = t
                elif column_index == "location_provider":
                    empty_df[column_index] = [LocationProvider["UNKNOWN"].value for i in range(num_samples_to_add)]
                elif column_index == "image_codec":
                    empty_df[column_index] = [ImageCodec["UNKNOWN"].value for i in range(num_samples_to_add)]
                elif column_index == "audio_codec":
                    empty_df[column_index] = [AudioCodec["UNKNOWN"].value for i in range(num_samples_to_add)]
                elif column_index == "network_type":
                    empty_df[column_index] = [NetworkType["UNKNOWN_NETWORK"].value for i in range(num_samples_to_add)]
                elif column_index == "power_state":
                    empty_df[column_index] = [PowerState["UNKNOWN_POWER_STATE"].value
                                              for i in range(num_samples_to_add)]
                elif column_index == "cell_service":
                    empty_df[column_index] = [CellServiceState["UNKNOWN"].value for i in range(num_samples_to_add)]
        dataframe = dataframe.append(empty_df, ignore_index=True)

    return dataframe


def add_dataless_timestamps_to_df(dataframe: pd.DataFrame,
                                  start_index: int,
                                  sample_interval_micros: float,
                                  num_samples_to_add: int,
                                  add_to_start: bool = False,
                                  copy: bool = True,
                                  ) -> pd.DataFrame:
    """
    adds dataless timestamps directly to a dataframe that already contains data
      Note:
        * dataframe must not be empty
        * start_index must be non-negative and less than the length of dataframe
        * num_samples_to_add must be greater than 0
        * the points are added onto the end and the result is not sorted

    :param dataframe: dataframe to add dataless timestamps to
    :param start_index: index of the dataframe to use as starting point for creating new values
    :param sample_interval_micros: sample interval in microseconds of the timestamps
    :param num_samples_to_add: the number of timestamps to create
    :param add_to_start: if True, subtracts sample_interval_micros from start_timestamp, default False
    :param copy: if True, copy the value of the start point when creating new points, default True
    :return: updated dataframe with synthetic data points
    """
    if len(dataframe) > start_index and len(dataframe) > 0 and num_samples_to_add > 0:
        start_timestamp = dataframe["timestamps"].iloc[start_index]
        dataframe = dataframe.append(
            create_dataless_timestamps_df(start_timestamp, sample_interval_micros,
                                          dataframe.columns, num_samples_to_add, add_to_start),
            ignore_index=True)
    return dataframe


def create_dataless_timestamps_df(
        start_timestamp: float,
        sample_interval_micros: float,
        columns: pd.Index,
        num_samples_to_add: int,
        add_to_start: bool = False,
) -> pd.DataFrame:
    """
    Creates an empty dataframe with num_samples_to_add timestamps, using columns as the columns
    the first timestamp created is 1 sample_interval_s from the start_timestamp

    :param start_timestamp: timestamp in microseconds since epoch UTC to start calculating other timestamps from
    :param sample_interval_micros: fixed sample interval in microseconds since epoch UTC
    :param columns: dataframe the non-timestamp columns of the dataframe
    :param num_samples_to_add: the number of timestamps to create
    :param add_to_start: if True, subtracts sample_interval_s from start_timestamp, default False
    :return: dataframe with timestamps and no data
    """
    empty_df = pd.DataFrame(np.full([num_samples_to_add, len(columns)], np.nan), columns=columns)
    enum_samples = {
        "location_provider": LocationProvider["UNKNOWN"].value,
        "image_codec": ImageCodec["UNKNOWN"].value,
        "audio_codec": AudioCodec["UNKNOWN"].value,
        "network_type": NetworkType["UNKNOWN_NETWORK"].value,
        "power_state": PowerState["UNKNOWN_POWER_STATE"].value,
        "cell_service": CellServiceState["UNKNOWN"].value
    }
    if num_samples_to_add > 0:
        if add_to_start:
            sample_interval_micros = -sample_interval_micros
        t = start_timestamp + np.arange(1, num_samples_to_add + 1) * sample_interval_micros
        for column_index in columns:
            if column_index == "timestamps":
                empty_df[column_index] = t
            elif column_index in enum_samples.keys():
                empty_df[column_index] = [enum_samples[column_index] for i in range(num_samples_to_add)]
            # elif column_index == "location_provider":
            #     empty_df[column_index] = [LocationProvider.UNKNOWN for i in range(num_samples_to_add)]
            # elif column_index == "image_codec":
            #     empty_df[column_index] = [ImageCodec.UNKNOWN for i in range(num_samples_to_add)]
            # elif column_index == "audio_codec":
            #     empty_df[column_index] = [AudioCodec.UNKNOWN for i in range(num_samples_to_add)]
            # elif column_index == "network_type":
            #     empty_df[column_index] = [NetworkType.UNKNOWN_NETWORK for i in range(num_samples_to_add)]
            # elif column_index == "power_state":
            #     empty_df[column_index] = [PowerState.UNKNOWN_POWER_STATE for i in range(num_samples_to_add)]
            # elif column_index == "cell_service":
            #     empty_df[column_index] = [CellServiceState.UNKNOWN for i in range(num_samples_to_add)]
    return empty_df
