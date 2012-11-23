from django.db import models
from django.contrib.auth.models import User

class NachaSettings(models.Model):
    """Regular Fields"""
    origin_routing_number = models.CharField(max_length=10)
    dest_routing_number   = models.CharField(max_length=10)
    origin_name           = models.CharField(max_length=30)
    dest_name             = models.CharField(max_length=30)

    """Foreign Key Fields"""
    user                  = models.ForeignKey(User)
    

class NachaHeader(models.Model):
    """Regular Fields"""
    immediate_origin      = models.CharField(max_length=10)
    immediate_destination = models.CharField(max_length=10)
    file_id_mod           = models.CharField(max_length=1)
    immediate_origin_name = models.CharField(max_length=23)
    immediate_dest_name   = models.CharField(max_length=23)

    """Foreign Key Fields"""
    user                  = models.ForeignKey(User)

class NachaBatchHeader(models.Model):
    """Enums"""
    SERV_CLS_CODES = (
        ('200', 'Debits and Credits'),
        ('220', 'Credits'),
        ('225', 'Debits'),
    )

    STD_ENT_CLS_CODES = (
        ('ARC', 'ARC'),
        ('PPD', 'PPD'),
        ('CTX', 'CTX'),
        ('POS', 'POS'),
        ('WEB', 'WEB'),
        ('BOC', 'BOC'),
        ('TEL', 'TEL'),
        ('MTE', 'MTE'),
        ('SHR', 'SHR'),
        ('CCD', 'CCD'),
        ('CIE', 'CIE'),
        ('POP', 'POP'),
        ('RCK', 'RCK'),
    )

    """Regular Fields"""
    serv_cls_code   = models.CharField(max_length=3, choices=SERV_CLS_CODES)
    company_name    = models.CharField(max_length=16)
    cmpy_dis_data   = models.CharField(max_length=20)
    company_id      = models.CharField(max_length=10)
    std_ent_cls_code= models.CharField(max_length=3, choices=STD_ENT_CLS_CODES)
    entry_desc      = models.CharField(max_length=10)
    desc_date       = models.CharField(max_length=6)
    eff_ent_date    = models.CharField(max_length=6)
    orig_stat_code  = models.CharField(max_length=1)
    orig_dfi_id     = models.CharField(max_length=8)
    batch_id        = models.CharField(max_length=7)

    """Foreign Key Fields"""
    user            = models.ForeignKey(User)
    nacha_header    = models.ForeignKey(NachaHeader)

class NachaRecordEntry(models.Model):

    TRANSACTION_CODES = (
        ('22', 'Credit to Checking Account'),
        ('27', 'Debit to Checking Account'),
        ('32', 'Credit to Savings Account'),
        ('37', 'Debit to Savings Account'),
        ('23', 'Credit Prenote to Checking Account'),
        ('28', 'Debit Prenote to Checking Account'),
        ('33', 'Credit Prenote to Savings Account'),
        ('38', 'Debit Prenote to Savings Account'),
    )

    """ Regular Fields"""
    transaction_code      = models.CharField(max_length=2, choices=TRANSACTION_CODES)
    recv_dfi_id           = models.CharField(max_length=8)
    check_digit           = models.CharField(max_length=1)
    dfi_acnt_num          = models.CharField(max_length=17)
    amount                = models.CharField(max_length=10)
    chk_serial_num        = models.CharField(max_length=15)
    ind_name              = models.CharField(max_length=22)
    disc_data             = models.CharField(max_length=2)
    id_number             = models.CharField(max_length=15)
    ind_id                = models.CharField(max_length=22)
    num_add_recs          = models.CharField(max_length=4)
    recv_cmpy_name        = models.CharField(max_length=16)
    reserved              = models.CharField(max_length=2)
    terminal_city         = models.CharField(max_length=4)
    terminal_state        = models.CharField(max_length=2)
    card_tr_typ_code_pos  = models.CharField(max_length=2)
    card_tr_typ_code_shr  = models.CharField(max_length=2)
    card_exp_date         = models.CharField(max_length=4)
    doc_ref_num           = models.CharField(max_length=11)
    ind_card_acct_num     = models.CharField(max_length=22)
    pmt_type_code         = models.CharField(max_length=2)
    add_rec_ind           = models.CharField(max_length=1)
    trace_num             = models.CharField(max_length=15)

    """Foreign Key"""
    user                = models.ForeignKey(User)
    nacha_batch_header  = models.ForeignKey(NachaBatchHeader)


