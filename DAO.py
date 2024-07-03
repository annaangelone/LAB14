from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getCromosomi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = ("""select distinct chromosome c
                    from genes g 
                    where Chromosome > 0""")
        cursor.execute(query, )

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(c1, c2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""select g1.chromosome c1, g2.chromosome c2, g1.geneId g1, g2.geneId g2, i.Expression_corr ec
                    from genes g1, genes g2, interactions i 
                    where g1.geneID = i.GeneID1 and g2.GeneID = i.GeneID2 
                    and g1.chromosome = %s and g2.chromosome = %s
                    """)
        cursor.execute(query, (c1, c2))

        for row in cursor:
            result.append((row["c1"], row["c2"], row["g1"], row["g2"], row["ec"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(c1, c2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = ("""select sum(distinct i.Expression_Corr) as peso
                    from genes g1, genes g2, interactions i 
                    where g1.geneID = i.GeneID1 and g2.GeneID = i.GeneID2 
                    and g1.chromosome = %s and g2.chromosome = %s
                        """)
        cursor.execute(query, (c1, c2))

        for row in cursor:
            result.append(row[0])

        cursor.close()
        conn.close()
        return result[0]
