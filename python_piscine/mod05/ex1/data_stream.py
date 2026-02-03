from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):
    def __init__(self, stream_id: str):
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        return [item for item in data_batch if item is not None]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"id": self.stream_id}


class SensorStream(DataStream):
    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            read = [float(x) for x in data_batch if isinstance(x, (int, float))]
            avg = sum(x for x in read) / len(read) if read else 0
            res = f"{len(read)} readings processed, avg temp: {avg}°C"
            return f"Sensor analysis: {res}"
        except Exception as e:
            return f"Error in SensorStream {e}"


class TransactionStream(DataStream):
    pass


class EventStream(DataStream):
    pass


class StreamProcessor():
    def __init__(self):
        self.streams = []

    def add_stream(self, stream: DataStream) -> None:
        if isinstance(stream, DataStream):
            self.stream.append(stream)

    def run(self, all_data: Dict(str, List[Any])) -> None:
        for data in self.streams:
            get_data = all_data.get(data.stream_id, [])
            res = data.process_batch(get_data)
            print(res)


if __name__ == "__main__":
    manager = StreamProcessor()

    sensor = SensorStream("SENSOR_001")
    manager.add_stream(sensor)
    data = {
        "SENSOR_001": [10, 25, 36]
        }
    manager.run(data)
