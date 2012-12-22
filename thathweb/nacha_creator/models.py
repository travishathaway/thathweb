from django.db import models
from django.contrib.auth.models import User

class NachaSettings(models.Model):
    """Regular Fields"""
    origin_routing_number = models.CharField(max_length=9)
    dest_routing_number   = models.CharField(max_length=9)
    origin_name           = models.CharField(max_length=30)
    dest_name             = models.CharField(max_length=30)

    """Foreign Key Fields"""
    user                  = models.ForeignKey(User)
    

class NachaHeader(models.Model):
    """Regular Fields"""
    immediate_origin      = models.CharField(max_length=10,verbose_name="Immediate Origin")
    immediate_destination = models.CharField(max_length=10,verbose_name="Immediate Destination")
    file_id_mod           = models.CharField(max_length=1,verbose_name="File ID Modifier")
    immediate_origin_name = models.CharField(max_length=23,verbose_name="Immediate Origin Name")
    immediate_dest_name   = models.CharField(max_length=23,verbose_name="Immediate Destination Name")

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
    serv_cls_code   = models.CharField(max_length=3, choices=SERV_CLS_CODES, 
                                        verbose_name="Service Class Code")
    company_name    = models.CharField(max_length=16, verbose_name="Company Name")
    cmpy_dis_data   = models.CharField(max_length=20, verbose_name="Company Discretionary Data")
    company_id      = models.CharField(max_length=10, verbose_name="Company ID")
    std_ent_cls_code= models.CharField(max_length=3, choices=STD_ENT_CLS_CODES,
                                        verbose_name="Standard Entry Class Code")
    entry_desc      = models.CharField(max_length=10, verbose_name="Entry Description")
    desc_date       = models.CharField(max_length=6, verbose_name="Description Date")
    eff_ent_date    = models.CharField(max_length=6, verbose_name="Effective Entry Date")
    orig_stat_code  = models.CharField(max_length=1, verbose_name="Originator Status Code")
    orig_dfi_id     = models.CharField(max_length=8, verbose_name="Originating DFI ID")

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
    transaction_code      = models.CharField(max_length=2, choices=TRANSACTION_CODES,
                                                verbose_name="Transaction Code")
    recv_dfi_id           = models.CharField(max_length=8, verbose_name="Routing Number")
    dfi_acnt_num          = models.CharField(max_length=17, verbose_name="Account Number")
    amount                = models.CharField(max_length=10)
    chk_serial_num        = models.CharField(max_length=15, verbose_name="Check Serial Number")
    ind_name              = models.CharField(max_length=22, verbose_name="Name")
    disc_data             = models.CharField(max_length=2, verbose_name="Discretionary Data")
    id_number             = models.CharField(max_length=15, verbose_name="ID Number")
    ind_id                = models.CharField(max_length=22, verbose_name="Individual ID")
    recv_cmpy_name        = models.CharField(max_length=16, verbose_name="Receiving Company Name")
    reserved              = models.CharField(max_length=2, verbose_name="Reserved")
    terminal_city         = models.CharField(max_length=4, verbose_name="Terminal City")
    terminal_state        = models.CharField(max_length=2, verbose_name="Terminal State")
    card_tr_typ_code_pos  = models.CharField(max_length=2, verbose_name="Card Transaction Type Code")
    card_tr_typ_code_shr  = models.CharField(max_length=2, verbose_name="Card Transaction Type Code")
    card_exp_date         = models.CharField(max_length=4, verbose_name="Card Expiration Date")
    doc_ref_num           = models.CharField(max_length=11, verbose_name="Document Reference Number")
    ind_card_acct_num     = models.CharField(max_length=22, verbose_name="Individual Card Account Number")
    pmt_type_code         = models.CharField(max_length=2, verbose_name="Payment Type Code")
    add_rec_ind           = models.CharField(max_length=1)

    """Foreign Key"""
    user                = models.ForeignKey(User)
    nacha_batch_header  = models.ForeignKey(NachaBatchHeader)


