import asyncio
import asynqp


async def server_to_server_broadcasts(app):
    connection = await asynqp.connect(
        host=app.config.AMQP_HOST,
        port=app.config.AMQP_PORT,
        username=app.config.AMQP_USERNAME,
        password=app.config.AMQP_PASSWORD)

    channel = await connection.open_channel()

    @app.listener('after_server_stop')
    async def teardown(*_):
        await channel.close()
        await connection.close()

    exchange = await channel.declare_exchange('test.exchange', 'direct')
    queue = await channel.declare_queue('test.queue')

    await queue.bind(exchange, 'routing.key')

    msg = asynqp.Message({'hello': 'world'})
    exchange.publish(msg, 'routing.key')

    async for message in queue.get():
        print(message.json())
        message.ack()


async def database_broadcasts(app):
    pass


async def subscribe_and_broadcast(app):
    await asyncio.wait([
        server_to_server_broadcasts(app),
        database_broadcasts(app)])
