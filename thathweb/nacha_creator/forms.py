from django.forms import ModelForm
import models

class NachaSettings(ModelForm):

    class Meta:
        model = models.NachaSettings
        exclude = ('user',)

class NachaHeader(ModelForm):
    
    class Meta:
        model = models.NachaHeader
        exclude = ('user',)

class NachaBatchHeader(ModelForm):

    class Meta:
        model = models.NachaBatchHeader
        exclude = ('user','nacha_header')

class NachaRecordEntry(ModelForm):

    base_set = ['transaction_code','recv_dfi_id','check_digit','dfi_acnt_num','amount']

    

    entry_field_sets = {
        'ARC' : base_set + ['chk_serial_num','ind_name', 'disc_data'],
        'PPD' : base_set + ['id_number','ind_name','disc_data'] ,
        'CTX' : base_set + ['id_number','num_add_recs','recv_cmpy_name','disc_data'],
        'POS' : base_set + ['id_number','ind_name','card_tr_typ_code_pos'],
        'WEB' : base_set + ['id_number','ind_name','pmt_type_code'],
        'BOC' : base_set + ['chk_serial_num','ind_name', 'disc_data'],
        'TEL' : base_set + ['id_number','ind_name','disc_data'],
        'MTE' : base_set + ['ind_name','ind_id','disc_data'],
        'SHR' : base_set + ['card_exp_date','doc_ref_num','ind_card_acct_num','card_tr_typ_code_shr'],
        'CCD' : base_set + ['id_number','ind_name','disc_data'],
        'CIE' : base_set + ['ind_name','ind_id','disc_data'],
        'POP' : base_set + ['chk_serial_num','terminal_city','terminal_state','ind_name','disc_data'],
        'RCK' : base_set + ['chk_serial_num','ind_name', 'disc_data'],
    }

    class Meta:
        model = models.NachaRecordEntry
        exclude = ('user','nacha_batch_header')
