from connection_database.sqlite3_connection.sqlite3_connection import SQLite3Connection
import json
import uuid
from queries import *

file_path = 'three_minutes_tweets.json.txt'
tweets = []

database = SQLite3Connection('Test')
database.create_database()
database.create_table(create_start_table)

# In[upload data]
tweets_count = 1
for line in open(file_path, 'r'):
    insert_data_list = []
    parsed_string = json.loads(line)
    if 'created_at' and 'user' and 'text' in parsed_string:
        insert_data_list.append(parsed_string['created_at'])
        insert_data_list.append(parsed_string['user']['name'])
        insert_data_list.append(parsed_string['text'])

        if parsed_string['user']['location'] != '':
            insert_data_list.append(parsed_string['user']['location'])
        else:
            insert_data_list.append('No data')

        if parsed_string['place'] is not None:
            insert_data_list.append(parsed_string['place']['country_code'])
        else:
            insert_data_list.append('No data')

        if parsed_string['entities']['urls']:
            display_url_list = []
            for i in parsed_string['entities']['urls']:
                display_url_list.append(i['display_url'])
            insert_data_list.append(', '.join(display_url_list))
        else:
            insert_data_list.append('No data')

        if 'lang' in parsed_string:
            insert_data_list.append(parsed_string['lang'])
        else:
            insert_data_list.append('No data')

        database.insert_data(insert_into_first_table, insert_data_list)
        print(f'Insert tweet {tweets_count} complete')
        tweets_count += 1

# In[Normalize]


def new_table(database_connection: SQLite3Connection,
              sql_select: str,
              sql_create: str,
              sql_insert: str):
    return_dictionary = {}
    all_items = database_connection.select_data(sql_select)
    database_connection.create_table(sql_create)
    for item in all_items:
        unique_id = uuid.uuid3(uuid.NAMESPACE_DNS, str(item))
        item_list = [str(unique_id), item[0]]
        database_connection.insert_data(sql_insert, item_list)
        return_dictionary[str(item[0])] = str(unique_id)
    return return_dictionary


users_dictionary = new_table(database, select_all_username, create_users_table, insert_into_users_table)
locations_dictionary = new_table(database, select_all_location, create_locations_table, insert_into_locations_table)
countries_dictionary = new_table(database, select_all_country_codes, create_countries_table, insert_into_countries_table)
languages_dictionary = new_table(database, select_all_languages, create_languages_table, insert_into_languages_table)

database.create_table(create_message_table)
all_data = database.select_data(select_all)

for line in all_data:
    insert_data = []
    unique_id = uuid.uuid4()
    insert_data.append(str(unique_id))
    insert_data.append(line[2])
    insert_data.append(line[0])

    if line[5] == 'No data':
        insert_data.append(None)
    else:
        insert_data.append(line[5])

    if line[1] != '':
        insert_data.append(users_dictionary[line[1]])

    if line[4] == 'No data':
        insert_data.append(None)
    else:
        insert_data.append(countries_dictionary[line[4]])

    if line[3] == 'No data':
        insert_data.append(None)
    else:
        insert_data.append(locations_dictionary[line[3]])

    if line[6] == 'No data':
        insert_data.append(None)
    else:
        insert_data.append(languages_dictionary[line[6]])

    database.insert_data(insert_into_messages_table, insert_data)

database.add_column(add_column)

# In[sentiment]

file_path = 'AFINN-111.txt'
sentiment_dictionary = {}

for line in open(file_path, 'r'):
    array = line.split('\t')
    array[1].replace('\n', '')
    sentiment_dictionary[array[0]] = int(array[1])

all_message = database.select_data(select_messages)

for message in all_message:
    words = message[1].split()
    sentiment = 0
    for word in words:
        if word in sentiment_dictionary:
            sentiment += sentiment_dictionary[word]
    update_list = [sentiment, message[0]]
    database.insert_data(update_sentiment, update_list)

# In[query]

user = database.select_data(happiest_user)

print(f'Happinest user - {user[0][0]}')

country = database.select_data(happiest_country)

print(f'Happinest country - {country[0][0]}')

location = database.select_data(happinest_location)

print(f'Happinest location - {location[0][0]}')

