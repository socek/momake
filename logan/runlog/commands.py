from datetime import datetime
from datetime import timezone
from typing import Optional
from uuid import UUID
from uuid import uuid4

from logan.runlog.conn import engine
from logan.runlog.queries import get_task
from logan.runlog.tables import TaskTable
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy.orm import Session


def set_task_log(
    task_id: str,
    run_id: UUID,
    check_runtime: Optional[datetime] = None,
    runtime: Optional[datetime] = None,
    runtime_finish: Optional[datetime] = None,
):
    task = get_task(task_id, run_id)
    if task:
        values = dict(
            check_runtime=check_runtime,
            runtime=runtime,
            runtime_finish=runtime_finish,
            updated_at=datetime.now(timezone.utc),
        )
        filtered = {k: v for k, v in values.items() if v is not None}
        stmt = (
            update(TaskTable)
            .where(
                TaskTable.task_id == task_id,
                TaskTable.run_id == run_id,
            )
            .values(**filtered)
        )
    else:
        stmt = insert(TaskTable).values(
            id=uuid4(),
            task_id=task_id,
            run_id=run_id,
            check_runtime=check_runtime,
            runtime=runtime,
            runtime_finish=runtime_finish,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
    with Session(engine()) as db:
        db.execute(stmt)
        db.commit()
