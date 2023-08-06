# MODULES
import datetime

# CORE
from core import core, DB

# MODELS
from alphaz.models.tests import AlphaTest, test
from alphaz.models.database.main_definitions import Test
from alphaz.models.database.operators import Operators
from alphaz.models.database.tests import TestChild, TestChilds

# LIBS
from alphaz.libs import date_lib, json_lib

LOG = core.get_logger("tests")


def delete():
    Test.query.delete()
    Test.query.session.commit()


class Database(AlphaTest):
    connected = False

    columns = [Test.name.key, Test.text.key, Test.number.key]

    date_datetime = date_lib.str_to_datetime("2020/01/07 10:02:03")
    parameters = {
        Test.name.key: "insert",
        Test.text.key: "insert_text",
        Test.number.key: 12,
        Test.date.key: date_datetime,
    }

    select_parameters = {
        Test.name.key: "select",
        Test.text.key: "select",
        Test.number.key: 12,
    }

    test_p = {"id": 1, "name": "test", "test_child_id": 1}
    test_p_child = {"id": 1, "name": "test"}
    test_p_childs_1 = {
        "id": 1,
        "name": "test",
        "parent_id": 1,
        "child_parent_id": 1,
    }
    test_p_childs_2 = {
        "id": 2,
        "name": "test2",
        "parent_id": 1,
        "child_parent_id": 1,
    }

    def __init__(self):
        super().__init__()

        self.db = core.db
        self.connected = self.db.test()

        if not self.connected:
            LOG.error("not connected")
            return
        # self.db.session.delete(Test)
        TestChilds.query.delete()
        Test.query.delete()
        TestChild.query.delete()

    def count(self):
        rows = self.db.select(Test)
        return len(rows)

    @test(save=False)
    def connexion(self):
        return self.connected

    @test(save=False)
    def truncate(self):
        rows = self.db.select(Test)
        self.assert_length(rows, 0)

    def init_childs(self, disabled_relationships: list | dict = None) -> dict:
        Test.query.delete()
        TestChild.query.delete()
        TestChilds.query.delete()

        DB.add(TestChild(**self.test_p_child))
        DB.add(Test(**self.test_p))

        DB.add(TestChilds(**self.test_p_childs_1))
        DB.add(TestChilds(**self.test_p_childs_2))

        rows = DB.select(Test, json=True, disabled_relationships=disabled_relationships)
        return rows

    @test()
    def childs_compare_fail(self):
        rows = self.init_childs()

        full_model = {x: y for x, y in self.test_p.items()}
        full_model["test_child"] = {x: y for x, y in self.test_p_child.items()}
        full_model["test_child"]["test_childs"] = [
            self.test_p_childs_2,
            self.test_p_childs_2,
        ]
        full_model["test_childs"] = [self.test_p_childs_1, self.test_p_childs_2]

        full_model["id"] = 3

        self.assert_length(rows, 1)
        self.assert_not_equal(
            rows[0],
            full_model,
            ignore={
                "update_date": None,
                "test_child": {"update_date": None, "test_childs": ["update_date"]},
                "test_childs": ["update_date"],
            },
        )

    @test()
    def childs_compare(self):
        rows = self.init_childs()

        full_model = {x: y for x, y in self.test_p.items()}
        full_model["test_child"] = {x: y for x, y in self.test_p_child.items()}
        full_model["test_child"]["test_childs"] = [
            self.test_p_childs_1,
            self.test_p_childs_2,
        ]
        full_model["test_childs"] = [self.test_p_childs_1, self.test_p_childs_2]

        self.assert_length(rows, 1)
        self.assert_equal(
            rows[0],
            full_model,
            ignore={
                "update_date": None,
                "test_child": {"update_date": None, "test_childs": ["update_date"]},
                "test_childs": ["update_date"],
            },
        )

    @test()
    def no_test_childs_compare(self):
        rows = self.init_childs(disabled_relationships=[Test.test_childs])

        full_model = {x: y for x, y in self.test_p.items()}
        full_model["test_child"] = {x: y for x, y in self.test_p_child.items()}
        full_model["test_child"]["test_childs"] = [
            self.test_p_childs_1,
            self.test_p_childs_2,
        ]
        # full_model["test_childs"] = [self.test_p_childs_1, self.test_p_childs_2]

        self.assert_length(rows, 1)
        self.assert_equal(
            rows[0],
            full_model,
            ignore={
                "update_date": None,
                "test_child": {"update_date": None, "test_childs": ["update_date"]},
                "test_childs": ["update_date"],
            },
        )

    @test()
    def no_test_child_compare(self):
        rows = self.init_childs(disabled_relationships=[Test.test_child])

        full_model = {x: y for x, y in self.test_p.items()}
        """full_model["test_child"] = {x: y for x, y in self.test_p_child.items()}
        full_model["test_child"]["test_childs"] = [
            self.test_p_childs_1,
            self.test_p_childs_2,
        ]"""
        full_model["test_childs"] = [self.test_p_childs_1, self.test_p_childs_2]

        self.assert_length(rows, 1)
        self.assert_equal(
            rows[0],
            full_model,
            ignore={
                "update_date": None,
                "test_child": {"update_date": None, "test_childs": ["update_date"]},
                "test_childs": ["update_date"],
            },
        )

    @test()
    def no_test_child_test_childs_compare(self):
        rows = self.init_childs(
            disabled_relationships={Test.test_child: TestChild.test_childs}
        )

        full_model = {x: y for x, y in self.test_p.items()}
        full_model["test_child"] = {x: y for x, y in self.test_p_child.items()}
        """full_model["test_child"]["test_childs"] = [
            self.test_p_childs_1,
            self.test_p_childs_2,
        ]"""
        full_model["test_childs"] = [self.test_p_childs_1, self.test_p_childs_2]

        self.assert_length(rows, 1)
        self.assert_equal(
            rows[0],
            full_model,
            ignore={
                "update_date": None,
                "test_child": {"update_date": None, "test_childs": ["update_date"]},
                "test_childs": ["update_date"],
            },
        )

    @test()
    def no_test_child_test_childs_compare_notation(self):
        rows = self.init_childs(
            disabled_relationships=[
                {Test.test_child: TestChild.test_childs},
                Test.test_childs,
            ]
        )

        full_model = {x: y for x, y in self.test_p.items()}
        full_model["test_child"] = {x: y for x, y in self.test_p_child.items()}
        """full_model["test_child"]["test_childs"] = [
            self.test_p_childs_1,
            self.test_p_childs_2,
        ]"""
        # full_model["test_childs"] = [self.test_p_childs_1, self.test_p_childs_2]

        self.assert_length(rows, 1)
        self.assert_equal(
            rows[0],
            full_model,
            ignore={
                "update_date": None,
                "test_child": {"update_date": None, "test_childs": ["update_date"]},
                "test_childs": ["update_date"],
            },
        )

    @test()
    def fail_no_test_child_test_childs_compare(self):
        rows = self.init_childs(
            disabled_relationships={Test.test_child: Test.test_childs}
        )

        full_model = {x: y for x, y in self.test_p.items()}
        full_model["test_child"] = {x: y for x, y in self.test_p_child.items()}
        full_model["test_child"]["test_childs"] = [
            self.test_p_childs_1,
            self.test_p_childs_2,
        ]
        full_model["test_childs"] = [self.test_p_childs_1, self.test_p_childs_2]

        self.assert_length(rows, 1)
        self.assert_equal(
            rows[0],
            full_model,
            ignore={
                "update_date": None,
                "test_child": {"update_date": None, "test_childs": ["update_date"]},
                "test_childs": ["update_date"],
            },
        )

    @test()
    def no_test_child_and_test_childs_compare(self):
        rows = self.init_childs(
            disabled_relationships=[Test.test_child, Test.test_childs]
        )

        full_model = {x: y for x, y in self.test_p.items()}

        self.assert_length(rows, 1)
        self.assert_equal(
            rows[0],
            full_model,
            ignore={
                "update_date": None,
                "test_child": {"update_date": None, "test_childs": ["update_date"]},
                "test_childs": ["update_date"],
            },
        )

    @test(save=False, begin=delete)
    def insert(self):
        test = self.db.add(Test, self.parameters)
        rows = self.db.select(Test)
        if len(rows) == 0:
            return False
        values = {x: getattr(rows[0], x) for x in self.parameters}
        return len(rows) == 1 and values == self.parameters

    @test(save=False, begin=delete)
    def roolback(self):
        rows = self.db.select(Test)
        if len(rows) != 0:
            return False

        test = self.db.add(Test, self.parameters, commit=False, rollback=False)
        rows = self.db.select(Test)
        if len(rows) != 1:
            return False
        self.db.rollback(session=test.query.session)

        # self.db.rollback()
        rows = self.db.select(Test)

        return len(rows) == 0

    @test(save=False, begin=delete)
    def roolback_update(self):
        rows = self.db.select(Test)
        if len(rows) != 0:
            return False

        test = self.db.add(Test, self.parameters, commit=True, rollback=False)

        new_parameters = {x: y for x, y in self.parameters.items()}
        new_parameters[Test.number.key] = 13
        self.db.update(test, new_parameters, commit=False)
        self.db.rollback(session=test.query.session)

        rows = self.db.select(Test)
        if len(rows) != 1:
            return False
        return new_parameters == rows[0]

    @test(save=False, begin=delete)
    def roolback_update_2(self):
        rows = self.db.select(Test)
        if len(rows) != 0:
            return False

        test = self.db.add(Test, self.parameters, commit=True, rollback=False)

        new_parameters = {Test.number.key: 13}
        self.db.update(
            test, new_parameters, filters=[Test.name == "insert"], commit=False
        )
        self.db.rollback(session=test.query.session)

        rows = self.db.select(Test)
        if len(rows) != 1:
            return False
        return new_parameters == rows[0]

    @test(save=False, begin=delete)
    def insert2(self):
        self.db.add(
            Test,
            {
                Test.name: self.parameters[Test.name.key],
                Test.number: self.parameters[Test.number.key],
                Test.text_: self.parameters[Test.text_.key],
                Test.date: self.parameters[Test.date.key],
            },
        )
        rows = self.db.select(Test)
        if len(rows) == 0:
            return False
        values = {x: getattr(rows[0], x) for x in self.parameters}
        return len(rows) == 1 and values == self.parameters

    @test(save=False, begin=delete)
    def insert3(self):
        test = Test(**self.parameters)
        test2 = self.db.add(test)
        rows = self.db.select(Test)
        if len(rows) == 0:
            return False
        values = {x: getattr(rows[0], x) for x in self.parameters}
        return len(rows) == 1 and values == self.parameters

    @test(save=False, begin=delete)
    def select_dict(self):
        self.db.add(Test, self.parameters)
        rows = self.db.select(Test, columns=self.columns, json=True)
        LOG.info(f"Selected {len(rows)} elements, expecting 1")
        if len(rows) == 0:
            return False
        values = {x: rows[0][x] for x in self.columns}
        parameters_values = {x: self.parameters[x] for x in self.columns}
        json_values = rows[0].to_json() if hasattr(rows[0], "to_json") else rows[0]
        return (
            len(rows) == 1
            and values == parameters_values
            and len(json_values) == len(self.columns)
        )

    @test(save=False, begin=delete)
    def delete(self):
        self.db.add(Test, self.parameters)
        self.db.delete(Test, name=[Test.name == self.parameters[Test.name.key]])
        rows = self.db.select(Test)
        return len(rows) == 0

    @test(save=False, begin=delete)
    def delete2(self):
        test = Test(**self.parameters)
        self.db.add(test)
        self.db.delete(test)
        rows = self.db.select(Test)
        return len(rows) == 0

    @test(save=False, begin=delete)
    def select_unique(self):
        self.db.add(Test, self.parameters)
        rows = self.db.select(Test, unique=Test.name.key)
        valid = len(rows) == 1
        if not valid:
            return False
        return rows[0] == self.parameters[Test.name.key]

    @test(save=False, begin=delete)
    def select_unique2(self):
        self.db.add(Test, self.parameters)
        rows = self.db.select(Test, unique=Test.name)
        valid = len(rows) == 1
        if not valid:
            return False
        return rows[0] == self.parameters[Test.name.key]

    @test(save=False, begin=delete)
    def add_update(self):
        self.db.add(Test, self.parameters)
        parameters = {x: y for x, y in self.parameters.items()}
        parameters[Test.number.key] += 1
        self.db.add(Test, parameters=parameters, update=True)
        rows = self.db.select(Test)
        return len(rows) == 1 and parameters == {
            x: getattr(rows[0], x) for x in self.parameters
        }

    @test(save=False, begin=delete)
    def add_or_update(self):
        self.db.add(Test, self.parameters)
        parameters = {x: y for x, y in self.parameters.items()}
        parameters[Test.number.key] += 1
        test2 = Test(**parameters)
        self.db.add_or_update(test2)
        rows = self.db.select(Test)
        return len(rows) == 1 and parameters == {
            x: getattr(rows[0], x) for x in self.parameters
        }

    @test(save=False, begin=delete)
    def update_with_values(self):
        add = self.db.add(Test, self.parameters)
        parameters = {x: y for x, y in self.parameters.items()}
        parameters[Test.number.key] += 1
        parameters[Test.id.key] = add.id
        self.db.update(Test, values=parameters)
        rows = self.db.select(Test)
        return len(rows) == 1 and parameters == {
            x: getattr(rows[0], x) for x in parameters
        }

    @test(save=False, begin=delete)
    def update_with_model(self):
        added = self.db.add(Test, self.parameters)
        parameters = {x: y for x, y in self.parameters.items()}
        parameters[Test.number.key] += 1
        parameters[Test.id.key] = added.id
        test = Test(**parameters)
        test.query.session.commit()
        # updated = self.db.update(Test(**parameters))
        rows = self.db.select(Test)
        return len(rows) == 1 and parameters == {
            x: getattr(rows[0], x) for x in parameters
        }

    @test(save=False, begin=delete)
    def update_with_model_update(self):
        added = self.db.add(Test, self.parameters)
        parameters = {x: y for x, y in self.parameters.items()}
        parameters[Test.number.key] += 1
        parameters[Test.id.key] = added.id
        test = Test(**parameters)
        # test.query.session.commit()
        updated = self.db.update(test)
        rows = self.db.select(Test)
        return len(rows) == 1 and parameters == {
            x: getattr(rows[0], x) for x in parameters
        }

    @test(save=False, begin=delete)
    def update_with_transient_model(self):
        added = self.db.add(Test, self.parameters, commit=False)
        added.number += 1
        updated = self.db.update(added)
        rows = self.db.select(Test)
        return len(rows) == 1 and parameters == {
            x: getattr(rows[0], x) for x in parameters
        }

    @test(save=False, begin=delete)
    def update_last_with_model(self):
        added = self.db.add(Test, self.parameters)
        parameters_added = []
        for i in range(4):
            parameters = {x: y for x, y in self.parameters.items()}
            parameters[Test.number.key] += i + 1
            parameters[Test.id.key] = added.id
            updated = self.db.update(Test(**parameters))
            parameters_added.append({**parameters})
        rows = self.db.select(Test)
        return len(rows) == 1 and parameters == {
            x: getattr(rows[0], x) for x in parameters
        }

    @test(save=False, begin=delete)
    def update_multiple_with_model(self):
        parameters_list = []
        for i in range(4):
            parameters = {x: y for x, y in self.parameters.items()}
            parameters[Test.number.key] = i
            added = self.db.add(Test, parameters)
            parameters[Test.id.key] = added.id
            parameters_list.append({**parameters})

        for i in range(4):
            parameters_list[i][Test.number.key] += 1
            updated = self.db.update(Test(**parameters_list[i]))

        rows = self.db.select(Test)
        db_parameters_list = [
            {x: getattr(row, x) for x in parameters_list[i]}
            for i, row in enumerate(rows)
        ]
        A = []
        for i, db_parameters in enumerate(db_parameters_list):
            p = next(
                iter(
                    [
                        x
                        for x in parameters_list
                        if x[Test.id.key] == db_parameters[Test.id.key]
                    ]
                ),
                None,
            )
            A.append(p == db_parameters)
        return len(rows) == 4 and all(A) and len(A) == 4

    @test(save=False, begin=delete)
    def add_or_update_multiple(self):
        tests = [Test(**self.parameters)]
        for i in range(5):
            parameters = {x: y for x, y in self.parameters.items()}
            parameters[Test.number.key] += i
            tests.append(Test(**parameters))
        tests.append(Test(**self.parameters))
        self.db.add_or_update(tests)
        rows = self.db.select(Test)
        return len(rows) == 1 and self.parameters == {
            x: getattr(rows[0], x) for x in self.parameters
        }

    @test(save=False, begin=delete)
    def add_or_update_multiple2(self):
        # take the first insert
        tests = [Test(**self.parameters)]
        for i in range(5):
            parameters = {x: y for x, y in self.parameters.items()}
            parameters[Test.number.key] += i
            tests.append(Test(**parameters))
        self.db.add_or_update(tests)
        rows = self.db.select(Test)
        return len(rows) == 1 and self.parameters == {
            x: getattr(rows[0], x) for x in self.parameters
        }

    @test(save=False, begin=delete)
    def add_or_update_multiple3(self):
        tests = [Test(**self.parameters)]
        for i in range(5):
            parameters = {x: y for x, y in self.parameters.items()}
            parameters[Test.number.key] += i
            tests.append(Test(**parameters))
        parameters2 = {x: y for x, y in self.parameters.items()}
        parameters2[Test.name.key] = "new"
        tests.append(Test(**parameters2))
        self.db.add_or_update(tests)
        rows = self.db.select(Test)
        return len(rows) == len(tests) and all(
            [
                y == getattr(rows[0], x)
                for x, y in self.parameters.items()
                if x != Test.number.key
            ]
        )

    @test(description="Test session bulk update", begin=delete)
    def bulk_update(self):
        rows = self.db.select(Test)
        self.assert_is_empty(rows)

        tests = [Test(**self.parameters)]
        for i in range(5):
            parameters = {x: y for x, y in self.parameters.items()}
            parameters[Test.number.key] += i
            tests.append(Test(**parameters))
        self.db.add_or_update(tests)
        numbers = self.db.select(Test, unique=Test.number)
        self.assert_length(numbers, 5)
        self.assert_equal(set(numbers), set([12, 13, 14, 15, 16]))

        rows = self.db.select(Test)
        update_data = []
        for i, row in enumerate(rows):
            p = row.to_json()
            p[Test.number.key] = 0
            p[Test.update_date.key] = datetime.datetime.now()
            p[Test.date.key] = datetime.datetime.strptime(
                p[Test.date.key], "%Y-%m-%dT%H:%M:%S"
            )
            update_data.append(p)

        self.db.session.bulk_update_mappings(Test, update_data)
        self.db.commit()

        numbers = self.db.select(Test, unique=Test.number)
        self.assert_length(numbers, 1)
        self.assert_equal(set(numbers), set([0]))

    @test(description="Test integrated bulk update", begin=delete)
    def bulk_update_2(self):
        rows = self.db.select(Test)
        self.assert_is_empty(rows)

        tests = [Test(**self.parameters)]
        for i in range(5):
            parameters = {x: y for x, y in self.parameters.items()}
            parameters[Test.number.key] += i
            tests.append(Test(**parameters))
        self.db.add_or_update(tests)
        numbers = self.db.select(Test, unique=Test.number)
        self.assert_length(numbers, 5)
        self.assert_equal(set(numbers), set([12, 13, 14, 15, 16]))

        rows = self.db.select(Test)
        for i, row in enumerate(rows):
            row.number = 0

        self.db.commit()

        numbers = self.db.select(Test, unique=Test.number)
        self.assert_length(numbers, 1)
        self.assert_equal(set(numbers), set([0]))

    """@test(save=False)
    def upsert(self):
        Test.query.delete()
        test = Test(**self.parameters)
        self.db.add(test)
        parameters = {x:y for x,y in self.parameters.items()}
        parameters[Test.number.key] += 1
        test2 = Test(**self.parameters)
        self.db.upsert(Test,test2)
        rows    = self.db.select(Test)
        return len(rows) == 1 and parameters == {x:getattr(rows[0],x) for x in self.parameters}"""

    @test(save=False, begin=delete)
    def update_none(self):
        test = Test(**self.parameters)
        self.db.update(test)
        rows = self.db.select(Test)
        self.assert_is_empty(rows)

        self.db.update(Test, self.parameters)
        rows = self.db.select(Test)
        self.assert_is_empty(rows)

    @test(description="Test select filters on dates", begin=delete)
    def select_date_filters(self):
        tests = [Test(**self.parameters)]
        for i in range(5):
            parameters = {x: y for x, y in self.parameters.items()}
            parameters[Test.number.key] = i
            parameters[Test.date.key] = date_lib.str_to_datetime(
                "2020/01/%s 10:02:03" % (i + 1)
            )
            tests.append(Test(**parameters))
        self.db.add_or_update(tests)

        tests = self.db.select(
            Test,
            filters=[
                {Test.number: {Operators.IN: 1}},
            ],
        )
        self.assert_length(tests, 1)

        tests = self.db.select(
            Test,
            filters=[
                {Test.number: {Operators.IN: [1, 100]}},
            ],
        )
        self.assert_length(tests, 1)

        tests = self.db.select(
            Test,
            filters=[
                {
                    Test.date: {
                        Operators.SUPERIOR_OR_EQUAL: date_lib.str_to_datetime(
                            "01/01/2020 10:02:03"
                        ),
                        Operators.INFERIOR_OR_EQUAL: date_lib.str_to_datetime(
                            "03/01/2020 10:02:03"
                        ),
                    },
                },
            ],
        )
        self.assert_length(tests, 3)

        tests = self.db.select(
            Test,
            filters=[
                {
                    Test.date: {
                        Operators.BETWEEN_OR_EQUAL: (
                            date_lib.str_to_datetime("01/01/2020 10:02:03"),
                            date_lib.str_to_datetime("03/01/2020 10:02:03"),
                        )
                    },
                },
            ],
        )
        self.assert_length(tests, 3)

    @test()
    def jsonify_database_models(self):
        parameters = {x: y for x, y in self.parameters.items()}
        parameters["id"] = 0
        transient = Test(**parameters)
        model = Test

        json_transient = json_lib.jsonify_database_models(transient)
        json_model = json_lib.jsonify_database_models(model)

        self.db.add_or_update(transient)
        rows = self.db.select(Test)

        json_persistent = json_lib.jsonify_database_models(rows[0])

        same_dicts = {
            x: y for x, y in json_transient.items() if x != "update_date"
        } == {x: y for x, y in json_persistent.items() if x != "update_date"}

        return same_dicts and type(json_model) == list and type(json_model[0]) == dict
