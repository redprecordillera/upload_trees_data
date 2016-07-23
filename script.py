from random import randrange
import csv
import MySQLdb
conn = MySQLdb.connect(
    host= "localhost",
    user="root",
    passwd="root",
    db="mcueto_reforestacionpanul",
    unix_socket="/opt/lampp/var/mysql/mysql.sock"
    )
x = conn.cursor()


def main():

    with open("backup.csv", 'rt') as input:
        reader = csv.reader(input, delimiter = ',')

        all = []
        row = next(reader)

        for k, row in enumerate(reader):

            people_name         = row[1]
            people_phone        = row[2]
            if(people_phone is None):
                people_phone = "somephone"
            people_email        = row[3]
            if(people_email is None):
                people_email = "somemail"
            people_community    = row[4]

            species_name        = row[5]

            specimen_map_code   = row[0]
            specimen_location   = row[6]
            specimen_plant_date = row[7]
            specimen_code       = row[8]

            responsible = {
                "id":"",
                "firstname":people_name,
                "lastname":"",
                "email":people_email,
                "phone":people_phone,
                "community":people_community
            }

            species = {
                "id":"",
                "name":species_name,
                "alias":species_name,
                "description":species_name,
                "image_url":species_name
            }

            specimen = {
                "id":"",
                "code":specimen_code,
                "map_code":specimen_map_code,
                "plant_date":specimen_plant_date,
                "species_id":""
            }


            # Insert species
            try:
                sql_input = """INSERT INTO `plants_species` (`id`, `name`, `alias`, `description`, `image_url`) VALUES (NULL, '{}', '{}', '{}', '{}');"""
                sql_input = sql_input.format(species["name"], species["alias"], species["description"], species["image_url"])
                x.execute(sql_input)
                conn.commit()
                # print("Inserted: "+species["name"])
            except Exception as e:
                conn.rollback()

            species_id = None

            #Get specie
            try:
                sql_input = "SELECT * FROM plants_species WHERE plants_species.name = '{}'".format(species["name"])
                x.execute(sql_input)
                sql_row = x.fetchone()
                while sql_row is not None:
                  species_id = sql_row[0]
                  sql_row = x.fetchone()

            except Exception as e:
                print(e)
                # conn.rollback()



            #Insert specimen
            try:
                sql_input = "INSERT INTO `plants_specimen` (`id`, `code`, `map_code`, `plant_date`, `species_id`) VALUES (NULL, '{}', '{}', CURRENT_DATE(), '{}');"
                sql_input = sql_input.format(specimen["code"], specimen["map_code"], species_id)
                # print(sql_input)
                x.execute(sql_input)
                conn.commit()
                # print("Inserted: "+specimen["code"])
            except Exception as e:
                conn.rollback()
                # print("error")
                # print(e)

            responsible_id = None

            #Get responsible

            #insert Responsible
            try:
                sql_input = "INSERT INTO `people_responsible` (`id`, `firstname`, `lastname`, `email`, `phone`) VALUES (NULL, '{}', '{}', '{}', '{}');".format(responsible["firstname"], responsible["firstname"], responsible["email"], responsible["phone"])
                x.execute(sql_input)
                conn.commit()
                # responsible_id = x.lastrowid
                # print("Inserted: "+specimen["code"])
            except Exception as e:
                conn.rollback()
                # print("error")
                # print(e)


            try:
                sql_input = "SELECT * FROM people_responsible WHERE people_responsible.email = '{}'".format(responsible["email"])
                # print(sql_input)
                x.execute(sql_input)
                sql_row = x.fetchone()

                responsible_id = sql_row[0]
                # print(sql_row)

            except Exception as e:
                # print(e)
                conn.rollback()

            # print(responsible_id)

    conn.close()

main()

print("Thanks for use :)")
