create_start_table = ''' DROP TABLE IF EXISTS AllTweetInformation;
                            CREATE TABLE
                                AllTweetInformation (
                                    CreateAt TEXT,
                                    Name TEXT,
                                    TweetText TEXT,
                                    Location TEXT,
                                    CountryCode TEXT,
                                    DisplayUrl TEXT,
                                    Lang TEXT
                                )
            '''

add_column = '''
                ALTER TABLE 
                    Messages
                ADD COLUMN 
                    Sentiment INTEGER
'''

select_all_username = '''
                        SELECT DISTINCT 
                            Name
                        FROM 
                            AllTweetInformation
                        WHERE
                            Name <> ''
                        '''

select_all_location = '''
                        SELECT DISTINCT 
                            Location
                        FROM 
                            AllTweetInformation
                        where 
                            Location != 'No data'
                        and 
                            Location <> ''
                        '''

select_all_country_codes = '''
                            SELECT DISTINCT 
                                CountryCode
                            FROM 
                                AllTweetInformation
                            where 
                                CountryCode != 'No data'
                            and 
                                CountryCode <> ''
                        '''

select_all_languages = '''
                            SELECT DISTINCT 
                                Lang
                            FROM 
                                AllTweetInformation
                            where 
                                Lang != 'No data'
                            and 
                                Lang <> ''
                        '''

select_all = '''
                SELECT
                    *
                FROM 
                    AllTweetInformation
                WHERE
                    Name <> ''
                '''

select_messages = '''
                    SELECT
                        Id, 
                        MessageText
                    FROM 
                        Messages
                    WHERE 
                        LanguageId = '1cd7f6cb-f6ae-3e19-aa5a-456e4bcccadb'
                    '''

create_users_table = ''' DROP TABLE IF EXISTS Users;
                            CREATE TABLE
                                Users (
                                    Id TEXT NOT NULL PRIMARY KEY,
                                    Name TEXT NOT NULL
                                )
            '''

create_locations_table = '''DROP TABLE IF EXISTS Locations;
                            CREATE TABLE
                                Locations (
                                    Id TEXT NOT NULL PRIMARY KEY,
                                    Name TEXT NOT NULL
                                )
            '''

create_countries_table = '''DROP TABLE IF EXISTS Countries;
                            CREATE TABLE
                                Countries (
                                    Id TEXT NOT NULL PRIMARY KEY,
                                    Name TEXT NOT NULL
                                )
            '''

create_languages_table = '''DROP TABLE IF EXISTS Languages;
                            CREATE TABLE
                                Languages (
                                    Id TEXT NOT NULL PRIMARY KEY,
                                    Name TEXT NOT NULL
                                )
            '''

create_message_table = '''
                        DROP TABLE IF EXISTS Messages;
                        CREATE TABLE
                            Messages (
                                Id TEXT NOT NULL PRIMARY KEY,
                                MessageText TEXT,
                                CreationDate TEXT NOT NULL,
                                DisplayUrl TEXT,
                                UserId TEXT NOT NULL,
                                CountryId TEXT,
                                LocationId TEXT,
                                LanguageId TEXT,
                                FOREIGN KEY(UserId) REFERENCES Users(Id),
                                FOREIGN KEY(CountryId) REFERENCES Countries(Id),
                                FOREIGN KEY(LocationId) REFERENCES Location(Id),
                                FOREIGN KEY(LanguageId) REFERENCES Languages(Id)
                            )
                        '''

insert_into_first_table = '''
                            INSERT INTO 
                                AllTweetInformation 
                            VALUES 
                                (?,?,?,?,?,?,?)
                            '''

insert_into_users_table = '''
                            INSERT INTO 
                                Users
                            VALUES 
                                (?,?)
                            '''

insert_into_locations_table = '''
                                INSERT INTO 
                                    Locations
                                VALUES 
                                    (?,?)
                            '''

insert_into_countries_table = '''
                                INSERT INTO 
                                    Countries
                                VALUES 
                                    (?,?)
                            '''

insert_into_languages_table = '''
                                INSERT INTO 
                                    Languages
                                VALUES 
                                    (?,?)
                            '''

insert_into_messages_table = '''
                                INSERT INTO 
                                    Messages
                                VALUES 
                                    (?,?,?,?,?,?,?,?)
                            '''

update_sentiment = '''
                    UPDATE 
                        Messages 
                    SET 
                        Sentiment = ?
                    WHERE 
                        Id = ?
                    '''

happiest_user = '''
                    SELECT
                        u.Name,
                        sum(Sentiment) AS Sum
                    FROM
                        Messages
                    LEFT JOIN
                        Users U 
                    ON 
                        Messages.UserId = U.Id
                    WHERE
                        Sentiment IS NOT NULL
                    GROUP BY 
                        U.Name
                    ORDER BY Sum DESC
                    LIMIT 1
                '''

happiest_country = '''
                    SELECT
                        C.Name,
                        sum(Sentiment) AS Sum
                    FROM
                        Messages
                    LEFT JOIN
                        Countries C 
                    ON 
                        Messages.CountryId = C.Id
                    WHERE
                        Sentiment IS NOT NULL
                    AND
                        C.Name IS NOT NULL
                    GROUP BY 
                        C.Name
                    ORDER BY Sum DESC
                    LIMIT 1
                    '''

happinest_location = '''
                        SELECT
                            L.Name,
                            sum(Sentiment) AS Sum
                        FROM
                            Messages
                        LEFT JOIN
                            Locations L on Messages.LocationId = L.Id
                        WHERE
                            Sentiment IS NOT NULL
                        AND
                            L.Name IS NOT NULL
                        GROUP BY L.Name
                        ORDER BY Sum DESC
                        LIMIT 1
                        '''