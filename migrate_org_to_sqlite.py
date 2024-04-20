import pandas as pd
import sqlite3
from io import StringIO

from ipdb import set_trace as db, iex


@iex
def main():
    org_table_file_to_sqlite_file(org_file=org_table_str, db_file='names-test.db', table_name='names')


def find_org_table_lines(org_file):
    pass


org_table_str = StringIO("""| Name | Age | City    |
|------+-----+---------|
| John |  30 | New York|
| Jane |  25 | London  |
| Mark |  35 | Paris   |
""")



def org_table_file_to_sqlite_file(org_file, db_file, table_name):
    df = pd.read_csv(org_file, skiprows=[1], sep='|', )
    num_col = len(df.columns)
    df.drop(df.columns[[0, num_col-1]], axis=1, inplace=True)
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

    # sqlite3 test_simple.db "select * from names"
    print("Migration complete.")


main()