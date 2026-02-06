from typing import Protocol, Any, List
from abc import ABC, abstractmethod


class ProcessingStage(Protocol):
    def process(self, data: Any) -> Any:
        ...


class ProcessingPipeline(ABC):
    def __init__(self, pipeline_id: str):
        self.stages: List[ProcessingStage] = []
        self.pipeline_id = pipeline_id

    @abstractmethod
    def process(self, data: Any) -> Any:
        ...

    def add_stage(self, stage: Any) -> None:
        self.stages.append(stage)

    def run(self, data: Any) -> None:
        res = data
        for p in self.stages:
            res = p.process(res)
        return res


class InputStage:
    def process(self, data: Any) -> dict:
        if not data:
            raise ValueError("Input data error")
        if isinstance(data, str):
            res = {}
            words = data.split()
            for i in range(0, len(words), 2):
                if i + 1 < len(words):
                    key = words[i]
                    val = words[i + 1]
                    res[key] = val
            return res
        elif isinstance(data, list):
            res = {data[i]: data[i + 1] for i in range(0, len(data), 2)}
            return res
        return data


class TransformStage:
    def process(self, data: Any) -> dict:
        if not data:
            raise ValueError("Transform data error")
        return data


class OutputStage:
    def process(self, data: Any) -> str:
        if not data:
            raise ValueError("Output data error")
        return f"Processed {data}"


class JsonAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str):
        super().__init__(pipeline_id)
    ...


class CsvAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str):
        super().__init__(pipeline_id)
    ...


class StreamAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str):
        super().__init__(pipeline_id)
    ...


class NexusManager:
    def add_pipeline():
        ...
    ...


if __name__ == "__main__":
    ...
