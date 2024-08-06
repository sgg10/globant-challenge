# import os

from kafka.consumer import create_consumer, consume


def run():
    consumer = create_consumer()

    try:
        for message in consume(consumer):
            print(message)
    except KeyboardInterrupt:
        ...
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Exiting...")
        consumer.close()
        print("Consumer closed.")


if __name__ == "__main__":
    run()
