import os
import pandas as pd
import sqlite3
from io import StringIO

from ipdb import set_trace as db, iex


res = os.get_terminal_size()
columns, lines = res.columns, res.lines


media_org_dir = os.path.expanduser('~/d/txt/todo')

@iex
def main():

    # org_table_file_to_sqlite_file(org_file=org_table_str, db_file='names-test.db', table_name='names')

    db_name = 'media.db'
    media_org_files = [
        'watch',
        'read',
        'play',
    ]
    for name in media_org_files:
        org_file = '%s/%s.txt' % (media_org_dir, name)
        print('-------------')
        print(org_file)
        org_file_to_sqlite_file(org_file, db_name)

    # sqlite3 -tabs watch.db "select * from 'movies-seen'"
    # sqlite3 test_simple.db "select * from names"
    # sqlite3 media.db ".dump"


def find_org_table_lines(org_file):
    pass


org_table_str = StringIO("""| Name | Age | City    |
|------+-----+---------|
| John |  30 | New York|
| Jane |  25 | London  |
| Mark |  35 | Paris   |
""")


def org_file_to_sqlite_file(org_file, db_file):
    with open(org_file, 'r') as f:
        lines = f.read().split('\n')

    org_table_name = ''
    header = ''
    table_lines = []
    for n, line in enumerate(lines):
        if line.startswith('*'):
            # header line
            header = line
            # print(line)
            continue

        if line.startswith('|-') or line.startswith('| <'):
            # skippable table lines
            continue

        if line.startswith('#+NAME'):
            # table name
            # print(line)
            org_table_name = ':'.join(line.split(':')[2:])
            # print(org_table_name)
            continue

        if line.startswith('|'):
            # table row
            table_lines.append(line)
        else:
            if not table_lines:
                # top of file
                continue
            # end of table
            sql_table_name = org_table_name or header or 'unknown'
            sql_table_name = sql_table_name.replace(' ', '_').replace('-', '_')

            # print(line)
            print('')
            print('%s: %d data lines' % (sql_table_name, len(table_lines)))
            table_str = '\n'.join(table_lines)
            # import this table as string data

            org_table_file_to_sqlite_file(org_string=table_str,db_file=db_file, table_name=sql_table_name)
            header = ''
            sql_table_name = ''
            table_lines = []

def org_table_file_to_sqlite_file(org_file=None, org_string=None, db_file=None, table_name=None):
    if org_string is not None:
        df = pd.read_csv(StringIO(org_string), skiprows=[1], sep='|', )
    elif org_file is not None:
        df = pd.read_csv(org_file, skiprows=[1], sep='|', )

    # remove extra columns
    num_col = len(df.columns)
    df.drop(df.columns[[0, num_col-1]], axis=1, inplace=True)

    # strip all strings in data
    df_str = df.select_dtypes('object')
    df[df_str.columns] = df_str.apply(lambda x: x.str.strip())

    # strip column names
    df = df.rename(columns=lambda x: x.strip())

    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print("Migrated to %s.%s" % (db_file, table_name))
    column_names = [s.strip() for s in df.columns.to_list()]
    print(df.columns)


main()
