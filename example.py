import xmlparser as xp

xmlobject = xp.Example()
case = xp.CaseViewer(xmlobject)

cars = case.get_vehicles()

d = xp.xml2dict(cars)
print(d)

