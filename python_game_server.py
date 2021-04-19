#!/usr/bin/env python3
""" Python wars"""
import socket


def snddata(asocket, data):
    """Don't call this method directly"""
    asocket.send(data + "End_Of_File_DATA_End_Of_File")


def rcvdata(asocket):
    """Don't call this method directly"""
    database = ""
    eof = False
    while not eof:
        newdata = asocket.recv(2048)
        database += newdata
        eof = (database[-10:] == "End") or (newdata == "")
    return database[:-10]


class Exercise:
    """ exercise class"""

    serverip = "10.10.10.10"
    serverport = 10000

    def register(self, teamname, password=""):
        """Use  this  method  to  register   your  teams.  Pass  it  your  team
        name  and  your team  password.  To  join  an  existing team  you  must
        know  the  team  password.  Once  registered  all  points  scored  from
        your  IP  will be  credited  to  the  team.  NOTE: When  you  initially
        register  for  a  team  or  change teams  ALL  points  associated  with
        your  IP   will  be   lost.  SO  REGISTER   FIRST!!  For   example  >>>
        game_object.register('my_team','my_password')"""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, "REGISTER=" + teamname + ":" + password)
        data_packet = rcvdata(mysocket)
        mysocket.close()
        return data_packet

    def points(self, number):
        """Use this  method to see how  many points a given  question is worth.
        The argument  must be an  integer of the  question number you  want the
        point value of. For example,  game_object.point(1) will return how many
        points question 1 is worth if answered correctly."""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, str(number).strip() + "-P")
        data_packet = rcvdata(mysocket)
        mysocket.close()
        return data_packet

    def question(self, number):
        """Use  this method  to read  a question.  It takes  one argument.  The
        argument must  be an integer of  the question number you  want to read.
        For  example,  to  see  question  number  1  you  would  do  this:  >>>
        game_object.question(1)"""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, str(number).strip() + "-Q")
        data_packet = rcvdata(mysocket)
        mysocket.close()
        return data_packet

    def score(self):
        """This  method  prints  the  current  scoreboard.  Example  >>>  print
        game_object.score()"""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, "SCORE")
        data_packet = rcvdata(mysocket)
        mysocket.close()
        return data_packet

    def data(self, number):
        """This method will give you the data for a given question that you are
        supposed to manipulate.  This method takes one  argument. That argument
        is an integer  for the data element you want  to retrieve. For example,
        the  data  element  of  question  one is  retrieved  by  executing  >>>
        game_object.data(1) For many functions this is a dynamic element and it
        changes  every time  you query  it. You  will typically  pass the  data
        returned by this method to a function that will calculate the answer to
        the  question so  you  can  submit it  to  answer.  For example,  after
        creating a function called 'solve_number_1()' get the answer by calling
        solve_number_1(game_object.data(1))"""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, str(number).strip() + "-D")
        data_packet = rcvdata(mysocket)
        mysocket.close()
        if "Invalid Question Number" in data_packet:
            return data_packet
        try:
            data_packet = int(data_packet)
        except socket.error as err:
            print(err)
        if type(data_packet) != str:
            return data_packet
        if data_packet[0] == "[" and data_packet[-1] == "]":
            data_packet = eval(data_packet)
        elif data_packet[0] == "(" and data_packet[-1] == ")":
            data_packet = eval(data_packet)
        elif data_packet[0] == "{" and data_packet[-1] == "}":
            data_packet = eval(data_packet)
        return data_packet

    def answer(self, number, myanswer):
        """This method is used to submit an answer. It takes two arguments. The
        first  argument  is an  integer  for  the  question you  are  answering
        and  the  second   is  the  answer.  Typically  you   will  submit  the
        answer  by calling  a  function  that calculates  the  answer based  on
        the  data  element.  For   example,  after  writing  'solve_number_1()'
        you  would  submit your  answer  by  calling >>>  game_object.answer(1,
        solve_number_1(game_object.data(1)))"""
        mysocket = socket.socket()
        mysocket.connect((self.serverip, self.serverport))
        snddata(mysocket, str(number).strip() + "-A=" + str(myanswer).strip())
        data_packet = rcvdata(mysocket)
        mysocket.close()
        return data_packet
