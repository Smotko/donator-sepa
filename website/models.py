from django.db import connection

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_payments_list(*args):
    
    cursor = connection.cursor()
    
    sql = "SELECT p.*, a.*, pr.name_project, b.sifra_banke as bic, trr.id_trr "\
        + "FROM agreement_pay_installment as p, sfr_agreement as a, sfr_bank as b, sfr_project as pr "\
        + "JOIN sfr_project_trr as trr ON trr.id_vrstica = "\
        + "   (SELECT id_vrstica FROM sfr_project_trr WHERE id_project = pr.id_project LIMIT 1)  "\
        + "WHERE p.id_agreement = a.id_agreement AND p.pay_type='04' "\
        + "  AND pr.id_project = a.id_project AND trr.id_project = a.id_project "\
        + "  AND b.sifra_banke ILIKE a.sifra_banke || '%%' "
    
    if len(args) == 1:
        sql += "  AND p.id_vrstica = %s "
    else:
        sql += "  AND p.date_activate = %s AND a.id_project = %s "
             
    sql += "ORDER BY a.sifra_banke"
    cursor.execute(sql, args)
    return dictfetchall(cursor)
    
def get_payments_details(payment):
    cursor = connection.cursor()
    
