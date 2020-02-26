if __name__ == '__main__':

    # Import Adafruit IO REST client.
    from Adafruit_IO import Client, Feed, Data, RequestError
    import datetime

    # Set to your Adafruit IO key.
    # Remember, your key is a secret,
    # so make sure not to publish it when you publish this code!
    ADAFRUIT_IO_KEY = 'aio_Mbeo57A4D24lfhO07ODfzvIOgKQy'

    # Set to your Adafruit IO username.
    # (go to https://accounts.adafruit.com to find your username)
    ADAFRUIT_IO_USERNAME = 'BohemianXen'

    # Create an instance of the REST client.
    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    acc = []
    try:
        acc.append(aio.feeds('lightbluefalldetectorax'))
        acc.append(aio.feeds('lightbluefalldetectoray'))
        acc.append(aio.feeds('lightbluefalldetectoraz'))
    except RequestError:
        print("Error establishing feeds")
        # feed = Feed(name="temperature")
        # temperature = aio.create_feed(feed)

    #
    # Retrieving data
    #

    data = []

    for i in range(3):
        sample = []
        for j in range(3):
            sample.append(aio.data(acc[j].key))
            print(sample[-1])
        data.append(sample)


# #
# # Adding data
# #
#
# aio.send_data(temperature.key, 42)
# # works the same as send now
# aio.append(temperature.key, 42)
#
# # setup batch data with custom created_at values
# yesterday = (datetime.datetime.today() - datetime.timedelta(1)).isoformat()
# today = datetime.datetime.now().isoformat()
# data_list = [Data(value=50, created_at=today), Data(value=33, created_at=yesterday)]
# # send batch data
# aio.send_batch_data(temperature.key, data_list)
