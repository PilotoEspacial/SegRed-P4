#!/usr/bin/env python3

import warnings
import requests
import os
import json

os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs"

warnings.filterwarnings("ignore")

URL = "https://myserver.local:5000"
USERS = {
    "user1": "12345Pass1.!_",
    "user2": "54321Pass2.!_",
    "user3": "12345Pass1.!_",
}


def _req(path, data=None, method="GET", check=True, token=None):
    if data:
        data = json.dumps(data)

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"token {token}"
    r = requests.request(method, f"{URL}/{path}", data=data, headers=headers)
    #print(r.text)
    if check:
        r.raise_for_status()
    return r


def login(user):
    r = _req("login", data={"username": user, "password": USERS[user]}, method="POST")
    token = r.json()
    return token["access_token"]


def test_version():
    print("+++ Testing /version... ")
    r = _req("version")
    assert r.text


def test_signup():
    print("+++ Testing /signup... ")

    for u, p in USERS.items():
        r = _req(
            "signup",
            method="POST",
            data={"username": u, "password": p},
        )
        token = r.json()
        assert token["access_token"]

    for u, p in USERS.items():
        r = _req(
            "signup", data={"username": u, "password": p}, method="POST", check=False
        )
        if r.ok:
            assert False, f"{u} already exists"


def test_login():
    print("+++ Testing /login... ")
    for u in USERS:
        login(u)

    r = _req(
        "login", data={"username": "foo", "password": "bar"}, method="POST", check=False
    )
    if r.ok:
        assert False, "user does not exist"

    r = _req(
        "login",
        data={"username": "user1", "password": "bar"},
        method="POST",
        check=False,
    )
    if r.ok:
        assert False, "not valid password for user1"


def test_create_and_update_doc():
    print("+++ Testing create docs... ")
    for u in USERS:
        token = login(u)
        r = _req(
            f"{u}/doc{u}",
            data={"doc_content": {"username": u}},
            method="POST",
            token=token,
        )
        assert r.json()["size"]

    for u in USERS:
        token = login(u)
        r = _req(
            f"{u}/doc{u}",
            data={"doc_content": {"username": u}},
            method="POST",
            token=token,
            check=False,
        )
        if r.ok:
            assert False, "document already exists"

    print("+++ Testing update docs... ")
    for u in USERS:
        token = login(u)
        r = _req(
            f"{u}/doc{u}", data={"doc_content": {"user": u}}, method="PUT", token=token
        )
        assert r.json()["size"]

    token = login("user1")
    r = _req(
        "user1/doc1234",
        data={"doc_content": {"user": "user1"}},
        method="PUT",
        token=token,
        check=False,
    )
    if r.ok:
        assert False, "document does not exist"


def test_all_docs():
    for u in USERS:
        token = login(u)
        r = _req(
            f"{u}/_all_docs",
            token=token,
        )
        docs = r.json()
        assert len(docs) == 1
        assert docs[f"doc{u}"]["user"] == u


def test_delete_docs():
    for u in USERS:
        token = login(u)
        r = _req(
            f"{u}/doc{u}",
            method="DELETE",
            token=token,
        )
        r = _req(
            f"{u}/doc{u}",
            token=token,
            check=False
        )
        if r.ok:
            assert False, f'document should be removed'

def easter_egg():
    print("\n\n")
    print("+++ Test succesfully... Thanks for this course :)")
    for i in range(1,30,2):
        print(('^'*i).center(30))

    for leg in range(3):
        print(('|||').center(30))
    print(('\_____/').center(30))
    print(' '+30*'-')
    print('($$$$) Merry Christmas & Happy New Year! ($$$$)')


def main():
    tests = [
        test_version,
        test_signup,
        test_login,
        test_create_and_update_doc,
        test_all_docs,
        test_delete_docs,
        easter_egg,
    ]
    for t in tests:
        t()
    return 0


if __name__ == "__main__":
    exit(main())
