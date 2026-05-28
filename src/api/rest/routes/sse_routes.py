from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
import logging
from uuid import UUID
logger=logging.getLogger(__name__)
router = APIRouter()
subscribers: dict = {} 
@router.get("/sse/{user_id}")
async def sse_endpoint(user_id:UUID):
    queue = asyncio.Queue()
    subscribers[user_id] = queue

    async def event_generator():
        try:
            while True:
                data = await queue.get()  # waits until a task is assigned
                yield {"event": "task_assigned",    "data": json.dumps(data)}
                logger.info(f"Sent SSE update to user {user_id} for task assignment")
        except asyncio.CancelledError:
            del subscribers[user_id]  # cleanup on disconnect

    return EventSourceResponse(event_generator())
