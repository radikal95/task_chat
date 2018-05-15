from flask_login import login_user, UserMixin, login_required


class Member(UserMixin):
    def __init__(self, id = None,
                 password = None,
                 status = None,
                 team_id= None,
                 city = None,
                 task_id = None,
                 answer = None):
        self.id = id
        self.password = password
        self.status = status
        self.team_id = team_id
        self.city = city
        self.task_id = task_id
        self.answer = answer

    def get(self):
        from run import db_query
        query = """SELECT  id, password, status, team_id, city, task_id, answer
                                                                   FROM public.member
                                                              WHERE {} = {};"""

        query_result = db_query.execute_query(query.format('id', self.id))
        if len(query_result.value) < 1:
            raise Exception
        self.id = query_result.value[0][0]
        self.password = query_result.value[0][1]
        self.status = query_result.value[0][2]
        self.team_id = query_result.value[0][3]
        self.city = query_result.value[0][4]
        self.task_id = query_result.value[0][5]
        self.answer = query_result.value[0][6]

    def update_status(self, new_status):
        from run import db_query
        query = """  UPDATE public.member
                            SET status= {} WHERE id={};"""
        query_result = db_query.execute_query(query.format(new_status,self.id), is_dml=True)

    def update_task(self, new_task):
        from run import db_query
        query = """  UPDATE public.member
                            SET task_id= {} WHERE id={};"""
        query_result = db_query.execute_query(query.format(new_task,self.id), is_dml=True)

    def update_answer(self, new_answer):
        from run import db_query
        query = """  UPDATE public.member
                                SET answer= '{}' WHERE id={};"""
        query_result = db_query.execute_query(query.format(new_answer, self.id), is_dml=True)

    def search(self):
        from run import  db_query
        query = """SELECT  id FROM public.member
                   WHERE status = 1 and city!='{}' LIMIT 1;"""
        search_result = db_query.execute_query(query.format(self.city))
        if len(search_result.value) < 1:
            return False
        else:
            conn = db_query.create_db_connection()
            cur = conn.cursor()
            query = """INSERT INTO public.team(
            	                    count, points)
            	                    VALUES (2, 0)
            	                    RETURNING id;"""
            team_insert_result = db_query.execute_query_wo_commit(cur, query)
            conn.commit()
            db_query.close_db_connection(cur, conn)
            query = """  UPDATE public.member
                                        SET team_id= {} , status = 2 WHERE id in ({},{});"""
            update_result = db_query.execute_query(query.format(team_insert_result.value[0][0], self.id,search_result.value[0][0]), is_dml=True)
            query = """  UPDATE public.member
                                                    SET task_id= 1 WHERE id = {};"""
            set_task_result = db_query.execute_query(query.format(self.id), is_dml=True)
            query = """  UPDATE public.member
                                                    SET task_id= 2 WHERE id = {};"""
            set_task_result = db_query.execute_query(query.format(search_result.value[0][0]), is_dml=True)
            return True

    def add_to_team(self):
        from run import  db_query
        query = """SELECT  id, count, points
                                                                         FROM public.team
                                                                    WHERE count = 1 LIMIT 1;"""
        query_result = db_query.execute_query(query)
        if len(query_result.value)>1:
            team_id = query_result.value[0][0]
            query = """ UPDATE public.member
                            SET team_id= {},status=2 WHERE id={};"""
            query_result = db_query.execute_query(query.format(team_id,self.id), is_dml=True)
            query = """ UPDATE public.team
                            SET count= 2 WHERE id={};"""
            query_result = db_query.execute_query(query.format(team_id), is_dml=True)
        else:
            query = """INSERT INTO public.team(count, points)
	                                    VALUES ( 1, 0);"""
            query_result = db_query.execute_query(query, is_dml=True)
            self.add_to_team()


    def get_answer(self):
        from run import db_query
        query = """SELECT  answer FROM public.member
                    WHERE team_id = {} and id != {};"""
        query_result = db_query.execute_query(query.format(self.team_id,self.id))
        return  (query_result.value[0][0])

    def team_status(self):
        from run import db_query
        query = """SELECT  status FROM public.member
                            WHERE team_id = {};"""
        query_result = db_query.execute_query(query.format(self.team_id))
        return (query_result.value[0][0])

    def get_task(self):
        from run import db_query
        query = """SELECT  task_id FROM public.member
                    WHERE team_id = {} and id != {};"""
        task_query_result = db_query.execute_query(query.format(self.team_id,self.id))
        query = """SELECT  value FROM public.task
                            WHERE id = {};"""
        query_result = db_query.execute_query(query.format(task_query_result.value[0][0]))
        return query_result.value[0][0]

class Team():
    def __init__(self, id = None,
                 count = None,
                 points = None):
        self.id = id
        self.count = count
        self.points = points

    def get(self):
        from run import db_query
        query = """SELECT  id, count, points
                                                                      FROM public.team
                                                                 WHERE id = {};"""

        query_result = db_query.execute_query(query.format(self.id))
        if len(query_result.value) < 1:
            raise Exception
        self.id = query_result.value[0][0]
        self.count = query_result.value[0][1]
        self.points = query_result.value[0][2]



class Task():
    def __init__(self, id = None,
                 value = None):
        self.id = id
        self.value = value

    def get(self):
        from run import db_query
        query = """SELECT  id, value
                                                                              FROM public.task
                                                                         WHERE id = {};"""

        query_result = db_query.execute_query(query.format(self.id))
        if len(query_result.value) < 1:
            raise Exception
        self.id = query_result.value[0][0]
        self.value = query_result.value[0][1]

