from datetime import datetime
import pandas as pd
from flask import make_response, abort

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def invent_zip():
    return 12345

PEOPLE = pd.read_csv('ml-100k/u.user', sep='|',
        names=['user', 'age', 'sex', 'job', 'zip'])

def set_people(df):
    """
    This function set the value of PEOPLE
    :param df: the new dataframe
    :return: Nothing
    """
    global PEOPLE
    PEOPLE = df

def get_people():
    global PEOPLE
    return PEOPLE




def read_all(length=None, offset=0 ):
    """
    This function responds to a request for /people
    with the complete lists of people
    :return:        json string of list of people
    """
    PEOPLE = get_people()
    if length == None:
        length = len(PEOPLE)
    if not PEOPLE.empty:
        # select colums
        end = offset + length
        rows = PEOPLE.iloc[offset:end]
        rows = rows[['user', 'age', 'sex']]
        rows_dict = rows.to_dict(orient="records")
        users = []
        for entry in rows_dict:
            users.append({
                "user": int(entry['user']),
                "age": int(entry["age"]),
                "sex": entry["sex"],

            })
    # otherwise, nope, not found
    else:
        abort(
            404, "No users with ratings"
        )
    return users

def read_one(user_id):
    """
    This function responds to a request for /users/{user_id}
    with one matching person from people
    :param user_id:   id of user
    :return:        person matching last name
    """
    PEOPLE = get_people()
    # Does the person exist in people?
    person = PEOPLE[PEOPLE['user'] == user_id]
    if not person.empty:
        # select colums
        rows = person[['user', 'age', 'sex']]
        rows_dict = rows.to_dict(orient="records")
        users = []
        for entry in rows_dict:
            users.append({
                "user": int(entry['user']),
                "age": int(entry["age"]),
                "sex": entry["sex"],

            })
    # otherwise, nope, not found
    else:
        abort(
            404, "No user user with user_id  {user_id} ".format(user_id=user_id)
        )

    return users

def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    user_id = int(person.get("user", None))
    age = int(person.get("age", None))
    sex = person.get("sex", None)
    job = person.get("job", None)
    zip = invent_zip()

    PEOPLE = get_people()
    # Does the person exist already?
    person = PEOPLE[PEOPLE['user'] == user_id]
    if person.empty:
        dfNew = pd.DataFrame(columns=['user', 'age', 'sex', 'job', 'zip'])
        dfNew.loc[0] = [user_id, age, sex, job, zip]
        result = pd.concat([PEOPLE, dfNew])
        set_people(result)
        return make_response(
            "user {user_id} successfully created".format(user_id=user_id), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Person with user_id {user_id} already exists".format(user_id=user_id),
        )

def update(user_id, person):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Does the person exist in people?
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()

        return PEOPLE[lname]

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )


def delete(user_id):
    # todo
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )

    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )




# Create a handler for our read (GET) people
def read():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        sorted list of people
    """
    # Create the list of people from our data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]

person_test = {
    "user": 955,
    "age": 2,
    "sex":"M",
    "job": "engineer"
}
# create(person_test)