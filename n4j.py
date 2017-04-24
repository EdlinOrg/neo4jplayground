
from py2neo import Graph

class N4J:

    graph = None

    def __init__(self, url):
        self.url = url

    def get_graph(self):
        if self.graph == None:
            self.graph = Graph(self.url)

        return self.graph

    def is_fof(self, ourid1, ourid2):
        """
        Returns boolean whether the two users are 2nd degree
        """
        cursor = self.get_graph().run(
            "OPTIONAL MATCH (user1 :User{ourid:{ourid1}})-[:FRIEND]-(yourFriends),"
            "(yourFriends)-[:FRIEND]-(user2 :User{ourid:{ourid2}})"
            "RETURN user2 IS NOT NULL as isConnected;"
            , {"ourid1": ourid1, "ourid2": ourid2})

        res = cursor.evaluate()

        cursor.close()

        return res

    def is_fofof(self, ourid1, ourid2):
        """
        Returns boolean whether the two users are connected through 2nd or 3rd degree
        """
        cursor = self.get_graph().run(
            "OPTIONAL MATCH (user1 :User{ourid:{ourid1}})-[:FRIEND*2..3]-(user2 :User{ourid:{ourid2}})"
            "RETURN user2 IS NOT NULL as isConnected;"
            , {"ourid1": ourid1, "ourid2": ourid2})

        res = cursor.evaluate()

        cursor.close()

        return res

    def get_2nd_or_3rd(self, ourid):
        """
        Returns a list of 2nd and 3rd degree connections for the specific ourid
        """
        cursor = self.get_graph().run(
            "MATCH (:User{ourid:{ourid}})-[:FRIEND*2..3]-(user) RETURN user.ourid as ourid"
            , {"ourid": ourid})

        res = set()
        while cursor.forward():
            cur = cursor.current()
            res.add(cur['ourid'])

        cursor.close()

        return list(res)