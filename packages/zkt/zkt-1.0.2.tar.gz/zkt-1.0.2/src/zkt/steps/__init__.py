from zpy.utils.http_client import ZHttp, ZHttpResponse, HLevels
from zpy.app import zapp_context
from zpy.utils.values import if_null_get
from zkt import Step, OutputStep

logger = zapp_context().logger


class ExtractOutputValue(Step[OutputStep]):
    def run(self, result: OutputStep = None, shared_data: dict = {}) -> dict:
        return result.data


class DictValueExtract(Step[OutputStep]):
    def __init__(self, name: str, key: str):
        Step.__init__(self, name)
        self.key = key

    def run(self, result: OutputStep = None, shared_data: dict = {}) -> OutputStep:

        if isinstance(result, dict) and self.key in result:
            return OutputStep(data=result[self.key])
        if (
            isinstance(result, OutputStep)
            and isinstance(result.data, dict)
            and self.key in result.data
        ):
            return OutputStep(data=result.data[self.key])
        return OutputStep(data={})


class StoreTransactData(Step[OutputStep]):
    def __init__(self, name: str, key: str):
        Step.__init__(self, name)
        self.key = key

    def run(self, result: OutputStep = None, shared_data: dict = {}) -> OutputStep:

        if result:
            self.global_data[self.key] = result.data
        return result


class HttpResponseVerifier(Step[ZHttpResponse]):
    def __init__(self, name: str):
        Step.__init__(self, name)

    def run(self, result: ZHttpResponse = None, shared_data: dict = {}) -> OutputStep:
        if self.verbose:
            print("Response verifier: ", result.json)

        if result and result.is_ok():
            return OutputStep(data=result.json())

        return OutputStep(data=result.json(), is_ok=False)


class PostHttpRequest(Step):
    def __init__(self, name: str, log_levels: list[HLevels] = None):
        Step.__init__(self, name)
        self.log_levels = if_null_get(log_levels, [])

    def run(
        self, transaction_data: OutputStep = None, shared_data: dict = {}
    ) -> ZHttpResponse:
        x_data = {}
        if transaction_data:
            x_data = transaction_data.data

        url = x_data.get("url")
        headers = x_data.get("headers", {})
        data = x_data.get("data", {})
        body = x_data.get("body", None)
        params = x_data.get("params", {})

        if body:
            result = ZHttp.post(
                url=url,
                headers=headers,
                params=params,
                json=body,
                wrap_in_zhttp=True,
                log_options=self.log_levels,
                logger=logger,
            )
        if data:
            result = ZHttp.post(
                url=url,
                headers=headers,
                params=params,
                data=data,
                wrap_in_zhttp=True,
                log_options=self.log_levels,
                logger=logger,
            )
        return result
