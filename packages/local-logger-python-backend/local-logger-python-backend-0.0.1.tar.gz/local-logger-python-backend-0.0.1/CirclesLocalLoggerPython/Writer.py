class Writer:
    def __init__(self, pool):
        self._pool = pool

    def add(self, **kwargs):

        try:
            params_to_insert = kwargs['object']
            # creating connection
            connection = self._pool.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"insert into location.location_table (coordinate) values (POINT({params_to_insert['latitude']},{params_to_insert['longitude']}));")
            coordinate_id = cursor.lastrowid
            params_to_insert.pop('latitude')
            params_to_insert.pop('longitude')
            params_to_insert['location_id'] = coordinate_id
            listed_values = list(params_to_insert.values())
            joined_keys = ','.join(list(params_to_insert.keys()))
            generate_values_pattern = ','.join(['%s' for i in range(len(listed_values))])
            sql = f"""INSERT INTO logger_table ({joined_keys})
                        VALUES ({generate_values_pattern});
            """
            cursor.execute(sql,listed_values)
        except Exception as e:
            print("catched " + str(e))
        finally:
            connection.commit()
            cursor.close()
            connection.close()

    def add_message(self, message, log_level):

        try:
            # creating connection
            connection = self._pool.get_connection()
            cursor = connection.cursor()
            sql = f"INSERT INTO logger_table (payload, severity_id) VALUES ('{message}', {log_level})"
            cursor.execute(sql)

        except Exception as e:
            print("catched" + str(e))
        finally:
            connection.commit()
            cursor.close()
            connection.close()
