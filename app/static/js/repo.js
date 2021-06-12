//let awv = parseInt(document.getElementById('awv').value);
//let mmr = parseInt(document.getElementById('mmr').value);
//let cash_price = parseInt(document.getElementById('mmr').value);
let status = document.getElementById('status').value;
let awv = parseInt(document.getElementById('awv').value);
let mmr = parseInt(document.getElementById('mmr').value);
let cash_price = parseInt(document.getElementById('cash_price').value);
console.log("===",awv,mmr,cash_price,"===")
function financial(value) {
    if (value && value !== '') {
        let absValue = Math.abs(value);
        let returnString = Number(absValue).toLocaleString('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        });
        return value < 0 ? '(' + returnString + ')' : returnString;
    } else{
        return null;
    }
}
window.onload = function (){
    const arr = ['actual_proceeds','back_end_product_cancellation', 'insurance_claims'];
    for (let i =0; i < arr.length; i++) {
        if (['', 'None', null, 'NaN'].includes(document.getElementById(arr[i]).value))  {
            document.getElementById(arr[i]).value = 0;
        }
    }
    if (document.getElementById('vin').value) {
        decodeVin(document.getElementById('vin').value);
    }
    update_accounting();
    calc_cmp();
    calc_net();
    document.getElementById('pforma_gl').innerHTML = financial(document.getElementById('pforma_gl').innerHTML);
    document.getElementById('pforma_nrv').innerHTML = financial(document.getElementById('pforma_nrv').innerHTML);

}

function update_accounting() {
    let status = document.getElementById('status').value;
    console.log(status)
    if (status=="Sold"){
        let min_val = document.getElementById('acct_min_val');
        // min_val.value = Math.min.apply(null, [0, awv, mmr, cash_price].filter(Boolean));
        console.log('min val: ' +min_val.value);
        document.getElementById('a_min_value').innerText = 'min: ' + String(financial(min_val.value));
        let acct_gain_loss = document.getElementById('acct_gain_loss');
        let actual_proceeds = document.getElementById('actual_proceeds').value || 0;
        acct_gain_loss.value = actual_proceeds - min_val.value;
        console.log('acct_gain_loss: ' + String(acct_gain_loss.value));
        console.log('min val: ' + String(min_val.value));
        console.log(Math.min((acct_gain_loss.value/min_val.value), 0).toFixed(3));
        console.log('obj.val' + String(document.getElementById('disp_acct_diff').value));
        document.getElementById('disp_acct_diff').innerHTML = String(((acct_gain_loss.value/min_val.value)*100).toFixed(1))+'%';
        document.getElementById('acct_diff').value = (acct_gain_loss.value/min_val.value).toFixed(3);
        document.getElementById('acct_gain_loss').value =acct_gain_loss.value
        calc_gross_co();
}else{
    document.getElementById('disp_acct_diff').innerHTML = 0
    document.getElementById('acct_diff').value=0
    document.getElementById('acct_gain_loss').value =0
    document.getElementById('acct_min_val').value =0
    calc_gross_co();
}

}

function calc_cmp() {
    console.log('recalculating...');
    // calculate current month proceeds dynamically
    let cmp = document.getElementById("current_mo_proceeds_estimate");
    let est = parseInt(document.getElementById('estimated_recovery').value);
    console.log('estimated recovery: '+String(est));
    let awv = parseInt(document.getElementById('awv').value);
    console.log("awv is ===========================================>", awv, typeof(awv))
    let mmr = parseInt(document.getElementById('mmr').value);
    let cash_price = parseInt(document.getElementById('cash_price').value);
    console.log("========",awv,mmr,cash_price,"========")
    document.getElementById('acct_min_val').value = Math.min(awv,mmr,cash_price)
    let arr = [awv, mmr, cash_price];
    console.log('arr: '+ String(arr));
    if ((awv || mmr || cash_price) && est && (status === 'Repo')) {
        cmp.value = Math.min.apply(null, arr.filter(Boolean)) * (est * 0.01);
        document.getElementById('curr_mo_proceeds').innerHTML = financial(cmp.value);
    } else {
        document.getElementById('curr_mo_proceeds').innerHTML = '';
    }
    update_accounting();
    calc_net()
}

function calc_inv(d){
    if (status === 'Repo') {
        let gaap_date = new Date(d);
        //console.log(new Date().getMonth() - gaap_date.getMonth());
        document.getElementById('months_in_inventory').value = (new Date().getMonth() - gaap_date.getMonth());
        //document.getElementById('acct_repo_month').value = String(gaap_date.getMonth())+'-'+String(gaap_date.getFullYear());
    }
    check_required();
}

function calc_gross_co(){
    let balance = Math.max(document.getElementById('balance_repo_date').value, 0);
    let actual_proceeds = Math.max(document.getElementById('actual_proceeds').value, 0);
    //let back_end = document.getElementById('back_end_product_cancellations').value || 0;
    //let insurance_claims = document.getElementById('insurance_claims').value || 0;
    let eom_est = Math.max(document.getElementById('eom_gaap_proceeds_estimate').value, 0);
    let co_amt = document.getElementById('gross_co_amt');
    let curr = document.getElementById('current_mo_proceeds_estimate').value;
    console.log('curr: ' + curr);
    if (status === 'Repo') {
        if (eom_est === 0){
            co_amt.value = curr - balance;
        } else{
            co_amt.value = eom_est - balance;
        }

        //console.log(status, co_amt.value, eom_est, balance);
    } else {
        co_amt.value = actual_proceeds - balance;
        //console.log(status, co_amt.value, eom_est, balance);
    }
    document.getElementById('gross_co_amount').innerHTML = financial(co_amt.value);
    document.getElementById('eom-gaap-proceeds').innerHTML = financial(eom_est);
    //}

}

function calc_net(){
    let net_loss_gain = document.getElementById('net_loss_or_gain');
    let gross_co = parseFloat(document.getElementById('gross_co_amt').value)
    let discount = Math.max(parseFloat(document.getElementById('unearned_discount').value), 0) ;
    net_loss_gain.value = gross_co + discount;
    document.getElementById('disp_net_loss_or_gain').innerText = financial(gross_co + discount);
}


function check_required() {
    //let year = document.getElementById('year').value;
    let loan = document.getElementById('loan').value;
    let gaap = document.getElementById('gaap_date').value;
    let valueList =  [loan, gaap];
    console.log(valueList)
    const test = (element) => element === "";
    // if sold require date_sold ...OCO...Reinstate...
    document.getElementById("submit_button").disabled = valueList.some(test);
}

function deleteMe() {
    let loan = document.getElementById('loan').value;
    let r = confirm("Are you sure you want to delete " + loan + "?");
    if (r) {

        let data = {'loan': loan}
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/delete-repo', false);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.send(JSON.stringify(data));
        let msg = 'Deleted '+loan;
        location.replace(window.location.pathname = "/repo-log?msg="+msg)
    }

}

function confirm_status(changed_status){
    let loan = document.getElementById('status').value;
    console.log(loan)
    if (loan === 'Repo') {
        let r = confirm("Do you want to change the status to " + changed_status + "?");
        if (r) {
            document.getElementById('status').value = changed_status;
        }
    }
}