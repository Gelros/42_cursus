from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):
    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria == "critical":
            return self.filter_high_priority(data_batch)
        return [item for item in data_batch if item is not None]

    @abstractmethod
    def filter_high_priority(self, data_batch: List[Any]) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"id": self.stream_id}


class SensorStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.name: str = "sensor batch"
        self.type: str = "Environmental Data"
        self.n: int = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            read: List[float] = [
                float(val) for x, val in data_batch if isinstance(
                    val, (int, float)
                    )
                ]
            avg: float = 0
            for x, val in data_batch:
                if x == "temp":
                    avg = val
            len_ope: int = len(read)
            self.n = len_ope
            res: str = f"{len_ope} readings processed, avg temp: {avg:.1f}°C"
            return f"Sensor analysis: {res}"
        except Exception as e:
            return f"Error in SensorStream: {e}"

    def filter_high_priority(self, data_batch: List[Any]) -> List[Any]:
        critical: List[Any] = []
        for action, val in data_batch:
            if action == "temp" and val > 25:
                critical.append(action)
            elif action == "humidity" and val > 60 or val < 20:
                critical.append(action)
            elif action == "pressure" and val > 1000:
                critical.append(action)
        return critical


class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.name: str = "transaction batch"
        self.type: str = "Financial Data"
        self.n: int = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            sum_buy: int = sum(
                val for action, val in data_batch if action == "buy"
                )
            sum_sell: int = sum(
                val for action, val in data_batch if action == "sell"
                )
            gain: int = sum_sell - sum_buy
            len_ope: int = sum(1 for action, val in data_batch)
            net: str = f" net flow: {gain} units"
            self.n = len_ope
            return f"Transaction analysis: {len_ope} operations,{net}"
        except Exception as e:
            return f"Error in Transaction stream: {e}"

    def filter_high_priority(self, data_batch: List[Any]) -> List[Any]:
        return [(action, val) for action, val in data_batch if val > 100]


class EventStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.name: str = "event batch"
        self.type: str = "System Events"
        self.n: int = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            len_op: int = len(data_batch)
            n_err: int = sum(1 for x in data_batch if x == "error")
            self.n = len_op
            return f"Event analysis: {len_op} events, {n_err} error detected"
        except Exception as e:
            return f"Error in Event stream: {e}"

    def filter_high_priority(self, data_batch: List[Any]) -> List[Any]:
        return [event for event in data_batch if event == "error"]


class StreamProcessor():
    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        if isinstance(stream, DataStream):
            self.streams.append(stream)

    def run(self, all_data: Dict[str, Any]) -> None:
        for data in self.streams:
            get_data: List[Any] = all_data.get(data.stream_id, [])
            print()
            print(f"Initializing {data.__class__.__name__}...")
            print(f"Stream ID: {data.stream_id}, Type: {data.type}")
            if not isinstance(data, EventStream):
                formatted: str = ', '.join(
                    [f"{action}:{val}" for action, val in get_data]
                    )
                print(f"Processing {data.name}: [{formatted}]")
            else:
                print(
                    f"Processing {data.name}: {all_data.get(data.stream_id)}"
                    )

            print(data.process_batch(get_data))

    def process_polymorphic_batch(self, all_data: Dict[str, Any],
                                  batch_number: int = 1) -> None:
        print("\n=== Polymorphic Stream Processing ===")
        print("Processing mixed stream types through unified interface...")

        res: List[str] = []
        print(f"\nBatch {batch_number} Results:")
        for data in self.streams:
            get_data: List[Any] = all_data.get(data.stream_id, [])
            data.process_batch(get_data)
            if isinstance(data, SensorStream):
                res.append(f"- Sensor data: {data.n} readings processed")
            elif isinstance(data, TransactionStream):
                res.append(
                    f"- Transaction data: {data.n} operations processed"
                    )
            elif isinstance(data, EventStream):
                res.append(f"- Event data: {data.n} events processed")

        for p in res:
            print(p)

        print("\nStream filtering active: High-priority data only")
        crit: List[str] = []
        for data in self.streams:
            get_data: List[Any] = all_data.get(data.stream_id, [])
            prio: List[Any] = data.filter_data(get_data, "critical")

            if isinstance(data, SensorStream) and prio:
                crit.append(f"{len(prio)} critical sensor alerts")
            elif isinstance(data, TransactionStream) and prio:
                crit.append(f"{len(prio)} large transaction")
            elif isinstance(data, EventStream) and prio:
                crit.append(f"{len(prio)} error")
        print(f"Filtered results: {', '.join(crit)}")

        print(
            "\nAll streams processed successfully. Nexus throughput optimal."
            )


if __name__ == "__main__":
    manager: StreamProcessor = StreamProcessor()

    sensor: SensorStream = SensorStream("SENSOR_001")
    trans: TransactionStream = TransactionStream("TRANS_001")
    event: EventStream = EventStream("EVENT_001")
    manager.add_stream(sensor)
    manager.add_stream(trans)
    manager.add_stream(event)
    data: Dict[str, List[Any]] = {
        "SENSOR_001": [("temp", 20), ("humidity", 65), ("pressure", 1013)],
        "TRANS_001": [("buy", 100), ("sell", 150), ("buy", 75)],
        "EVENT_001": ["login", "error", "logout"]
    }

    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    manager.run(data)

    manager.process_polymorphic_batch(data, 1)
