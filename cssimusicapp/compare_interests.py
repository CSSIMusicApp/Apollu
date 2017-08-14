class Compare_Interests:
    def recommendusers(self, usercompared):
        common = len(set(user.interests) & set(usercompared.interests))
