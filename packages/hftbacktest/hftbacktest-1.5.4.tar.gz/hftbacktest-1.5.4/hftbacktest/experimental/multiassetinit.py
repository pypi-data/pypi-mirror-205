from typing import Union, List, Optional

import numpy as np
import pandas as pd
from numba import boolean, int64, typeof, ListType
from numba.experimental import jitclass

from .assettype import (
    LinearAsset as LinearAsset_,
    InverseAsset as InverseAsset_,
)
from .backtest import SingleAssetHftBacktest as SingleAssetHftBacktest_
from .data import (
    merge_on_local_timestamp,
    validate_data,
    correct_local_timestamp,
    correct_exch_timestamp,
    correct_exch_timestamp_adjust,
    correct,
)
from .marketdepth import MarketDepth
from .models.latencies import (
    FeedLatency as FeedLatency_,
    ConstantLatency as ConstantLatency_,
    ForwardFeedLatency as ForwardFeedLatency_,
    BackwardFeedLatency as BackwardFeedLatency_,
    IntpOrderLatency as IntpOrderLatency_
)
from .models.queue import (
    RiskAverseQueueModel as RiskAverseQueueModel_,
    LogProbQueueModel as LogProbQueueModel_,
    IdentityProbQueueModel as IdentityProbQueueModel_,
    SquareProbQueueModel as SquareProbQueueModel_
)
from .order import BUY, SELL, NONE, NEW, EXPIRED, FILLED, CANCELED, GTC, GTX, Order, OrderBus
from .proc.local import Local
from .proc.nopartialfillexchange import NoPartialFillExchange
from .proc.partialfillexchange import PartialFillExchange
from .reader import (
    COL_EVENT,
    COL_EXCH_TIMESTAMP,
    COL_LOCAL_TIMESTAMP,
    COL_SIDE,
    COL_PRICE,
    COL_QTY,
    DEPTH_EVENT,
    DEPTH_CLEAR_EVENT,
    DEPTH_SNAPSHOT_EVENT,
    TRADE_EVENT,
    DataReader,
    Cache
)
from .stat import Stat
from .state import State
from .typing import (
    Data,
    ExchangeModelInitiator,
    AssetType,
    OrderLatencyModel,
    QueueModel,
    DataCollection,
    HftBacktestType
)


# JIT'ed latency models
ConstantLatency = jitclass()(ConstantLatency_)
FeedLatency = jitclass()(FeedLatency_)
ForwardFeedLatency = jitclass()(ForwardFeedLatency_)
BackwardFeedLatency = jitclass()(BackwardFeedLatency_)
IntpOrderLatency = jitclass()(IntpOrderLatency_)

# JIT'ed queue models
RiskAverseQueueModel = jitclass()(RiskAverseQueueModel_)
LogProbQueueModel = jitclass()(LogProbQueueModel_)
IdentityProbQueueModel = jitclass()(IdentityProbQueueModel_)
SquareProbQueueModel = jitclass()(SquareProbQueueModel_)

# JIT'ed asset types
LinearAsset = jitclass()(LinearAsset_)
InverseAsset = jitclass()(InverseAsset_)

Linear = LinearAsset()
Inverse = InverseAsset()

# JIT'ed HftBacktest
def MultiAssetHftBacktest(locals, exchs):
    jitted = jitclass(spec=[
        ('run', boolean),
        ('current_timestamp', int64),
        ('locals', typeof(locals)),
        ('exchs', typeof(exchs)),
    ])(MultiAssetHftBacktest_)
    return jitted(locals, exchs)


class Asset:
    data: DataCollection
    tick_size: float
    lot_size: float
    maker_fee: float
    taker_fee: float


def HftBacktest(
        asset: List[Asset],
        order_latency: OrderLatencyModel,
        asset_type: AssetType,
        queue_model: Optional[QueueModel] = None,
        snapshot: Optional[Data] = None,
        start_position: float = 0,
        start_balance: float = 0,
        start_fee: float = 0,
        trade_list_size: int = 0,
        exchange_model: ExchangeModelInitiator = None
):
    r"""
    Create a HftBacktest instance.

    Args:
        data: Data to be fed.
        tick_size: Minimum price increment for the given asset.
        lot_size: Minimum order quantity for the given asset.
        maker_fee: Maker fee rate; a negative value indicates rebates.
        taker_fee: Taker fee rate; a negative value indicates rebates.
        order_latency: Order latency model. See :doc:`Order Latency Models <order_latency_models>`.
        asset_type: Either ``Linear`` or ``Inverse``. See :doc:`Asset types <asset_types>`.
        queue_model: Queue model with default set as :class:`.models.queue.RiskAverseQueueModel`. See :doc:`Queue Models <queue_models>`.
        snapshot: The initial market depth snapshot.
        start_position: Starting position.
        start_balance: Starting balance.
        start_fee: Starting cumulative fees.
        trade_list_size: Buffer size for storing market trades; the default value of ``0`` indicates that market trades
                         will not be stored in the buffer.
        exchange_model: Exchange model with default set as ``NoPartialFillExchange``.

    Returns:
         JIT'ed :class:`.SingleAssetHftBacktest`
    """

    cache = Cache()

    if isinstance(data, list):
        local_reader = DataReader(cache)
        exch_reader = DataReader(cache)
        for item in data:
            if isinstance(item, str):
                local_reader.add_file(item)
                exch_reader.add_file(item)
            elif isinstance(item, pd.DataFrame) or isinstance(item, np.ndarray):
                local_reader.add_data(item)
                exch_reader.add_data(item)
            else:
                raise ValueError('Unsupported data type')
    elif isinstance(data, str):
        local_reader = DataReader(cache)
        local_reader.add_file(data)

        exch_reader = DataReader(cache)
        exch_reader.add_file(data)
    else:
        data = __load_data(data)
        local_reader = DataReader(cache)
        local_reader.add_data(data)

        exch_reader = DataReader(cache)
        exch_reader.add_data(data)

    if queue_model is None:
        queue_model = RiskAverseQueueModel()

    local_market_depth = MarketDepth(tick_size, lot_size)
    exch_market_depth = MarketDepth(tick_size, lot_size)

    if snapshot is not None:
        snapshot = __load_data(snapshot)
        local_market_depth.apply_snapshot(snapshot)
        exch_market_depth.apply_snapshot(snapshot)

    local_state = State(
        start_position,
        start_balance,
        start_fee,
        maker_fee,
        taker_fee,
        asset_type
    )
    exch_state = State(
        start_position,
        start_balance,
        start_fee,
        maker_fee,
        taker_fee,
        asset_type
    )

    exch_to_local_orders = OrderBus()
    local_to_exch_orders = OrderBus()

    local = Local(
        local_reader,
        local_to_exch_orders,
        exch_to_local_orders,
        local_market_depth,
        local_state,
        order_latency,
        trade_list_size
    )

    if exchange_model is None:
        exchange_model = NoPartialFillExchange

    exch = exchange_model(
        exch_reader,
        exch_to_local_orders,
        local_to_exch_orders,
        exch_market_depth,
        exch_state,
        order_latency,
        queue_model
    )

    return MultiAssetHftBacktest(locals, exchs)
