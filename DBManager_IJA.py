# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
sys.path.append("/Libs/mysql-connector-java-5.1.22-bin.jar")

from java.lang import Integer
from java.lang import Class
from java.sql import DriverManager
from java.sql import ResultSet

import threading
from threading import Lock

class DBManager(object):
    GlobalConn = None
    timeout = 200.0
    lock = None

    @staticmethod
    def init():
        DBManager.lock = Lock()
        DBManager.GlobalConn = None
        print (u'[DBManager] initialized DBManager!')

    @staticmethod
    def autoconnection():
        # DBManager.lock.acquire()
        if DBManager.GlobalConn is not None:
            DBManager.GlobalConn.close()
            DBManager.GlobalConn = None

        Class.forName("com.mysql.jdbc.Driver").newInstance()
        newConn = DriverManager.getConnection("jdbc:mysql://localhost:3306/test?", "root", "")
        # newConn = DriverManager.getConnection("jdbc:mysql://203.255.81.42:3306/stackoverflow?autoReconnect=true", "seal", "sel535424")
        newConn.setAutoCommit(True)
        DBManager.GlobalConn = newConn
        # DBManager.lock.release()

        # print(u'[DBManager] reconnected to DB because of the time out which is %d seconds!' % DBManager.timeout)
        # threading.Timer(DBManager.timeout, DBManager.autoconnection).start()
        pass

    @staticmethod
    def requestQuery(_query):
        '''
        request query with lock
        :param _query:
        :return:
        '''
        # DBManager.lock.acquire()

        stmt = DBManager.GlobalConn.createStatement(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY)

        stmt.setFetchSize(Integer.MIN_VALUE)
        items = []
        try:
            resultSet = stmt.executeQuery(_query)
        except:
            # DBManager.lock.release()
            return items

        # DBManager.lock.release()

        return resultSet

        # result_count = 0
        # while resultSet.next():
        #     result_count += 1
        #     # items.append(resultSet.getInt(1))
        #     items.append(resultSet.getInt('ID'))
        #     items.append(resultSet.getInt('STARTLINE'))
        #     items.append(resultSet.getInt('ENDLINE'))
        # resultSet.close()
        #
        # DBManager.lock.release()
        # return items, result_count

    # -*- coding: utf-8 -*-