from typing import Protocol, Any, List, Union, Dict
from abc import ABC, abstractmethod
import time


class ProcessingStage(Protocol):
    def process(self, data: Any) -> Any:
        ...


class ProcessingPipeline(ABC):
    def __init__(self, pipeline_id: str):
        self.stages: List[ProcessingStage] = []
        self.pipeline_id = pipeline_id
        self.errors: List[str] = []
        self.procces_time: float = 0.0
        self.record_processed: int = 0

    @abstractmethod
    def process(self, data: Any) -> Any:
        ...

    def add_stage(self, stage: Any) -> None:
        self.stages.append(stage)

    def run(self, data: Any) -> None:
        s_time = time.time()
        res = data
        try:
            for p in self.stages:
                res = p.process(res)
            self.record_processed += 1
        except Exception as e:
            self.errors.append(f"Error pipeline {self.pipeline_id}: {e}")
            raise
        finally:
            self.procces_time = time.time() - s_time
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
        if data["sensor"]:
            val = data["value"]
            unit = data["unit"]
            return f"Processed temperature reading: {val}°{unit} (NormalRange)"
        return f"{data}"


class JsonAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str):
        super().__init__(pipeline_id)

    def process(self, data: Any) -> Union[str, Any]:
        if isinstance(data, dict):
            print(f"Input: {data}")

        res = self.run(data)

        print("Transform: Enriched with metadata and validation")
        print(f"Output: {res}")
        return res


class CsvAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str):
        super().__init__(pipeline_id)

    def process(self, data: Any) -> Union[str, Any]:
        print(f'Input: "{data}"')
        res = self.run(data)

        print("Transform: Parsed and structured data")
        print(f"Output: {res}")

        return res


class StreamAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str):
        super().__init__(pipeline_id)

    def process(self, data: Any) -> str:
        print("Input: Real-time sensor stream")
        res = self.run(data)

        print("Transform: Aggregated and filtered")
        if isinstance(data, list):
            avg = sum(data) / len(data) if data else 0
            print(
                f"Output: Stream summary: {len(data)} readings, avg: {avg}°C"
                )

        return res


class NexusManager:
    def __init__(self, capacity: int = 100):
        self.pipelines: Dict[str, ProcessingPipeline] = {}
        self.capacity = capacity
        self.n_processed = 0

    def add_pipeline(self, pipeline: ProcessingPipeline) -> None:
        self.pipelines[pipeline.pipeline_id] = pipeline

    def get_pipeline(self, pipeline_id):
        self.pipelines.get(pipeline_id)

    def process_data(self, data: Any, pipeline_id: str) -> Any:
        pipeline = self.get_pipeline(pipeline_id)
        if pipeline:
            res = pipeline.process(data)
            self.n_processed += 1
            return res
        raise ValueError(f"Pipeline {pipeline_id} not found")

    def chain_pipelines(self, data: Any, pipelines_ids: List[str]) -> Any:
        res = data

        for p in pipelines_ids:
            pipeline = self.get_pipeline(pipelines_ids)
            if pipeline:
                res = pipeline

        return res


if __name__ == "__main__":
    print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===\n")
    manager = NexusManager()

    json = JsonAdapter("JSON_001")

    json.add_stage(InputStage())
    json.add_stage(TransformStage())
    json.add_stage(OutputStage())

    manager.add_pipeline(json)
    manager.process_data({"sensor": "temp", "value": 23.5, "unit": "C"}, "JSON_001")
