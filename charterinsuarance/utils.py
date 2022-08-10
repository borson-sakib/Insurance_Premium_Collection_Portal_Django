


from ldap3 import Server, Connection, ALL
from .models import *
def getUser(usermail):
    user = User.objects.get(email=usermail)
    context = {"user_info" : user}
    return context

def ldapcheck(username, password):
    servername= 'LDAP://10.10.100.12:389'
    server = Server(servername, get_info=ALL)  # define an unsecure LDAP server, requesting info on DSE and schema

    # define the connection
    # connection = Connection(server, auto_bind=True, user='nusher.jamil@mblbd.com', password='Nushit@123456')  # define an ANONYMOUS connection
    connection = Connection(server, user=username, password=password)  # define an ANONYMOUS connection
    # c.search('dc=mblbd,dc=com','(mail=najmus@mblbd.com)',attributes=['displayName'])
    # c.extend.standard.who_am_i()
    # print(type(c))
    # perform the Bind operation
    if not connection.bind():
        print('error in bind ', connection.result['description'])
        return False
    else:
        connection.search('dc=mblbd,dc=com','(mail={})'.format(username),attributes=['displayName'])
        displayname = str(connection.entries[0]).split("displayName:")[-1]
        connection.unbind()
        return True



def checkAuthUser( emailadrress):
    try:
        user = User.objects.get(email=emailadrress)
        if user is not None:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def getBranchNameList():
    queryset = Branch.objects.all()
    branchlist =  [x.branch_name for x in queryset ]
    return branchlist


def domainMailCheck(domainMail):
    domainMail = domainMail.lower()
    if(domainMail.endswith('@mblbd.com')):
        return domainMail

    else:
        return domainMail + '@mblbd.com'