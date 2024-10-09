/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
$('.form-group').removeClass('row');

$(function() {

    $('#form-register').attr('novalidate', 'novalidate');
    $('#form-investor').attr('novalidate', 'novalidate');
    $('#form-deposit').attr('novalidate', 'novalidate');
    $('#form-deposit-create').attr('novalidate', 'novalidate');

    $('.datepicker_birth').datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: '-80:-17',
        dateFormat:'yy-mm-dd',
        defaultDate:"-17y-m-d"
    });

    $('.datepicker_depositdate, .datepicker_withdrawaldate, .datepicker_rolloverdate').datepicker({
        dateFormat:'yy-mm-dd',
        maxDate: '0'
    });

    $('.deposit').unbind('change');

    $('.deposit').on('change', function(e){

        e.preventDefault();

        if ($(this).val() == ''){
            $('.withdrawal_amount, .withdrawal_date, .rollover_amount, .rollover_date, .rollover_return, .bank_acc_name, .bank_name, .bank_acc_no').val('');
            $('.rollover_tenor').prop('checked', false);
        } else {
            $.ajax({
                type: 'get',
                url: 'get_deposit',
                dataType: 'json',
                data: {deposit_id: $(this).val()}
            }).done(function(data){
                $('.withdrawal_amount, .rollover_amount').val(data[0].amount);
                $('.withdrawal_date, .rollover_date').val(data[0].withdrawal_date);
                $('.rollover_return').val(data[0].invest_return);
                $('.bank_acc_name').val(data[0].bank_acc_name);
                $('.bank_name').val(data[0].bank_name);
                $('.bank_acc_no').val(data[0].bank_acc_no);

                $('.rollover_tenor').each(function(i){
                    if ($(this).val() == data[0].invest_tenor) {
                        $(this).prop('checked', true)
                    }
                });
            });
        }
    });


    var officeForm = $('#form-office');
    $officeProvSelect = officeForm.find('select[name="province"]');
    $officeCitySelect = officeForm.find('select[name="city"]');

    $officeProvSelect.on('change', function(e){

        e.preventDefault();

        var provinceId = $(this).val();
        var cityId = $officeCitySelect.val();
        var options = '<option value>---------</option>';

        $officeCitySelect.empty();
        $officeCitySelect.html(options);

        if(provinceId){
            $.ajax({
              url: 'cities',
              type: 'get',
              dataType: 'json',
              data: { term: provinceId }
            }).done(function(data) {
                for (var i = 0; i < data.length; i++){
                    var isSelected = data[i].id == cityId ? 'selected="selected"' : '';
                    options += '<option value="'+data[i].id+'" '+isSelected+'>'+data[i].name+'</option>';
                }

              $officeCitySelect.html(options);
            });
        }

    });
    $officeProvSelect.trigger('change');



    var registerForm = $('#form-register');
    $agentProvSelect = registerForm.find('select[name="agent-province"]');
    $agentCitySelect = registerForm.find('select[name="agent-city"]');


    $agentProvSelect.on('change', function(e){

        e.preventDefault();

        var provinceId = $(this).val();
        var cityId = $agentCitySelect.val();
        var options = '<option value>-----</option>';
        $agentCitySelect.empty();
        $agentCitySelect.html(options);

        if(provinceId){
            $.ajax({
              url: 'cities',
              type: 'get',
              dataType: 'json',
              data: { term: provinceId }
            }).done(function(data) {
                for (var i = 0; i < data.length; i++){
                    var isSelected = data[i].id == cityId ? 'selected="selected"' : '';
                    options += '<option value="'+data[i].id+'" '+isSelected+'>'+data[i].name+'</option>';
                }

              $agentCitySelect.html(options);
            });
        }

    });
    $agentProvSelect.trigger('change');



    $provinceInvestSelect = registerForm.find('select[name="investor-province"]');
    $cityInvestSelect = registerForm.find('select[name="investor-city"]');

    $provinceInvestSelect.on('change', function(){
    
        var provinceId = $(this).val();
        var cityId = $cityInvestSelect.val();
        var options = '<option value>---------</option>';

        $cityInvestSelect.empty();
        $cityInvestSelect.html(options);

        if(provinceId){
            $.ajax({
              url: 'cities',
              type: 'get',
              dataType: 'json',
              data: { term: provinceId }
            }).done(function(data) {
                for (var i = 0; i < data.length; i++){
                    var isSelected = data[i].id == cityId ? 'selected="selected"' : '';
                    options += '<option value="'+data[i].id+'" '+isSelected+'>'+data[i].name+'</option>';
                }

              $cityInvestSelect.html(options);
            });
        }

    });
    $provinceInvestSelect.trigger('change');



    $("[name=investor-investor_type]").on("click", function(){

        $('.div_pic').hide();
        $('.div_pic_position').hide();

        $('.val_pic_corporate').val('');
        $('.val_pic_position').val('');

        var type = $('[name=investor-investor_type]:checked').val();
        if(type=='individual'){

            investor_type = "individual";

        }else{
            
            $('.div_pic').show();
            $('.div_pic_position').show();

            investor_type = "corporate";
        }

        sessionStorage.setItem("investor_type", investor_type);

    });


    var type = $('[name=investor-investor_type]:checked').val();

    $('.div_pic').show();
    $('.div_pic_position').show();

    if (type=='individual') {
        $('.div_pic').hide();
        $('.div_pic_position').hide();

        sessionStorage.setItem("investor_type", "individual");
    } else {
        sessionStorage.setItem("investor_type", "corporate");
    }

    investor_type = sessionStorage.getItem("investor_type");
    if (investor_type=="corporate") {
        $('input[name="deposit-deposit_type"]').removeAttr("checked");
        $('input[name="deposit-deposit_type"][value="gross"]').attr('checked', 'checked');
        $('input[name="deposit-deposit_type"][value="netto"]').attr('disabled', 'true');
    }


    $(".investor_name").keyup(function(e) {
        e.preventDefault();

        $('.investor_bank_acc_name').val($(this).val());
    });


    $('.deposit_value, .withdrawal_amount, .rollover_amount').mask('000.000.000.000.000', {reverse: true});
    $('.return_value').mask('00.00', {reverse: true});


    $(".submit-deposit").click(function(){
        $(".deposit_value").unmask();
    });

    $(".submit-withdrawal").click(function(){
        $(".withdrawal_amount").unmask();
    })


    $(".submit-investor").click(function(){

        sessionStorage.removeItem("investor_type");
        var type = $('[name=investor-investor_type]:checked').val();
        if(type=="individual"){
            sessionStorage.setItem("investor_type", "individual");
        }else{
            sessionStorage.setItem("investor_type", "corporate");
        }

        var investor_bank_acc_name = $(".investor_bank_acc_name").val();
        var investor_bank_name = $(".investor_bank_name").val();
        var investor_bank_acc_no = $(".investor_bank_acc_no").val();

        sessionStorage.setItem("investor_bank_acc_name", investor_bank_acc_name);
        sessionStorage.setItem("investor_bank_name", investor_bank_name);
        sessionStorage.setItem("investor_bank_acc_no", investor_bank_acc_no);
    });


    var investor_bank_acc_name = sessionStorage.getItem("investor_bank_acc_name");
    var investor_bank_name = sessionStorage.getItem("investor_bank_name");
    var investor_bank_acc_no = sessionStorage.getItem("investor_bank_acc_no");

    if(investor_bank_acc_name && investor_bank_name){
        $('.deposit_bank_acc_name').val(investor_bank_acc_name);
        $('.deposit_bank_name').val(investor_bank_name);
        $('.deposit_bank_acc_no').val(investor_bank_acc_no);
    }

    sessionStorage.removeItem("investor_bank_acc_name");
    sessionStorage.removeItem("investor_bank_name");
    sessionStorage.removeItem("investor_bank_acc_no");

    $('.investor-choose').on('change', function(){
        var investor_name = $(".investor-choose :selected").text();
        var valselected = $(".investor-choose :selected").val();

        $('.npwp_investor').val('');

        $('#details-investor').hide();

        if(valselected){
            $.ajax({
              url: 'getinvestor',
              type: 'get',
              dataType: 'json',
              data: { term: valselected }
            }).done(function(data) {

                $('#details-investor').show();

                var valtax = data[0]['tax_id_no'];
                var valtype = data[0]['investor_type'];

                $('input[name="deposit_type"]').removeAttr("checked");
                $('input[name="deposit_type"]').removeAttr("disabled");

                if(valtype=="corporate"){
                    $('input[name="deposit_type"][value="gross"]').attr('checked', 'true');
                    $('input[name="deposit_type"][value="netto"]').attr('disabled', 'true');
                }else{
                    $('input[name="deposit_type"][value="netto"]').attr('checked', 'true');
                }

                $('.npwp_investor').val(valtax);
                $('.data-investor-type').html('<input class="form-control" type="text" name="optradio" value="'+valtype+'" readonly>');

            });
        }

    });
    $('.investor-choose').trigger('change');

    $('input[name="deposit-product_type"][value="isprint"]').attr('disabled', 'true');
    $('input[name="product_type"][value="isprint"]').attr('disabled', 'true');

    $("#id_agent-photo").change(function(){
        readURL(this);
    });
    $("#id_agent-photo").trigger('change');

    $("[data-fancybox]").fancybox();

});


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function (e) {
            $('#show-image').attr("width","110");
            $('#show-image').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}
