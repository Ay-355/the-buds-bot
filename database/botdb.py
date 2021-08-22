import sqlite3


class BotDatabase:
    def __init__(self, db_filepath):
        """
        Class used to connect to the database

        db_filepath = file path to the file

        """
        self.conn = sqlite3.connect(db_filepath)
        self.conn.cursor().execute("PRAGMA foreign_keys = 1")  # Enables foreign keys
        self.initiate_db()

    def initiate_db(self):
        create_player_to_id_table = ("""CREATE TABLE IF NOT EXISTS server_players (
                                        discord_id integer NOT NULL,
                                        coc_tag text NOT NULL,
                                        coc_name text NOT NULL,
                                        coc_th text NOT NULL,
                                        PRIMARY KEY(coc_tag))""")
        
        self.conn.cursor().execute(create_player_to_id_table)
        self.conn.commit()


        create_role_to_clan_table = ("""CREATE TABLE IF NOT EXISTS role_to_tag (
                                        guild_id integer NOT NULL,
                                        role_id integer NOT NULL,
                                        clan_tag text NOT NULL,
                                        PRIMARY KEY(clan_tag))""")

        self.conn.cursor().execute(create_role_to_clan_table)
        self.conn.commit()


    def register_user(self, tuple_data):
        """Used to register a user by taking their data"""
        sql = """INSERT INTO server_players(
                discord_id,
                coc_tag,
                coc_name,
                coc_th)
                VALUES (?,?,?,?)
                """
        self.conn.cursor().execute(sql, tuple_data)
        self.conn.commit()


    def get_player_with_id(self, tuple_data):
        """Gets a players accounts using their id"""

        c = self.conn.cursor()
        c.execute("SELECT coc_tag FROM server_players WHERE discord_id =?", tuple_data)
        results = c.fetchall()
        return [row[0] for row in results]


    def get_member_with_tag(self, tuple_data):
        """Gets the members id using their tag"""

        c = self.conn.cursor()
        c.execute("SELECT discord_id FROM server_players WHERE coc_tag =?", tuple_data)
        results = c.fetchone()
        if results is None:
            return None
        for row in results:
            return row




    def get_all_users(self):
        """Gets all the users"""        
        sql = """SELECT * FROM server_players"""
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchall()


    def get_tags(self):
        sql = "SELECT coc_tag FROM server_players"
        c = self.conn.cursor()
        c.execute(sql)
        results = c.fetchall()
        return [row[0] for row in results]



    def get_townhall(self):
        """gets users townhall"""   
        sql = "SELECT coc_th FROM server_players"
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchall()


    # def update_server_players(self, tuple_data):
    #     """Updates the tale when they upgrade townhall or other things

    #     Args:
    #         tuple_data (tuple): has the data we need to update
    #     """
    #     c = self.conn.cursor()
    #     c.execute("""UPDATE server_players SET coc_th=? WHERE coc_tag=?""", tuple_data)
    #     results = c.fetchall()
    #     return results


    def update_user_th(self, tuple_data):
        """Updates users townhall on upgrades

        Args:
            tuple_data (tuple): has the data we need to update
        """
        c = self.conn.cursor()
        c.execute("""UPDATE server_players SET coc_th=? WHERE coc_tag=?""", tuple_data)
        return c.fetchall()


    def link_role_to_tag(self, tuple_data):
        """Links a discord role to a clan_tag

        Args:
            tuple_data (tuple): tuple of the data we need to insert into table
        """
        sql = """INSERT INTO role_to_tag(
            guild_id,
            role_id,
            clan_tag)
            VALUES (?,?,?)
            """
        self.conn.cursor().execute(sql, tuple_data)
        self.conn.commit()


    def get_linked_roles(self, tuple_data):
        """gets all the linked role to clan in a guild

        Args:
            tuple_data (tuple): the guild id
        """
        c = self.conn.cursor()
        c.execute("""SELECT role_id FROM role_to_tag WHERE guild_id=?""", tuple_data)
        results = c.fetchall()
        return [row[0] for row in results]


    def get_linked_clans(self, tuple_data):
        """gets all the clans that are linked to clans in a guild

        Args:
            tuple_data (tuple): the guild id
        """
        c = self.conn.cursor()
        c.execute("""SELECT clan_tag FROM role_to_tag WHERE guild_id=?""", tuple_data)
        results = c.fetchall()
        return [row[0] for row in results]


    def get_role_from_clan_tag(self, tuple_data):
        c = self.conn.cursor()
        c.execute("""SELECT role_id FROM role_to_tag WHERE clan_tag=? AND guild_id=?""", tuple_data)
        results = c.fetchall()
        for row in results:
            return row[0]



    def get_linked_clans_and_roles(self, tuple_data):
        """gets all the roles that are linked to clans in a guild

        Args:
            tuple_data (tuple): the guild id
        """
        c = self.conn.cursor()
        c.execute("""SELECT clan_tag, role_id FROM role_to_tag WHERE guild_id=?""", tuple_data)
        tag, role = c.fetchall()
        return tag, role



    def get_linked_clans_without_guild_id(self):
        """gets all the clans in the database"""
        c = self.conn.cursor()
        c.execute("""SELECT clan_tag FROM role_to_tag""")
        results = c.fetchall()
        return [row[0] for row in results]



    def remove_user_from_server_players_with_coc_tag(self, tuple_data):
        """removes an entry from the server_players database"""
        c = self.conn.cursor()
        c.execute("""DELETE FROM server_players WHERE coc_tag=?""", tuple_data)
        self.conn.commit()



    def remove_role_from_role_to_tag(self, tuple_data):
        """removes a row from role_to_tag"""
        c = self.conn.cursor()
        c.execute("""DELETE FROM role_to_tag WHERE role_id=? AND guild_id=?""", tuple_data)
        self.conn.commit()