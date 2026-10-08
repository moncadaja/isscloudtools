def slack_create_channel(client,channel_name ):
    channel = client.conversations_create(name = channel_name, is_private = True)
    return channel.data['channel']['id'], channel.data['channel']


# def slack_invite_to_channel(client, channel_id, users = ['U016TSW4MSB', 'U018F0DLENQ', 'U01RR69G6E8']):
def slack_invite_to_channel(client, channel_id, users=['U016TSW4MSB', 'U01RR69G6E8']):
    return client.conversations_invite(channel=channel_id, users=users).data['ok']


def slack_upload_image(client,channel_id, path_to_file, message):
    return client.files_upload_v2(file=path_to_file, initial_comment=message, channel=channel_id).data['ok']


def slack_post_message(client,channel_id, text):
    return client.chat_postMessage(channel=channel_id,text = text).data['ok']


def slack_channel_exists(client, channel_name):
    channels = client.conversations_list(types ="public_channel, private_channel" ).data['channels']
    channel_info = []
    channel_id = []
    for channel in channels:
        if channel['name_normalized'] == channel_name:
            channel_info = channel
            channel_id = channel['id']
            break
    return channel_id, channel_info



