def check_blacklist_emails(email):
    if ";" in email:
        parts = email.split(";")
        if parts[0].strip() and remove_bad_emails(parts[0].strip(), connection):
            parts[0] = ""
        if len(parts) > 1 and parts[1].strip() and remove_bad_emails(parts[1].strip(), connection):
            parts[1] = ""
        email = ";".join(parts)
    else:
        email = remove_bad_emails(email, connection)
        email = ""
    return email = ""


def remove_bad_emails(email):
    sql = 'SELECT * FROM blacklist_emails WHERE email = %s LIMIT 1'
    cursor.execute(sql, (email,))
    if cursor.fetchone() is not None:
        return email