import cx_Oracle
class Model:

    def __init__(self):
        self.song_dict={}
        self.db_status=True
        self.conn=None
        self.cur=None

        try:
            self.conn=cx_Oracle.connect("mouzikka/music@127.0.0.1/xe")
            print("connection opened")
            self.cur=self.conn.cursor()
            print("Cursor opened")

        except cx_Oracle.DatabaseError as ex:
            print("DB Error:",ex)
            self.db_status=False

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("Cursor closed")

        if self.conn is not None:
            self.conn.close()
            print("Connection closed")


    def add_song(self,song_name,song_path):
        self.song_dict[song_name]=song_path
        print("song added:",song_name)


    def get_song_path(self,song_name):
        return self.song_dict[song_name]

    def remove_song(self,song_name):
        self.song_dict.pop(song_name)
        print("song removed:",song_name)



    def search_song_in_favourites(self,song_name):
        self.cur.execute("select song_name from myfavourites where song_name=:1",(song_name,))
        song_tuple=self.cur.fetchone()
        if  song_tuple is None:
            return False
        else:
            return True


    def add_song_to_favourites(self,song_name,song_path):
        is_song_present=self.search_song_in_favourites(song_name)
        if is_song_present:
            return "song already present in your favourites"

        self.cur.execute("select max(song_id) from myfavourites")
        last_song_id=self.cur.fetchone()[0]
        next_song_id=1
        if last_song_id is not None:
            next_song_id=last_song_id+1
        self.cur.execute("insert into myfavourites values(:1,:2,:3)",(next_song_id,song_name,song_path))
        self.conn.commit()
        return "song added to your favourites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from myfavourites")
        songs_present=False
        for song_name,song_path in self.cur:
            self.song_dict[song_name] = song_path
            songs_present=True
        if songs_present==True:
            return "List populated from favourites"
        return "No song present in your favourites"


    def remove_song_from_favourites(self,song_name):
        try:
            self.cur.execute("Delete from myfavourites where song_name=:1", (song_name,))
            n = self.cur.rowcount
            if n == 0:
                print("No rows deleted")
                return "Song not present in favourites"
            else:
                print(n, " song deleted deleted")
                self.conn.commit()
                return " rows deleted"

        except (Exception) as ex:
            print(ex)
            
