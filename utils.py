# -*- coding: utf-8 -*-
from flask import flash
import os
import psycopg2
from werkzeug.utils import secure_filename
import errno
import hashlib
import smtplib as smtp
from transliterate import translit


class FlashUtils:
    @staticmethod
    def generate_success(text):
        flash(text, 'success')

    @staticmethod
    def generate_error(text):
        flash(text, 'danger')


class UploadUtils:
    @staticmethod
    def allowed_file(filename):
        from run import app
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    # file upload method
    @staticmethod
    def upload_file(files, answer_uuid):
        from run import app
        saved_files = []
        for file in files:
            if file and UploadUtils.allowed_file(file.filename):
                filename, file_extension = os.path.splitext(file.filename)
                try:
                    filename = translit(filename, reversed=True)
                except:
                    None
                filename = secure_filename(''.join((filename, file_extension)))
                full_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)) + app.config['UPLOAD_FOLDER'] + '/answer/{}'.format(
                        str(answer_uuid)), filename)
                if not os.path.exists(os.path.dirname(full_path)):
                    try:
                        os.makedirs(os.path.dirname(full_path))
                    except OSError as exc:  # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                file.save(full_path)
                saved_files.append(filename)
        return saved_files

class DbQuery:
    def __init__(self):
        from run import app
        self.conn_string = "dbname={} user={} password={} host={}".format(app.config['DATABASE_URL'],
                                                                          app.config['USERNAME'],
                                                                          app.config['PASSWORD'], app.config['HOST'])

    def create_db_connection(self):
        return psycopg2.connect(self.conn_string)

    def close_db_connection(self, cur, conn):
        cur.close()
        conn.close()

    def execute_query(self, query, is_dml=False):
        conn = self.create_db_connection()
        cursor = None
        result = None

        try:
            cursor = conn.cursor()
            cursor.execute(query)
            if is_dml:
                result = DbQueryResponse()
                conn.commit()
            else:
                result = DbQueryResponse(value=cursor.fetchall())
        except psycopg2.Error as e:
            if cursor is not None:
                conn.rollback()
                result = DbQueryResponse(False, e.pgerror)
        except Exception as e:
            if cursor is not None:
                conn.rollback()
                result = DbQueryResponse(False, 'Error')
        finally:
            if cursor is not None:
                cursor.close()
        conn.close()
        return result

    def execute_query_wo_commit(self, cursor, query, is_dml=False):
        result = None
        try:
            cursor.execute(query)
            if is_dml:
                result = DbQueryResponse()
            else:
                result = DbQueryResponse(value=cursor.fetchall())
        except psycopg2.Error as e:
            if cursor is not None:
                result = DbQueryResponse(False, e.pgerror)
        return result

class DbQueryResponse:
    def __init__(self, is_success=True, value=None):
        self.success = is_success
        self.value = value

    def __str__(self):
        return "success : {}, value: {}".format(str(self.success), str(self.value))


class PasswordUtils:
    @staticmethod
    def generate(encoded_string):
        from run import app
        return ((hashlib.sha256(encoded_string + app.config['SECRET_KEY'].encode())).hexdigest())


def send_email(subject, mail_to, text):
    from run import app
    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(app.config['EMAIL_MAIL_FROM'],
                                                           mail_to,
                                                           subject,
                                                           text)
    server = smtp.SMTP_SSL(app.config['EMAIL_SERVER'])
    # server.set_debuglevel(1)
    # server.ehlo(email)
    server.login(app.config['EMAIL_LOGIN'], app.config['EMAIL_PASSWORD'])
    server.auth_plain()
    server.sendmail(app.config['EMAIL_MAIL_FROM'], mail_to, message.encode('utf-8'))
    server.quit()


def get_dictionary_by_name(item, value=None):
    from run import  db_query
    if not value:
        query_result = db_query.execute_query(""" SELECT *
                                               FROM public.{}
                                               ORDER BY id ASC;""".format(item))
        return (query_result.value)
    else:
        query_result = db_query.execute_query(""" SELECT id
                                               FROM public.{}
                                               WHERE name='{}';""".format(item, value))
        return (query_result.value[0][0])


def set_or_appned_to_array(array, idx, value):
    idx = int(idx)
    try:
        array[idx] = value
    except:
        if idx > 0:
            for i in range(0, idx+1):
                array.append('')
        else:
            array.append('')
        array[idx] = value
    return array
