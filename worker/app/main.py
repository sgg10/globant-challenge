import json
import logging
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

import constants
from database.models import Task
from tasks.manager import TaskManager
from database.connection import create_session
from kafka.consumer import create_consumer, consume


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def process_task(message: dict):
    logging.info(constants.PROCESS_TASK_INIT_MESSAGE(message["task_id"]))
    _, session = create_session()

    task = session.query(Task).filter_by(id=message["task_id"]).first()

    if task.status_id == constants.TaskStatusIdEnum.COMPLETED:
        logging.info(constants.PROCESS_ALREADY_COMPLETED(message["task_id"]))
        return

    if task.status_id == constants.TaskStatusIdEnum.FAILED:
        logging.info(constants.PROCESS_ALREADY_FAILED(message["task_id"]))
        return

    task.status_id = constants.TaskStatusIdEnum.IN_PROGRESS.value
    task.start_at = datetime.now()

    session.commit()

    try:
        task_manager = TaskManager(message, session)
        result, error = task_manager.run()

        if error:
            raise Exception(error)

        task.status_id = constants.TaskStatusIdEnum.COMPLETED.value
        task.config = {**json.loads(task.config), "result": result}
    except Exception as e:
        logging.error(
            constants.PROCESS_TASK_FAILED(message["task_id"]) + f" Error: {e}"
        )

        task.status_id = constants.TaskStatusIdEnum.FAILED.value
        task.config = {**json.loads(task.config), "error": str(e)}
    finally:
        task.end_at = datetime.now()

    session.commit()

    logging.info(constants.PROCESS_TASK_SUCCESS(message["task_id"]))


def run():
    logging.info(constants.CONSUMER_START_MESSAGE)
    consumer = create_consumer()

    if constants.USE_CONCURRENCE:
        with ProcessPoolExecutor(max_workers=constants.WORKERS) as executor:
            try:
                for message in consume(consumer):
                    executor.submit(process_task, message)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                logging.error(
                    constants.PROCESS_TASK_FAILED(message["task_id"]) + f" Error: {e}"
                )
            finally:
                logging.info(constants.CONSUMER_CLOSE_MESSAGE)
                consumer.close()
            executor.shutdown(wait=True)

        return

    try:
        for message in consume(consumer):
            process_task(message)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(
            constants.PROCESS_TASK_FAILED(message["task_id"]) + f" Error: {e}"
        )
    finally:
        logging.info(constants.CONSUMER_CLOSE_MESSAGE)
        consumer.close()


if __name__ == "__main__":
    run()
