from O365 import Tasks
e = 'evernichon@alan-allman.com'
p = 'IeGhoos0Eiph'
authenticiation = (e,p)

t = Tasks(auth=authenticiation) #Email, Password, Delay fetching so I can change the filters.

t.getTasks()

for task in t.Tasks :


    print task.getSubject()
    print task.getOwner()
    print task.getCreatedTime()
   # print m.getSenderName()
#    print m.getBody()

