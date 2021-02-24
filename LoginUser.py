class LoginUser:
    def fromDB(self, userID, cursor):
        self.userID = userID
        self.cursor = cursor

        self.cursor.execute('SELECT * FROM users WHERE id = %s', self.userID)
        self.__user = self.cursor.fetchone()
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])

    def get_email(self):
        return str(self.__user['email'])

    def get_count(self):
        return str(self.__user['count'])