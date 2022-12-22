def main():
    Event()


    @client.event
    async def on_message(message):
        try:

            if message.author.id == morangs_id:
                return

            with open('Database/user_blacklist.txt', 'r', encoding='utf-8') as user_blacklist_data:
                if str(message.author.id) in user_blacklist_data.read().split():
                    return
                user_blacklist_data.close()

            await Automatic(message).update()

            has_prefix = True if str(message.content).startswith(PREFIX) else False
            await Commands(message, has_prefix).update()

        except Exception:
            traceback.print_exc()
            await client.get_channel(999363516505010186).send(f'```{traceback.format_exc()}```')


    client.run(TOKEN)


if __name__ == '__main__':
    import traceback

    from core import client, DEVELOPER_ID, morangs_id, TOKEN, PREFIX
    from events import Event
    from commands import Commands
    from automatics import Automatic

    main()
