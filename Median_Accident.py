import pymysql

myConnection = pymysql.connect(db = 'accidents')
cur = myConnection.cursor()

cur.execute('SELECT vtype FROM vehicle_type WHERE vtype LIKE "%otorcycle%";')
cycleList = cur.fetchall()

selectSQL = ('''
SELECT t.vtype, a.accidents_severity
FROM accidents_2015 AS a
JOIN vehicles_2015 AS v
ON a.accidents_index = v.accidents_index
JOIN vehicle_type AS t 
ON v.vehicle_type = t.vcode
WHERE t.vtype LIKE %s
ORDER BY a.accidents_severity;
''')

insertSQL = ('''
INSERT INTO accident_median VALUES (%s, %s);
''')

for cycle in cycleList:
    cur.execute(selectSQL, cycle[0])
    accidents = cur.fetchall()
    quotient, remainder = divmod(len(accidents), 2)
    if remainder:
        med_sev = accidents[quotient][1]
    else:
        med_sev = (accidents[quotient][1] + accidents[quotient + 2][1])/2
    print('Finding the median for ', cycle[0])
    cur.execute(insertSQL, (cycle[0], med_sev))

myConnection.commit()
myConnection.close()