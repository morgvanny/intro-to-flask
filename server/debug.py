#!/usr/bin/env python3
import ipdb
from app import app
from models import Production, CastMember, Role, db
if __name__ == "__main__":
    with app.app_context():
        ipdb.set_trace()
        print("bye")
