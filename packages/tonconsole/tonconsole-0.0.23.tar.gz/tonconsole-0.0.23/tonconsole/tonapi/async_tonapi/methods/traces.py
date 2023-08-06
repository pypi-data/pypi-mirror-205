import base64

from tonconsole.tonapi.async_tonapi import AsyncTonapiClient

from tonconsole.tonapi.schema.traces import Trace


class TraceMethod(AsyncTonapiClient):

    async def get_trace(self, trace_id: str) -> Trace:
        """
        Get the trace by trace ID or hash of any transaction in trace.

        :param trace_id: trace ID or transaction hash in hex (without 0x) or base64url format
        :return: :class:`Trace`
        """
        method = f"v2/traces/{base64.urlsafe_b64encode(trace_id.encode()).decode()}"
        response = await self._request(method=method)

        return Trace(**response)
