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

    with open("input.csv", 'rt') as input:
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
            specimen_code       = row[9]

            responsible = {
                "id":"",
                "unique_id":people_email,
                "firstname":people_name,
                "lastname":"",
                "email":people_email,
                "phone":people_phone,
                "community":people_community
            }

            if(responsible["unique_id"] is None):
                responsible["unique_id"] = responsible["phone"]

            species = {
                "id":"",
                "name":species_name,
                "scientific_name":species_name,
                "alias":species_name,
                "description":species_name,
                "leaf_type":species_name,
                "water_requirements":species_name,
                "sun_exposure":species_name,
                "image_url":species_name
            }

            specimen = {
                "id":"",
                "code":specimen_code,
                "map_code":specimen_map_code,
                "plant_date":specimen_plant_date,
                "irrigation_date":specimen_plant_date,
                "species_id":""
            }


            # Insert species
            try:
                sql_input = """INSERT INTO `plants_species` (`id`, `name`, `scientific_name`, `alias`, `description`, `leaf_type`, `water_requirements`, `sun_exposure`, `image_url`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"""
                sql_input = sql_input.format(species["name"], species["scientific_name"], species["alias"], species["description"], species["leaf_type"], species["water_requirements"], species["sun_exposure"], species["image_url"])
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
                sql_input = "INSERT INTO `plants_specimen` (`id`, `code`, `map_code`, `plant_date`, `irrigation_date`, `species_id`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}');"
                sql_input = sql_input.format(specimen["code"], specimen["map_code"], specimen["plant_date"], specimen["irrigation_date"], species_id)
                # print(sql_input)
                x.execute(sql_input)
                conn.commit()

                print("UPLOADED SPECIMEN: "+specimen["code"])
            except Exception as e:
                conn.rollback()
                # print("error")
                print(e)

            specimen_id = None
            responsible_id = None

            # Get specimen
            try:
                sql_input = "SELECT * FROM plants_specimen WHERE plants_specimen.code = '{}'".format(specimen["code"])
                x.execute(sql_input)
                sql_row = x.fetchone()
                while sql_row is not None:
                  specimen_id = sql_row[0]
                  sql_row = x.fetchone()

            except Exception as e:
                print(e)
                # conn.rollback()

            #insert Responsible
            if responsible["unique_id"]:
                try:
                    sql_input = "INSERT INTO `people_responsible` (`id`, `unique_id`, `firstname`, `lastname`, `email`, `phone`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}');"
                    sql_input = sql_input.format(responsible["unique_id"], responsible["firstname"], responsible["lastname"], responsible["email"], responsible["phone"])
                    x.execute(sql_input)
                    conn.commit()
                    # responsible_id = x.lastrowid
                    print("UPLOADED RESPONSIBLE: "+responsible["firstname"])
                except Exception as e:
                    conn.rollback()
                    print(e)

                #Get responsible
                try:
                    sql_input = "SELECT * FROM people_responsible WHERE people_responsible.unique_id = '{}'".format(responsible["unique_id"])
                    x.execute(sql_input)
                    sql_row = x.fetchone()

                    if sql_row[1] is not None:
                        responsible_id = sql_row[0]
                    else:
                        print("none")

                except Exception as e:
                    conn.rollback()

                # insert Responsible specimen asociation
                try:
                    sql_input = "INSERT INTO `people_responsible_specimens` (`id`, `responsible_id`, `specimen_id`) VALUES (NULL, '{}', '{}');"
                    sql_input = sql_input.format(responsible_id, specimen_id)
                    x.execute(sql_input)
                    conn.commit()
                    # responsible_id = x.lastrowid
                    print("LINKED {}<-->{}".format(responsible_id, specimen_id))
                except Exception as e:
                    conn.rollback()
                    print(e)

            print(responsible_id)
            print(specimen_id)

    conn.close()

main()

print("Thanks for use :)")
